# Start Monitoring Dashboard
# Run this to view the monitoring dashboard

Write-Host "Starting Monitoring Dashboard..." -ForegroundColor Cyan
Write-Host "Dashboard will open at: http://localhost:8501" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

streamlit run monitoring/dashboard.py
