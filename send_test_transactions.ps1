# Send Multiple Test Transactions and Watch Dashboard
Write-Host "Sending 10 test transactions..." -ForegroundColor Cyan
Write-Host ""

$transactions = @(
    @{ step=10; amount=100; oldbalanceOrg=5000; newbalanceOrig=4900; oldbalanceDest=1000; newbalanceDest=1100; type="PAYMENT"; nameOrig="C1111111111"; nameDest="M2222222222" },
    @{ step=20; amount=50000; oldbalanceOrg=60000; newbalanceOrig=10000; oldbalanceDest=0; newbalanceDest=0; type="TRANSFER"; nameOrig="C3333333333"; nameDest="C4444444444" },
    @{ step=30; amount=250; oldbalanceOrg=10000; newbalanceOrig=9750; oldbalanceDest=500; newbalanceDest=750; type="PAYMENT"; nameOrig="C5555555555"; nameDest="M6666666666" },
    @{ step=40; amount=100000; oldbalanceOrg=100000; newbalanceOrig=0; oldbalanceDest=50000; newbalanceDest=150000; type="CASH_OUT"; nameOrig="C7777777777"; nameDest="C8888888888" },
    @{ step=50; amount=1500; oldbalanceOrg=20000; newbalanceOrig=18500; oldbalanceDest=3000; newbalanceDest=4500; type="PAYMENT"; nameOrig="C9999999999"; nameDest="M1010101010" },
    @{ step=60; amount=75000; oldbalanceOrg=80000; newbalanceOrig=5000; oldbalanceDest=0; newbalanceDest=0; type="TRANSFER"; nameOrig="C1212121212"; nameDest="C1313131313" },
    @{ step=70; amount=350; oldbalanceOrg=15000; newbalanceOrig=14650; oldbalanceDest=2000; newbalanceDest=2350; type="DEBIT"; nameOrig="C1414141414"; nameDest="M1515151515" },
    @{ step=80; amount=200000; oldbalanceOrg=200000; newbalanceOrig=0; oldbalanceDest=100000; newbalanceDest=300000; type="TRANSFER"; nameOrig="C1616161616"; nameDest="C1717171717" },
    @{ step=90; amount=800; oldbalanceOrg=25000; newbalanceOrig=24200; oldbalanceDest=5000; newbalanceDest=5800; type="CASH_IN"; nameOrig="C1818181818"; nameDest="M1919191919" },
    @{ step=100; amount=45000; oldbalanceOrg=50000; newbalanceOrig=5000; oldbalanceDest=10000; newbalanceDest=55000; type="CASH_OUT"; nameOrig="C2020202020"; nameDest="C2121212121" }
)

$results = @()

foreach ($i in 0..($transactions.Count - 1)) {
    $tx = $transactions[$i]
    $body = $tx | ConvertTo-Json
    
    Write-Host "[$($i+1)/10] Sending transaction: $($tx.type) - $($tx.amount)..." -NoNewline
    
    try {
        $result = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -ContentType "application/json" -Body $body
        
        if ($result.is_fraud) {
            Write-Host " FRAUD" -ForegroundColor Red
        } else {
            Write-Host " NORMAL" -ForegroundColor Green
        }
        
        $results += [PSCustomObject]@{
            Amount = $tx.amount
            Type = $tx.type
            IsFraud = $result.is_fraud
            ReconError = [math]::Round($result.reconstruction_error, 2)
            Probability = [math]::Round($result.fraud_probability * 100, 1)
        }
    } catch {
        Write-Host " FAILED" -ForegroundColor Yellow
    }
    
    Start-Sleep -Milliseconds 200
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RESULTS SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$results | Format-Table -AutoSize

Write-Host ""
Write-Host "Total Sent: $($transactions.Count)" -ForegroundColor Green
Write-Host "Frauds: $($results | Where-Object {$_.IsFraud} | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Red
Write-Host "Normal: $($results | Where-Object {-not $_.IsFraud} | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Green

Write-Host ""
Write-Host "NOW:" -ForegroundColor Yellow
Write-Host "1. Open Dashboard: http://localhost:8501" -ForegroundColor Cyan
Write-Host "2. Click 'Refresh Data' button" -ForegroundColor Cyan
Write-Host "3. See the charts update with new predictions!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check metrics endpoint: http://localhost:8000/metrics" -ForegroundColor Gray
