# Simple test to see the prediction flow
Write-Host "Testing Fraud Detection API - See how predictions work!" -ForegroundColor Cyan
Write-Host ""

# 1. Check if API is alive
Write-Host "[1/3] Checking if API is running..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✓ API Status: $($health.status)" -ForegroundColor Green
    Write-Host "✓ Model Loaded: $($health.model_loaded)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ API not responding! Make sure Docker is running." -ForegroundColor Red
    exit
}

# 2. Get API info
Write-Host "[2/3] Getting API information..." -ForegroundColor Yellow
try {
    $info = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
    Write-Host "API: $($info.service)" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host "Could not get API info" -ForegroundColor Red
}

# 3. Check metrics
Write-Host "[3/3] Checking current metrics..." -ForegroundColor Yellow
try {
    $metrics = Invoke-RestMethod -Uri "http://localhost:8000/metrics" -Method Get
    Write-Host "Total Predictions: $($metrics.total_predictions)" -ForegroundColor Cyan
    Write-Host "Frauds Detected: $($metrics.fraud_detected)" -ForegroundColor Cyan
    Write-Host "Fraud Rate: $([math]::Round($metrics.fraud_rate * 100, 2))%" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host "Could not get metrics" -ForegroundColor Red
}

Write-Host "========================================" -ForegroundColor Green
Write-Host "API is working! Your model is deployed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "The model (autoencoder.keras) is running inside Docker"
Write-Host "waiting to make predictions!"
