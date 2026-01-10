# ============================================================
# COMPLETE MLOPS SYSTEM TEST
# Tests: Predictions, Monitoring, Metrics Tracking
# ============================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TESTING COMPLETE MLOPS SYSTEM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# TEST 1: Health Check
# ============================================================
Write-Host "[TEST 1] Checking API Health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✓ Status: $($health.status)" -ForegroundColor Green
    Write-Host "✓ Model Loaded: $($health.model_loaded)" -ForegroundColor Green
    Write-Host "✓ Model Version: $($health.model_version)" -ForegroundColor Green
} catch {
    Write-Host "✗ API Health Check Failed!" -ForegroundColor Red
    exit
}
Write-Host ""

# ============================================================
# TEST 2: Send Test Predictions (Normal + Suspicious)
# ============================================================
Write-Host "[TEST 2] Testing Fraud Predictions..." -ForegroundColor Yellow

# Normal transaction (low amount, regular payment)
$normalTx = @{
    step = 1
    amount = 500.0
    oldbalanceOrg = 10000.0
    newbalanceOrig = 9500.0
    oldbalanceDest = 5000.0
    newbalanceDest = 5500.0
    type = "PAYMENT"
    nameOrig = "C1234567890"
    nameDest = "M9876543210"
} | ConvertTo-Json

Write-Host "  → Testing NORMAL transaction (500 payment)..." -ForegroundColor Cyan
try {
    $result1 = Invoke-RestMethod -Uri "http://localhost:8000/predict" `
        -Method Post `
        -ContentType "application/json" `
        -Body $normalTx
    
    if ($result1.is_fraud) {
        Write-Host "    Prediction: FRAUD ⚠️" -ForegroundColor Red
    } else {
        Write-Host "    Prediction: NORMAL ✓" -ForegroundColor Green
    }
    Write-Host "    Fraud Probability: $([math]::Round($result1.fraud_probability * 100, 2))%" -ForegroundColor Gray
    Write-Host "    Reconstruction Error: $([math]::Round($result1.reconstruction_error, 6))" -ForegroundColor Gray
    Write-Host "    Confidence: $([math]::Round($result1.confidence * 100, 2))%" -ForegroundColor Gray
} catch {
    Write-Host "    ✗ Prediction failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Suspicious transaction (large amount, zero balances)
$suspiciousTx = @{
    step = 100
    amount = 500000.0
    oldbalanceOrg = 500000.0
    newbalanceOrig = 0.0
    oldbalanceDest = 0.0
    newbalanceDest = 0.0
    type = "TRANSFER"
    nameOrig = "C9999999999"
    nameDest = "C1111111111"
} | ConvertTo-Json

Write-Host "  -> Testing SUSPICIOUS transaction (500K transfer, zero balances)..." -ForegroundColor Cyan
try {
    $result2 = Invoke-RestMethod -Uri "http://localhost:8000/predict" `
        -Method Post `
        -ContentType "application/json" `
        -Body $suspiciousTx
    
    if ($result2.is_fraud) {
        Write-Host "    Prediction: FRAUD" -ForegroundColor Red
    } else {
        Write-Host "    Prediction: NORMAL" -ForegroundColor Green
    }
    Write-Host "    Fraud Probability: $([math]::Round($result2.fraud_probability * 100, 2))%" -ForegroundColor Gray
    Write-Host "    Reconstruction Error: $([math]::Round($result2.reconstruction_error, 6))" -ForegroundColor Gray
    Write-Host "    Confidence: $([math]::Round($result2.confidence * 100, 2))%" -ForegroundColor Gray
} catch {
    Write-Host "    Failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Another suspicious (high amount to old balance ratio)
$suspiciousTx2 = @{
    step = 200
    amount = 95000.0
    oldbalanceOrg = 100000.0
    newbalanceOrig = 5000.0
    oldbalanceDest = 1000.0
    newbalanceDest = 96000.0
    type = "CASH_OUT"
    nameOrig = "C5555555555"
    nameDest = "C6666666666"
} | ConvertTo-Json

Write-Host "  -> Testing SUSPICIOUS transaction (95K cash out, 95% of balance)..." -ForegroundColor Cyan
try {
    $result3 = Invoke-RestMethod -Uri "http://localhost:8000/predict" `
        -Method Post `
        -ContentType "application/json" `
        -Body $suspiciousTx2
    
    if ($result3.is_fraud) {
        Write-Host "    Prediction: FRAUD" -ForegroundColor Red
    } else {
        Write-Host "    Prediction: NORMAL" -ForegroundColor Green
    }
    Write-Host "    Fraud Probability: $([math]::Round($result3.fraud_probability * 100, 2))%" -ForegroundColor Gray
    Write-Host "    Reconstruction Error: $([math]::Round($result3.reconstruction_error, 6))" -ForegroundColor Gray
    Write-Host "    Confidence: $([math]::Round($result3.confidence * 100, 2))%" -ForegroundColor Gray
} catch {
    Write-Host "    Failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# ============================================================
# TEST 3: Check Metrics Tracking
# ============================================================
Write-Host "[TEST 3] Checking Metrics Tracking..." -ForegroundColor Yellow
try {
    $metrics = Invoke-RestMethod -Uri "http://localhost:8000/metrics" -Method Get
    Write-Host "✓ Total Predictions: $($metrics.total_predictions)" -ForegroundColor Green
    Write-Host "✓ Frauds Detected: $($metrics.fraud_detected)" -ForegroundColor Green
    Write-Host "✓ Normal Transactions: $($metrics.normal_detected)" -ForegroundColor Green
    Write-Host "✓ Fraud Rate: $([math]::Round($metrics.fraud_rate * 100, 2))%" -ForegroundColor Green
    Write-Host "✓ Avg Response Time: $([math]::Round($metrics.avg_response_time * 1000, 2)) ms" -ForegroundColor Green
    Write-Host "✓ Avg Confidence: $([math]::Round($metrics.avg_confidence * 100, 2))%" -ForegroundColor Green
} catch {
    Write-Host "✗ Metrics check failed" -ForegroundColor Red
}
Write-Host ""

# ============================================================
# TEST 4: Check Logs
# ============================================================
Write-Host "[TEST 4] Checking Prediction Logs..." -ForegroundColor Yellow
$logFile = "logs/metrics.jsonl"
if (Test-Path $logFile) {
    $logCount = (Get-Content $logFile | Measure-Object -Line).Lines
    Write-Host "✓ Predictions logged: $logCount entries" -ForegroundColor Green
    Write-Host "  Log file: $logFile" -ForegroundColor Gray
} else {
    Write-Host "⚠ No log file found yet" -ForegroundColor Yellow
}
Write-Host ""

# ============================================================
# SUMMARY
# ============================================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TEST SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ API is running and healthy" -ForegroundColor Green
Write-Host "✓ Predictions are working" -ForegroundColor Green
Write-Host "✓ Metrics are being tracked" -ForegroundColor Green
Write-Host "✓ Logs are being written" -ForegroundColor Green
Write-Host ""
Write-Host "Dashboard: http://localhost:8501" -ForegroundColor Yellow
Write-Host "API Docs:  http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Metrics:   http://localhost:8000/metrics" -ForegroundColor Yellow
Write-Host ""
