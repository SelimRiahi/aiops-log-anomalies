# ============================================================
# FRAUD DETECTION MLOPS SYSTEM - STARTUP SCRIPT
# ============================================================
# This script starts the complete MLOps system
# ============================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FRAUD DETECTION MLOPS SYSTEM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "[1/4] Checking Docker..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "  ✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker is not running!" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Start containers
Write-Host "[2/4] Starting containers..." -ForegroundColor Yellow
Write-Host "  Starting API container..." -NoNewline
docker-compose up -d api 2>&1 | Out-Null
Write-Host " Done" -ForegroundColor Green

Write-Host "  Starting Dashboard container..." -NoNewline
docker-compose up -d dashboard 2>&1 | Out-Null
Write-Host " Done" -ForegroundColor Green
Write-Host ""

# Wait for services to be ready
Write-Host "[3/4] Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Health check
Write-Host "[4/4] Checking service health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -ErrorAction Stop
    if ($health.status -eq "healthy") {
        Write-Host "  OK API is healthy" -ForegroundColor Green
    } else {
        Write-Host "  WARNING API responded but not healthy" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  WARNING API not responding yet (may need more time)" -ForegroundColor Yellow
}
Write-Host ""

# Show running containers
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SYSTEM STATUS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
docker ps --filter "name=fraud-detection" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host ""

# Show URLs
Write-Host "========================================" -ForegroundColor Green
Write-Host "  🚀 SYSTEM READY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access the system:" -ForegroundColor White
Write-Host ""
Write-Host "  📊 Dashboard (Monitoring):" -ForegroundColor Cyan
Write-Host "     http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "  🔌 API Documentation (Swagger):" -ForegroundColor Cyan
Write-Host "     http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "  📈 Metrics Endpoint:" -ForegroundColor Cyan
Write-Host "     http://localhost:8000/metrics" -ForegroundColor White
Write-Host ""
Write-Host "  ✅ Health Check:" -ForegroundColor Cyan
Write-Host "     http://localhost:8000/health" -ForegroundColor White
Write-Host ""

# Show quick test commands
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  QUICK TESTS" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Test with real user history:" -ForegroundColor White
Write-Host "  .\test_real_history.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "Send multiple test transactions:" -ForegroundColor White
Write-Host "  .\send_test_transactions.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "Check system status:" -ForegroundColor White
Write-Host "  .\test_system.ps1" -ForegroundColor Gray
Write-Host ""

Write-Host "To stop the system:" -ForegroundColor Red
Write-Host "  docker-compose down" -ForegroundColor Gray
Write-Host ""
