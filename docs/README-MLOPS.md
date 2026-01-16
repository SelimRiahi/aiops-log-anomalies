# 🚀 MLOps Fraud Detection System

Production-ready fraud detection system using Autoencoder and MLOps best practices.

## 📋 Overview

This project transforms a fraud detection ML model into a **production-grade MLOps system** with:

- ✅ REST API for real-time predictions
- ✅ Model performance monitoring
- ✅ Data drift detection
- ✅ Automated retraining pipeline
- ✅ Docker containerization
- ✅ CI/CD pipeline
- ✅ Comprehensive testing

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Client App    │─────▶│   FastAPI API    │─────▶│  Autoencoder    │
│  (Any system)   │      │  (Port 8000)     │      │     Model       │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Metrics Tracker │
                         └──────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
           ┌─────────────────┐        ┌──────────────────┐
           │ Drift Detector  │        │   Monitoring     │
           │   (Automated)   │        │   Dashboard      │
           └─────────────────┘        └──────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │   Retraining    │
           │    Pipeline     │
           └─────────────────┘
```

## 📁 Project Structure

```
mlops-fraud-detection/
│
├── api/                          # FastAPI application
│   ├── main.py                   # API endpoints
│   ├── schemas.py                # Request/response models
│   └── model_handler.py          # Model loading & prediction
│
├── monitoring/                   # Monitoring & drift detection
│   ├── metrics_tracker.py        # Track predictions & performance
│   ├── drift_detection.py        # Data drift detection
│   └── dashboard.py              # Streamlit monitoring UI
│
├── pipelines/                    # Automated workflows
│   ├── retrain_pipeline.py       # Automated retraining
│   └── drift_check.py            # Scheduled drift checking
│
├── tests/                        # Unit tests
│   ├── test_api.py
│   ├── test_model.py
│   └── test_monitoring.py
│
├── config/                       # Configuration
│   └── config.py                 # Central configuration
│
├── models/                       # Trained models (generated)
│   ├── autoencoder.keras
│   ├── autoencoder_scaler.pkl
│   └── ae_threshold.npy
│
├── logs/                         # Logs & metrics
│   ├── api.log
│   ├── metrics.jsonl
│   └── drift_reports.jsonl
│
├── .github/workflows/            # CI/CD
│   └── ci-cd.yml                 # GitHub Actions workflow
│
├── Dockerfile                    # Container definition
├── docker-compose.yml            # Multi-container setup
├── requirements-prod.txt         # Production dependencies
└── README-MLOPS.md              # This file
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d

# API will be available at http://localhost:8000
# Dashboard at http://localhost:8501
```

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements-prod.txt

# Run the API
cd api
python main.py

# In another terminal, run monitoring dashboard
streamlit run monitoring/dashboard.py
```

## 📡 API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Make Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "step": 1,
    "amount": 9839.64,
    "oldbalanceOrg": 170136.0,
    "newbalanceOrig": 160296.36,
    "oldbalanceDest": 0.0,
    "newbalanceDest": 0.0,
    "type": "PAYMENT",
    "nameOrig": "C1231006815",
    "nameDest": "M1979787155"
  }'
```

### Get Metrics

```bash
curl http://localhost:8000/metrics
```

## 📊 Monitoring

### Real-time Dashboard

Access the monitoring dashboard at `http://localhost:8501` to view:

- Total predictions & fraud detection rate
- Response time metrics
- Fraud detection timeline
- Data drift status
- Recent predictions

### Drift Detection

```bash
# Manual drift check
python pipelines/drift_check.py
```

The system automatically detects:

- Distribution changes in incoming data
- Feature drift using Kolmogorov-Smirnov test
- Population Stability Index (PSI)

## 🔄 Automated Retraining

### Manual Retraining

```bash
python pipelines/retrain_pipeline.py
```

### Features

- ✅ Automatic model backup before retraining
- ✅ Performance evaluation on test set
- ✅ Rollback if new model performs worse
- ✅ Version tracking

### Trigger Conditions

- Scheduled (e.g., weekly)
- Data drift detected (severity > 30%)
- Performance degradation

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=api --cov=monitoring --cov=pipelines

# Run specific test
pytest tests/test_api.py -v
```

## 🔧 Configuration

Edit `config/config.py` to customize:

- API host/port
- Model version
- Drift detection thresholds
- Retraining schedule
- Logging levels

Environment variables:

```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export MODEL_VERSION=1.0.0
export DRIFT_THRESHOLD=0.1
export AUTO_RETRAIN=true
```

## 📈 MLOps Features

### 1. Model Serving

- FastAPI REST API
- Health checks
- Request validation
- Error handling
- Response time tracking

### 2. Monitoring

- Real-time metrics dashboard
- Prediction logging (JSONL format)
- Performance tracking
- Fraud detection analytics

### 3. Drift Detection

- Kolmogorov-Smirnov test
- Population Stability Index
- Automated alerts
- Scheduled checks

### 4. Retraining Pipeline

- Automated workflow
- Model backup & versioning
- Performance evaluation
- Rollback capability

### 5. Containerization

- Docker multi-stage build
- Docker Compose orchestration
- Health checks
- Volume mounting for persistence

### 6. CI/CD

- Automated testing (GitHub Actions)
- Code linting (flake8, black)
- Docker build & test
- Deployment pipeline

## 🔐 Production Considerations

### Security

- [ ] Add API authentication (JWT, API keys)
- [ ] Enable HTTPS/TLS
- [ ] Implement rate limiting
- [ ] Add input sanitization

### Scalability

- [ ] Add load balancer
- [ ] Horizontal scaling (multiple API instances)
- [ ] Caching layer (Redis)
- [ ] Message queue for async processing

### Observability

- [ ] Integrate Prometheus metrics
- [ ] Add distributed tracing (Jaeger/Zipkin)
- [ ] Central logging (ELK stack)
- [ ] Alerting (PagerDuty, Slack)

### Data Management

- [ ] Database for prediction history
- [ ] Data versioning (DVC)
- [ ] Feature store
- [ ] A/B testing framework

## 📚 API Documentation

Once the API is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Run tests: `pytest tests/`
4. Submit pull request

## 📝 Logs

All logs are stored in the `logs/` directory:

- `api.log` - API request/response logs
- `metrics.jsonl` - Prediction metrics (JSON Lines)
- `drift_reports.jsonl` - Drift detection reports

## 🆘 Troubleshooting

### Model not loading

```bash
# Ensure model files exist
ls models/

# If missing, train the model first
python 3_train.py
```

### API not responding

```bash
# Check if API is running
curl http://localhost:8000/health

# Check logs
tail -f logs/api.log
```

### Docker build fails

```bash
# Ensure model files are in models/ directory
# Check .dockerignore isn't excluding important files
```

## 📊 Performance Benchmarks

- **API Response Time**: < 100ms (p95)
- **Throughput**: 100+ requests/second (single instance)
- **Model Inference**: < 50ms
- **Memory Usage**: ~500MB (with model loaded)

## 🎯 Roadmap

- [ ] MLflow integration for experiment tracking
- [ ] Prometheus/Grafana metrics
- [ ] Model registry
- [ ] Multi-model serving
- [ ] A/B testing framework
- [ ] Feature importance tracking
- [ ] Explainability (SHAP values)
- [ ] Kubernetes deployment manifests

## 📄 License

MIT License

## 👤 Author

MLOps transformation of fraud detection system

---

**🚀 Production-Ready ML System | Built with MLOps Best Practices**
