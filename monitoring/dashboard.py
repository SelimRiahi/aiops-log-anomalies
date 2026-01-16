"""
Enhanced Multi-Page Monitoring Dashboard using Streamlit
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path
import sys
import json
import numpy as np

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from monitoring.metrics_tracker import metrics_tracker
from monitoring.drift_detection import drift_detector

st.set_page_config(
    page_title="MLOps Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio(
    "Select Dashboard",
    ["📊 Overview", "🔬 Deep Analytics", "🎯 Model Performance", "⚡ Real-Time Monitor", "📈 Business Insights"]
)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Controls")
refresh = st.sidebar.button("🔄 Refresh Data")
time_window = st.sidebar.selectbox(
    "Time Window",
    ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days", "All Time"],
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

def filter_by_time_window(df, time_window):
    """Filter dataframe by time window"""
    if len(df) == 0 or time_window == "All Time":
        return df
    
    hours_map = {
        "Last Hour": 1,
        "Last 6 Hours": 6,
        "Last 24 Hours": 24,
        "Last 7 Days": 168
    }
    
    cutoff_time = datetime.now() - timedelta(hours=hours_map.get(time_window, 24))
    return df[df['timestamp'] >= cutoff_time].copy()

# Load data
df = load_predictions()
df_filtered = filter_by_time_window(df, time_window)

# Calculate stats from file data
if len(df_filtered) > 0:
    stats = {
        'total_predictions': len(df_filtered),
        'fraud_detected': df_filtered['is_fraud'].sum(),
        'fraud_rate': df_filtered['is_fraud'].mean(),
        'avg_response_time_ms': df_filtered['response_time_ms'].mean(),
        'uptime_hours': (datetime.now() - df['timestamp'].min()).total_seconds() / 3600 if len(df) > 0 else 0
    }
else:
    stats = {
        'total_predictions': 0,
        'fraud_detected': 0,
        'fraud_rate': 0.0,
        'avg_response_time_ms': 0.0,
        'uptime_hours': 0.0
    }

# ==================== PAGE 1: OVERVIEW ====================
if page == "📊 Overview":
    st.title("🔍 Fraud Detection - Overview Dashboard")
    
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
    st.header("📊 Prediction Timeline")
    
    if len(df_filtered) > 0:
        # Resample by hour
        ts_hourly = df_filtered.set_index('timestamp').resample('1H').agg({
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
            line=dict(color='red', width=2),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            title='Frauds Detected Over Time',
            xaxis_title='Time',
            yaxis_title='Count',
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No data available for {time_window}")
    
    # Fraud by transaction type
    st.header("📋 Fraud by Transaction Type")
    
    if len(df_filtered) > 0 and 'transaction_type' in df_filtered.columns:
        fraud_by_type = df_filtered[df_filtered['is_fraud']].groupby('transaction_type').size()
        
        if len(fraud_by_type) > 0:
            fig3 = go.Figure(data=[
                go.Pie(
                    labels=fraud_by_type.index,
                    values=fraud_by_type.values,
                    hole=0.4,
                    marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
                )
            ])
            
            fig3.update_layout(
                title='Fraud Distribution by Transaction Type',
                height=400
            )
            
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No fraud detected yet")
    else:
        st.info("No fraud detected yet")
    
    # Recent predictions table
    st.header("🕐 Recent Predictions")
    
    if len(df_filtered) > 0:
        df_recent = df_filtered.sort_values('timestamp', ascending=False).head(20)
        
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

# ==================== PAGE 2: DEEP ANALYTICS ====================
elif page == "🔬 Deep Analytics":
    st.title("🔬 Deep Analytics Dashboard")
    
    if len(df_filtered) > 0:
        # Error distribution analysis
        st.header("📊 Reconstruction Error Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=df_filtered['reconstruction_error'],
                nbinsx=50,
                name='All Transactions',
                marker_color='lightblue',
                opacity=0.7
            ))
            
            # Add threshold line
            if 'threshold' in df_filtered.columns:
                threshold = df_filtered['threshold'].iloc[0]
                fig_hist.add_vline(x=threshold, line_dash="dash", line_color="red", 
                                   annotation_text=f"Threshold: {threshold:.4f}")
            
            fig_hist.update_layout(
                title='Reconstruction Error Distribution',
                xaxis_title='Reconstruction Error',
                yaxis_title='Frequency',
                height=400
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot by fraud status
            fig_box = go.Figure()
            
            fraud_data = df_filtered[df_filtered['is_fraud']]['reconstruction_error']
            normal_data = df_filtered[~df_filtered['is_fraud']]['reconstruction_error']
            
            fig_box.add_trace(go.Box(y=normal_data, name='Normal', marker_color='green'))
            fig_box.add_trace(go.Box(y=fraud_data, name='Fraud', marker_color='red'))
            
            fig_box.update_layout(
                title='Error Distribution: Normal vs Fraud',
                yaxis_title='Reconstruction Error',
                height=400
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Transaction amount analysis
        st.header("💰 Transaction Amount Analysis")
        
        if 'transaction_amount' in df_filtered.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Scatter plot: Amount vs Error
                fig_scatter = px.scatter(
                    df_filtered,
                    x='transaction_amount',
                    y='reconstruction_error',
                    color='is_fraud',
                    color_discrete_map={True: 'red', False: 'green'},
                    labels={'is_fraud': 'Fraud Status'},
                    title='Transaction Amount vs Reconstruction Error',
                    height=400
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            with col2:
                # Amount distribution by fraud status
                fig_amount = go.Figure()
                
                fig_amount.add_trace(go.Histogram(
                    x=df_filtered[df_filtered['is_fraud']]['transaction_amount'],
                    name='Fraud',
                    marker_color='red',
                    opacity=0.7,
                    nbinsx=30
                ))
                
                fig_amount.add_trace(go.Histogram(
                    x=df_filtered[~df_filtered['is_fraud']]['transaction_amount'],
                    name='Normal',
                    marker_color='green',
                    opacity=0.7,
                    nbinsx=30
                ))
                
                fig_amount.update_layout(
                    title='Amount Distribution: Normal vs Fraud',
                    xaxis_title='Transaction Amount',
                    yaxis_title='Frequency',
                    barmode='overlay',
                    height=400
                )
                st.plotly_chart(fig_amount, use_container_width=True)
        
        # Hourly patterns
        st.header("⏰ Temporal Patterns")
        
        df_filtered['hour'] = df_filtered['timestamp'].dt.hour
        df_filtered['day_of_week'] = df_filtered['timestamp'].dt.day_name()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Fraud by hour
            hourly_fraud = df_filtered.groupby('hour')['is_fraud'].agg(['sum', 'count'])
            hourly_fraud['rate'] = hourly_fraud['sum'] / hourly_fraud['count'] * 100
            
            fig_hour = go.Figure()
            fig_hour.add_trace(go.Bar(
                x=hourly_fraud.index,
                y=hourly_fraud['rate'],
                marker_color='orange',
                text=hourly_fraud['rate'].round(1),
                textposition='outside'
            ))
            
            fig_hour.update_layout(
                title='Fraud Rate by Hour of Day',
                xaxis_title='Hour',
                yaxis_title='Fraud Rate (%)',
                height=400
            )
            st.plotly_chart(fig_hour, use_container_width=True)
        
        with col2:
            # Fraud by day of week
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_fraud = df_filtered.groupby('day_of_week')['is_fraud'].agg(['sum', 'count'])
            daily_fraud['rate'] = daily_fraud['sum'] / daily_fraud['count'] * 100
            daily_fraud = daily_fraud.reindex([d for d in day_order if d in daily_fraud.index])
            
            fig_day = go.Figure()
            fig_day.add_trace(go.Bar(
                x=daily_fraud.index,
                y=daily_fraud['rate'],
                marker_color='purple',
                text=daily_fraud['rate'].round(1),
                textposition='outside'
            ))
            
            fig_day.update_layout(
                title='Fraud Rate by Day of Week',
                xaxis_title='Day',
                yaxis_title='Fraud Rate (%)',
                height=400
            )
            st.plotly_chart(fig_day, use_container_width=True)
        
        # Statistical summary
        st.header("📈 Statistical Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Reconstruction Error")
            st.write(df_filtered['reconstruction_error'].describe())
        
        with col2:
            st.subheader("Response Time (ms)")
            st.write(df_filtered['response_time_ms'].describe())
        
        with col3:
            if 'transaction_amount' in df_filtered.columns:
                st.subheader("Transaction Amount")
                st.write(df_filtered['transaction_amount'].describe())
    
    else:
        st.info("No data available for analysis")

# ==================== PAGE 3: MODEL PERFORMANCE ====================
elif page == "🎯 Model Performance":
    st.title("🎯 Model Performance Dashboard")
    
    if len(df_filtered) > 0:
        # Confusion Matrix (if we have ground truth)
        st.header("📊 Model Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Predictions", f"{len(df_filtered):,}")
        
        with col2:
            fraud_rate = df_filtered['is_fraud'].mean() * 100
            st.metric("Fraud Detection Rate", f"{fraud_rate:.2f}%")
        
        with col3:
            avg_confidence = df_filtered.get('confidence', pd.Series([0])).mean() * 100
            st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
        
        with col4:
            if 'threshold' in df_filtered.columns:
                threshold = df_filtered['threshold'].iloc[0]
                st.metric("Decision Threshold", f"{threshold:.4f}")
        
        # ROC-like curve (error distribution)
        st.header("🎯 Decision Boundary Analysis")
        
        # Calculate various threshold statistics
        thresholds = np.linspace(
            df_filtered['reconstruction_error'].min(),
            df_filtered['reconstruction_error'].max(),
            100
        )
        
        detection_rates = []
        for thresh in thresholds:
            detection_rate = (df_filtered['reconstruction_error'] > thresh).mean()
            detection_rates.append(detection_rate)
        
        fig_thresh = go.Figure()
        fig_thresh.add_trace(go.Scatter(
            x=thresholds,
            y=detection_rates,
            mode='lines',
            name='Detection Rate',
            line=dict(color='blue', width=2)
        ))
        
        # Add current threshold
        if 'threshold' in df_filtered.columns:
            current_thresh = df_filtered['threshold'].iloc[0]
            current_rate = (df_filtered['reconstruction_error'] > current_thresh).mean()
            fig_thresh.add_trace(go.Scatter(
                x=[current_thresh],
                y=[current_rate],
                mode='markers',
                name='Current Threshold',
                marker=dict(size=15, color='red', symbol='star')
            ))
        
        fig_thresh.update_layout(
            title='Detection Rate vs Threshold',
            xaxis_title='Threshold',
            yaxis_title='Detection Rate',
            height=400
        )
        st.plotly_chart(fig_thresh, use_container_width=True)
        
        # Response time analysis
        st.header("⚡ Performance Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Response time over time
            ts_response = df_filtered.set_index('timestamp').resample('1H')['response_time_ms'].mean().reset_index()
            
            fig_response = go.Figure()
            fig_response.add_trace(go.Scatter(
                x=ts_response['timestamp'],
                y=ts_response['response_time_ms'],
                mode='lines+markers',
                name='Avg Response Time',
                line=dict(color='green', width=2)
            ))
            
            fig_response.update_layout(
                title='Response Time Over Time',
                xaxis_title='Time',
                yaxis_title='Response Time (ms)',
                height=400
            )
            st.plotly_chart(fig_response, use_container_width=True)
        
        with col2:
            # Response time distribution
            fig_resp_dist = go.Figure()
            fig_resp_dist.add_trace(go.Histogram(
                x=df_filtered['response_time_ms'],
                nbinsx=30,
                marker_color='teal'
            ))
            
            fig_resp_dist.update_layout(
                title='Response Time Distribution',
                xaxis_title='Response Time (ms)',
                yaxis_title='Frequency',
                height=400
            )
            st.plotly_chart(fig_resp_dist, use_container_width=True)
        
        # Throughput analysis
        st.header("📊 Throughput Analysis")
        
        # Predictions per hour
        throughput = df_filtered.set_index('timestamp').resample('1H').size().reset_index(name='count')
        
        fig_throughput = go.Figure()
        fig_throughput.add_trace(go.Bar(
            x=throughput['timestamp'],
            y=throughput['count'],
            marker_color='indigo'
        ))
        
        fig_throughput.update_layout(
            title='Predictions per Hour',
            xaxis_title='Time',
            yaxis_title='Number of Predictions',
            height=400
        )
        st.plotly_chart(fig_throughput, use_container_width=True)
        
    else:
        st.info("No data available for performance analysis")

# ==================== PAGE 4: REAL-TIME MONITOR ====================
elif page == "⚡ Real-Time Monitor":
    st.title("⚡ Real-Time Monitoring Dashboard")
    
    # Auto-refresh
    st.sidebar.info("This page auto-refreshes every 5 seconds")
    
    if len(df) > 0:
        # Last 10 minutes data
        last_10min = df[df['timestamp'] >= (datetime.now() - timedelta(minutes=10))]
        
        st.header("📊 Last 10 Minutes Activity")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Predictions", len(last_10min))
        
        with col2:
            frauds_10min = last_10min['is_fraud'].sum()
            st.metric("Frauds Detected", frauds_10min, 
                     delta=f"{frauds_10min/max(len(last_10min), 1)*100:.1f}%")
        
        with col3:
            if len(last_10min) > 0:
                avg_error = last_10min['reconstruction_error'].mean()
                st.metric("Avg Error", f"{avg_error:.4f}")
            else:
                st.metric("Avg Error", "N/A")
        
        with col4:
            if len(last_10min) > 0:
                avg_resp = last_10min['response_time_ms'].mean()
                st.metric("Avg Response", f"{avg_resp:.2f} ms")
            else:
                st.metric("Avg Response", "N/A")
        
        # Real-time stream
        st.header("🔴 Live Prediction Stream")
        
        if len(last_10min) > 0:
            # Last 20 predictions
            stream_df = last_10min.sort_values('timestamp', ascending=False).head(20)
            
            for _, row in stream_df.iterrows():
                cols = st.columns([2, 1, 1, 1, 1])
                
                with cols[0]:
                    st.write(f"🕐 {row['timestamp'].strftime('%H:%M:%S')}")
                
                with cols[1]:
                    if row['is_fraud']:
                        st.error("🚨 FRAUD")
                    else:
                        st.success("✅ Normal")
                
                with cols[2]:
                    st.write(f"Error: {row['reconstruction_error']:.4f}")
                
                with cols[3]:
                    st.write(f"{row.get('transaction_type', 'N/A')}")
                
                with cols[4]:
                    amount = row.get('transaction_amount', 0)
                    st.write(f"${amount:,.2f}")
                
                st.divider()
        else:
            st.info("No recent activity in the last 10 minutes")
        
        # Mini charts
        st.header("📈 Minute-by-Minute Trends")
        
        if len(last_10min) > 0:
            # Resample by minute
            minute_data = last_10min.set_index('timestamp').resample('1min').agg({
                'is_fraud': 'sum',
                'reconstruction_error': 'mean',
                'response_time_ms': 'mean'
            }).reset_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_mini1 = go.Figure()
                fig_mini1.add_trace(go.Scatter(
                    x=minute_data['timestamp'],
                    y=minute_data['is_fraud'],
                    mode='lines+markers',
                    fill='tozeroy',
                    line=dict(color='red', width=2)
                ))
                fig_mini1.update_layout(
                    title='Frauds per Minute',
                    height=300,
                    showlegend=False
                )
                st.plotly_chart(fig_mini1, use_container_width=True)
            
            with col2:
                fig_mini2 = go.Figure()
                fig_mini2.add_trace(go.Scatter(
                    x=minute_data['timestamp'],
                    y=minute_data['reconstruction_error'],
                    mode='lines+markers',
                    fill='tozeroy',
                    line=dict(color='blue', width=2)
                ))
                fig_mini2.update_layout(
                    title='Avg Error per Minute',
                    height=300,
                    showlegend=False
                )
                st.plotly_chart(fig_mini2, use_container_width=True)
    
    else:
        st.info("Waiting for predictions...")
    
    # Add JavaScript for auto-refresh
    st.markdown(
        """
        <script>
        setTimeout(function(){
            window.location.reload();
        }, 5000);
        </script>
        """,
        unsafe_allow_html=True
    )

# ==================== PAGE 5: BUSINESS INSIGHTS ====================
elif page == "📈 Business Insights":
    st.title("📈 Business Insights Dashboard")
    
    if len(df_filtered) > 0 and 'transaction_amount' in df_filtered.columns:
        # Financial impact
        st.header("💰 Financial Impact Analysis")
        
        total_volume = df_filtered['transaction_amount'].sum()
        fraud_volume = df_filtered[df_filtered['is_fraud']]['transaction_amount'].sum()
        normal_volume = df_filtered[~df_filtered['is_fraud']]['transaction_amount'].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Volume", f"${total_volume:,.2f}")
        
        with col2:
            st.metric("Fraud Volume", f"${fraud_volume:,.2f}",
                     delta=f"{fraud_volume/total_volume*100:.2f}%")
        
        with col3:
            st.metric("Normal Volume", f"${normal_volume:,.2f}")
        
        with col4:
            avg_fraud_amount = df_filtered[df_filtered['is_fraud']]['transaction_amount'].mean() if fraud_volume > 0 else 0
            st.metric("Avg Fraud Amount", f"${avg_fraud_amount:,.2f}")
        
        # Volume over time
        st.header("📊 Transaction Volume Trends")
        
        vol_data = df_filtered.set_index('timestamp').resample('1H').agg({
            'transaction_amount': 'sum',
            'is_fraud': 'sum'
        }).reset_index()
        
        vol_data['fraud_amount'] = df_filtered[df_filtered['is_fraud']].set_index('timestamp').resample('1H')['transaction_amount'].sum().values
        vol_data['fraud_amount'] = vol_data['fraud_amount'].fillna(0)
        
        fig_volume = go.Figure()
        
        fig_volume.add_trace(go.Bar(
            x=vol_data['timestamp'],
            y=vol_data['transaction_amount'],
            name='Total Volume',
            marker_color='lightblue'
        ))
        
        fig_volume.add_trace(go.Bar(
            x=vol_data['timestamp'],
            y=vol_data['fraud_amount'],
            name='Fraud Volume',
            marker_color='red'
        ))
        
        fig_volume.update_layout(
            title='Transaction Volume Over Time',
            xaxis_title='Time',
            yaxis_title='Transaction Amount ($)',
            barmode='overlay',
            height=400
        )
        st.plotly_chart(fig_volume, use_container_width=True)
        
        # Transaction type analysis
        if 'transaction_type' in df_filtered.columns:
            st.header("💳 Transaction Type Analysis")
            
            type_analysis = df_filtered.groupby('transaction_type').agg({
                'transaction_amount': ['sum', 'mean', 'count'],
                'is_fraud': 'sum'
            }).round(2)
            
            type_analysis.columns = ['Total Volume', 'Avg Amount', 'Count', 'Fraud Count']
            type_analysis['Fraud Rate %'] = (type_analysis['Fraud Count'] / type_analysis['Count'] * 100).round(2)
            
            st.dataframe(type_analysis, use_container_width=True)
            
            # Visualization
            col1, col2 = st.columns(2)
            
            with col1:
                fig_type_vol = px.bar(
                    type_analysis.reset_index(),
                    x='transaction_type',
                    y='Total Volume',
                    title='Total Volume by Transaction Type',
                    color='Total Volume',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_type_vol, use_container_width=True)
            
            with col2:
                fig_type_fraud = px.bar(
                    type_analysis.reset_index(),
                    x='transaction_type',
                    y='Fraud Rate %',
                    title='Fraud Rate by Transaction Type',
                    color='Fraud Rate %',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_type_fraud, use_container_width=True)
        
        # Risk scoring
        st.header("⚠️ Risk Assessment")
        
        # Categorize transactions by amount
        df_filtered['amount_category'] = pd.cut(
            df_filtered['transaction_amount'],
            bins=[0, 1000, 10000, 100000, float('inf')],
            labels=['Small (<$1K)', 'Medium ($1K-$10K)', 'Large ($10K-$100K)', 'Very Large (>$100K)']
        )
        
        risk_by_amount = df_filtered.groupby('amount_category').agg({
            'is_fraud': ['sum', 'count']
        })
        risk_by_amount.columns = ['Fraud Count', 'Total Count']
        risk_by_amount['Fraud Rate %'] = (risk_by_amount['Fraud Count'] / risk_by_amount['Total Count'] * 100).round(2)
        
        fig_risk = go.Figure()
        
        fig_risk.add_trace(go.Bar(
            x=risk_by_amount.index.astype(str),
            y=risk_by_amount['Fraud Rate %'],
            marker_color=['green', 'yellow', 'orange', 'red'],
            text=risk_by_amount['Fraud Rate %'].round(1),
            textposition='outside'
        ))
        
        fig_risk.update_layout(
            title='Fraud Rate by Transaction Size',
            xaxis_title='Transaction Size',
            yaxis_title='Fraud Rate (%)',
            height=400
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Savings estimation
        st.header("💡 Estimated Savings")
        
        st.info(f"""
        **Fraud Detection Summary:**
        - Total fraudulent transactions detected: {int(stats['fraud_detected'])}
        - Total fraud volume blocked: ${fraud_volume:,.2f}
        - Average fraud amount: ${avg_fraud_amount:,.2f}
        - Fraud detection rate: {stats['fraud_rate']*100:.2f}%
        
        *Note: These estimates are based on predictions. Actual savings may vary.*
        """)
    
    else:
        st.info("No transaction data available for business insights")

# ==================== FOOTER (ALL PAGES) ====================
st.markdown("---")

# Drift detection section (shown on all pages except Real-Time)
if page != "⚡ Real-Time Monitor":
    with st.expander("⚠️ Data Drift Detection", expanded=False):
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

# System info footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 System Info")
st.sidebar.info(f"""
**Dashboard Version:** 2.0  
**Last Update:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Records:** {len(df):,}  
**Filtered Records:** {len(df_filtered):,}
""")
