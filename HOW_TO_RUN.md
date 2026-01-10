# HOW TO RUN THE FRAUD DETECTION MLOPS PROJECT

## 🚀 QUICK START

### **Option 1: One Command Start**
```powershell
.\start.ps1
```

This will:
- ✅ Check Docker is running
- ✅ Start API container (port 8000)
- ✅ Start Dashboard container (port 8501)
- ✅ Run health checks
- ✅ Show you all URLs

---

## 📋 STEP-BY-STEP GUIDE

### **Step 1: Ensure Docker is Running**
Open Docker Desktop and make sure it's running.

### **Step 2: Start the System**
```powershell
# Start both API and Dashboard
docker-compose up -d

# OR start individually
docker-compose up -d api        # Just API
docker-compose up -d dashboard  # Just Dashboard
```

### **Step 3: Verify Services**
```powershell
# Check running containers
docker ps

# Check API health
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

### **Step 4: Access the System**

**🌐 Open in Browser:**
- **Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Metrics**: http://localhost:8000/metrics

---

## 🧪 TESTING THE SYSTEM

### **Test 1: Real User History (Best Results)**
```powershell
.\test_real_history.ps1
```
Uses pre-computed features from test data. Model accuracy is high!

### **Test 2: Send Multiple Transactions**
```powershell
.\send_test_transactions.ps1
```
Sends 10 test transactions and shows results.

### **Test 3: Manual Testing via Swagger**
1. Go to http://localhost:8000/docs
2. Find **POST /predict_test_sample**
3. Click "Try it out"
4. Enter sample index (0-9997)
5. Click "Execute"
6. See prediction result!

### **Test 4: System Status Check**
```powershell
.\test_system.ps1
```
Checks health, sends test predictions, validates metrics.

---

## 📊 USING THE DASHBOARD

1. Open http://localhost:8501
2. Click **"🔄 Refresh Data"** to update metrics
3. View:
   - Total predictions
   - Fraud detection rate
   - Response times
   - Charts and timelines
   - Recent predictions table

---

## 🔍 MONITORING & LOGS

### **View API Logs**
```powershell
docker logs fraud-detection-api

# Follow logs in real-time
docker logs -f fraud-detection-api

# Last 50 lines
docker logs fraud-detection-api --tail 50
```

### **View Dashboard Logs**
```powershell
docker logs fraud-detection-dashboard
```

### **Check Metrics File**
```powershell
Get-Content logs/metrics.jsonl | Select-Object -Last 10
```

---

## 🛑 STOPPING THE SYSTEM

### **Stop Everything**
```powershell
docker-compose down
```

### **Stop Individual Services**
```powershell
docker stop fraud-detection-api
docker stop fraud-detection-dashboard
```

### **Restart Services**
```powershell
docker restart fraud-detection-api
docker restart fraud-detection-dashboard
```

---

## 🔧 TROUBLESHOOTING

### **Problem: Docker not running**
```powershell
# Start Docker Desktop manually
# Then run: .\start.ps1
```

### **Problem: Port already in use**
```powershell
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# Stop the process or change ports in docker-compose.yml
```

### **Problem: Dashboard shows no data**
```powershell
# Send some test predictions first
.\test_real_history.ps1

# Then refresh dashboard (click refresh button)
```

### **Problem: API returns 500 errors**
```powershell
# Check API logs
docker logs fraud-detection-api --tail 50

# Restart API
docker restart fraud-detection-api
```

### **Problem: Need to rebuild**
```powershell
# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📁 PROJECT STRUCTURE

```
aiops-log-anomalies/
├── api/                      # FastAPI application
│   ├── main.py              # API endpoints
│   ├── model_handler.py     # Model loading & prediction
│   └── schemas.py           # Request/response models
├── monitoring/              # Monitoring tools
│   ├── dashboard.py         # Streamlit dashboard
│   ├── metrics_tracker.py   # Metrics logging
│   └── drift_detection.py   # Data drift detection
├── models/                  # Trained ML models
│   ├── autoencoder.keras    # Main model
│   ├── autoencoder_scaler.pkl
│   └── ae_threshold.npy
├── logs/                    # System logs
│   ├── metrics.jsonl        # Prediction logs
│   └── api.log             # API logs
├── docker-compose.yml       # Multi-service orchestration
├── Dockerfile              # Container definition
├── start.ps1               # Startup script
└── test_*.ps1              # Test scripts
```

---

## 🎯 TYPICAL WORKFLOW

1. **Start System**: `.\start.ps1`
2. **Send Predictions**: Go to http://localhost:8000/docs
3. **Monitor Dashboard**: Open http://localhost:8501
4. **Run Tests**: `.\test_real_history.ps1`
5. **Check Metrics**: http://localhost:8000/metrics
6. **View Logs**: `docker logs fraud-detection-api`
7. **Stop System**: `docker-compose down`

---

## 📚 ADDITIONAL COMMANDS

```powershell
# Check API health
curl http://localhost:8000/health

# Get current metrics
curl http://localhost:8000/metrics

# Test single prediction (with real features)
curl -X POST "http://localhost:8000/predict_test_sample?sample_index=0"

# View all containers
docker ps -a

# Remove all stopped containers
docker-compose down --volumes
```

---

## ✅ SYSTEM IS READY WHEN YOU SEE:

```
Container: fraud-detection-api       Status: Up (healthy)
Container: fraud-detection-dashboard Status: Up

Access:
  Dashboard: http://localhost:8501
  API Docs:  http://localhost:8000/docs
```

**Now start making predictions! 🚀**
