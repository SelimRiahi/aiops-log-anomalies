# Test API - PowerShell Script
# Simple way to test your fraud detection API

$url = "http://localhost:8000/predict"

$body = @{
    step = 1
    amount = 9839.64
    oldbalanceOrg = 170136.0
    newbalanceOrig = 160296.36
    oldbalanceDest = 0.0
    newbalanceDest = 0.0
    type = "PAYMENT"
    nameOrig = "C1231006815"
    nameDest = "M1979787155"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FRAUD DETECTION RESULT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Is Fraud: " -NoNewline
if ($response.is_fraud) {
    Write-Host "YES (BLOCKED)" -ForegroundColor Red
} else {
    Write-Host "NO (APPROVED)" -ForegroundColor Green
}
Write-Host "Fraud Probability: $($response.fraud_probability * 100)%"
Write-Host "Confidence: $($response.confidence * 100)%"
Write-Host "Reconstruction Error: $($response.reconstruction_error)"
Write-Host "Threshold: $($response.threshold)"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
