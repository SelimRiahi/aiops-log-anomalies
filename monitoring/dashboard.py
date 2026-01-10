"""
Monitoring Dashboard using Streamlit
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path
import sys
import json

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from monitoring.metrics_tracker import metrics_tracker
from monitoring.drift_detection import drift_detector

st.set_page_config(
    page_title="MLOps Monitoring Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🔍 Fraud Detection - MLOps Monitoring Dashboard")

# Sidebar
st.sidebar.header("⚙️ Controls")
refresh = st.sidebar.button("🔄 Refresh Data")
time_window = st.sidebar.selectbox(
    "Time Window",
    ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days"],
    index=2
)

# Load data from file (dashboard runs in separate container)
@st.cache_data(ttl=5)
def load_predictions():
    """Load predictions from metrics file"""
    metrics_file = Path(__file__).parent.parent / 'logs' / 'metrics.jsonl'
    
    if not metrics_file.exists():
        return pd.DataFrame()
    
    predictions = []
    with open(metrics_file, 'r') as f:
        for line in f:
            try:
                predictions.append(json.loads(line))
            except:
                pass
    
    if predictions:
        df = pd.DataFrame(predictions)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return pd.DataFrame()

# Load data
df = load_predictions()

# Calculate stats from file data
if len(df) > 0:
    stats = {
        'total_predictions': len(df),
        'fraud_detected': df['is_fraud'].sum(),
        'fraud_rate': df['is_fraud'].mean(),
        'avg_response_time_ms': df['response_time_ms'].mean(),
        'uptime_hours': (datetime.now() - df['timestamp'].min()).total_seconds() / 3600
    }
else:
    stats = {
        'total_predictions': 0,
        'fraud_detected': 0,
        'fraud_rate': 0.0,
        'avg_response_time_ms': 0.0,
        'uptime_hours': 0.0
    }

# Main metrics
st.header("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Predictions",
        f"{stats['total_predictions']:,}",
        help="Total number of predictions made"
    )

with col2:
    st.metric(
        "Frauds Detected",
        f"{stats['fraud_detected']:,}",
        delta=f"{stats['fraud_rate']*100:.1f}%",
        help="Number and percentage of frauds detected"
    )

with col3:
    st.metric(
        "Avg Response Time",
        f"{stats['avg_response_time_ms']:.2f} ms",
        help="Average API response time"
    )

with col4:
    st.metric(
        "Uptime",
        f"{stats['uptime_hours']:.1f} hrs",
        help="System uptime"
    )

# Time series chart
# Time series chart
st.header("📊 Prediction Timeline")

if len(df) > 0:
    hours_map = {
        "Last Hour": 1,
        "Last 6 Hours": 6,
        "Last 24 Hours": 24,
        "Last 7 Days": 168
    }
    
    # Filter by time window
    cutoff_time = datetime.now() - timedelta(hours=hours_map[time_window])
    ts_data = df[df['timestamp'] >= cutoff_time].copy()
    
    if not ts_data.empty:
        # Resample by hour
        ts_hourly = ts_data.set_index('timestamp').resample('1H').agg({
            'is_fraud': 'sum',
            'reconstruction_error': 'mean',
            'response_time_ms': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=ts_hourly['timestamp'],
            y=ts_hourly['is_fraud'],
            name='Frauds Detected',
            mode='lines+markers',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title='Frauds Detected Over Time',
            xaxis_title='Time',
            yaxis_title='Count',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Reconstruction error over time
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=ts_hourly['timestamp'],
            y=ts_hourly['reconstruction_error'],
            name='Avg Reconstruction Error',
            mode='lines',
            fill='tozeroy',
            line=dict(color='blue', width=2)
        ))
        
        fig2.update_layout(
            title='Average Reconstruction Error Over Time',
            xaxis_title='Time',
            yaxis_title='MSE',
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info(f"No data available for {time_window}")
else:
    st.info("No predictions yet. Waiting for API calls...")

# Fraud by transaction type
st.header("📋 Fraud by Transaction Type")

if len(df) > 0 and 'transaction_type' in df.columns:
    fraud_by_type = df[df['is_fraud']].groupby('transaction_type').size().to_dict()
    
    if fraud_by_type:
        fig3 = go.Figure(data=[
            go.Bar(
                x=list(fraud_by_type.keys()),
                y=list(fraud_by_type.values()),
                marker_color='crimson'
            )
        ])
        
        fig3.update_layout(
            title='Frauds Detected by Transaction Type',
            xaxis_title='Transaction Type',
            yaxis_title='Count',
            height=400
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No fraud detected yet")
else:
    st.info("No fraud detected yet")

# Recent predictions table
st.header("🕐 Recent Predictions")

if len(df) > 0:
    df_recent = df.sort_values('timestamp', ascending=False).head(20)
    
    # Format for display
    display_df = df_recent[[
        'timestamp', 'is_fraud', 'reconstruction_error', 
        'response_time_ms', 'transaction_type', 'transaction_amount'
    ]].copy()
    
    display_df['is_fraud'] = display_df['is_fraud'].apply(
        lambda x: '🚨 FRAUD' if x else '✅ Normal'
    )
    
    display_df.columns = [
        'Timestamp', 'Status', 'Error', 'Response (ms)', 'Type', 'Amount'
    ]
    
    st.dataframe(display_df, use_container_width=True, height=400)
else:
    st.info("No predictions yet")

# Drift detection section
st.header("⚠️ Data Drift Detection")

drift_file = Path(__file__).parent.parent / 'logs' / 'drift_reports.jsonl'

if drift_file.exists():
    # Load latest drift report
    with open(drift_file, 'r') as f:
        lines = f.readlines()
        if lines:
            latest_report = json.loads(lines[-1])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                drift_status = "🔴 DRIFTED" if latest_report['is_drifted'] else "🟢 STABLE"
                st.metric("Drift Status", drift_status)
            
            with col2:
                st.metric(
                    "Drifted Columns",
                    f"{latest_report['num_drifted']} / {latest_report['num_tested']}"
                )
            
            with col3:
                st.metric(
                    "Severity",
                    f"{latest_report['drift_severity']*100:.1f}%"
                )
            
            st.info(f"**Recommendation:** {latest_report['recommendation']}")
            
            # Show drifted columns
            if latest_report['drifted_columns']:
                st.warning(f"Drifted columns: {', '.join(latest_report['drifted_columns'])}")
        else:
            st.info("No drift reports yet. Run drift detection.")
else:
    st.info("No drift reports yet. Run drift detection first.")

# Footer
st.markdown("---")
st.caption(f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
