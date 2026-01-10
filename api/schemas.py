"""
Request and Response schemas for the API
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TransactionRequest(BaseModel):
    """Request schema for fraud prediction"""
    step: int = Field(..., description="Time step (hour)")
    amount: float = Field(..., ge=0, description="Transaction amount")
    oldbalanceOrg: float = Field(..., ge=0, description="Origin account balance before")
    newbalanceOrig: float = Field(..., ge=0, description="Origin account balance after")
    oldbalanceDest: float = Field(..., ge=0, description="Destination account balance before")
    newbalanceDest: float = Field(..., ge=0, description="Destination account balance after")
    type: str = Field(..., description="Transaction type: PAYMENT, TRANSFER, CASH_OUT, DEBIT, CASH_IN")
    nameOrig: str = Field(..., description="Origin account ID")
    nameDest: str = Field(..., description="Destination account ID")

    class Config:
        json_schema_extra = {
            "example": {
                "step": 1,
                "amount": 9839.64,
                "oldbalanceOrg": 170136.0,
                "newbalanceOrig": 160296.36,
                "oldbalanceDest": 0.0,
                "newbalanceDest": 0.0,
                "type": "PAYMENT",
                "nameOrig": "C1231006815",
                "nameDest": "M1979787155"
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for fraud prediction"""
    is_fraud: bool = Field(..., description="Whether transaction is predicted as fraud")
    fraud_probability: float = Field(..., ge=0, le=1, description="Fraud probability (0-1)")
    reconstruction_error: float = Field(..., description="Model reconstruction error")
    threshold: float = Field(..., description="Detection threshold used")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")
    model_version: str = Field(..., description="Model version used")
    timestamp: datetime = Field(default_factory=datetime.now, description="Prediction timestamp")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_version: str
    timestamp: datetime = Field(default_factory=datetime.now)


class MetricsResponse(BaseModel):
    """Metrics response"""
    total_predictions: int
    fraud_detected: int
    fraud_rate: float
    avg_response_time_ms: float
    uptime_seconds: float
    timestamp: datetime = Field(default_factory=datetime.now)
