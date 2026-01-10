# Test Real User History Predictions
Write-Host "Testing with REAL user history features!" -ForegroundColor Cyan
Write-Host ""

Write-Host "Sending 5 test samples with real features..." -ForegroundColor Yellow
Write-Host ""

$samples = 0, 13, 25, 50, 100  # Different samples from test data

foreach ($index in $samples) {
    Write-Host "[$($index)] Sample $index..." -NoNewline
    
    try {
        $result = Invoke-RestMethod -Uri "http://localhost:8000/predict_test_sample?sample_index=$index" -Method Post
        
        $status = if ($result.is_fraud) { "FRAUD" } else { "NORMAL" }
        $color = if ($result.is_fraud) { "Red" } else { "Green" }
        
        Write-Host " $status" -ForegroundColor $color
        Write-Host "    Reconstruction Error: $([math]::Round($result.reconstruction_error, 4))" -ForegroundColor Gray
        Write-Host "    Threshold: $([math]::Round($result.threshold, 4))" -ForegroundColor Gray
        Write-Host "    Confidence: $([math]::Round($result.confidence * 100, 1))%" -ForegroundColor Gray
        Write-Host ""
    } catch {
        Write-Host " FAILED: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    Start-Sleep -Milliseconds 300
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CHECK THE ACTUAL LABELS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run this to see actual fraud labels:" -ForegroundColor Yellow
Write-Host 'python -c "import pandas as pd; df = pd.read_csv(''paysim_test.csv''); print(df.iloc[[0,13,25,50,100]][[''amount'', ''type_TRANSFER'', ''type_CASH_OUT'', ''reconstruction_error'' if ''reconstruction_error'' in df.columns else ''amount'', ''isFraud'']])"' -ForegroundColor Gray
Write-Host ""
Write-Host "Now go to:" -ForegroundColor Green
Write-Host "  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  Try POST /predict_test_sample with different indexes (0-9997)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dashboard: http://localhost:8501" -ForegroundColor Yellow
