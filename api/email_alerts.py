"""
Email Alert System for Fraud Detection
Sends real-time alerts when fraud is detected
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from typing import Dict

class EmailAlerter:
    """Send email alerts for fraud detection"""
    
    def __init__(self):
        # Email configuration from environment variables
        self.enabled = os.getenv('ALERT_ENABLED', 'false').lower() == 'true'
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', '')
        
        if self.enabled and not all([self.sender_email, self.sender_password, self.recipient_email]):
            print("⚠️  Email alerts enabled but credentials missing!")
            self.enabled = False
    
    def send_fraud_alert(self, transaction_data: Dict, prediction_details: Dict):
        """Send email alert for detected fraud"""
        
        if not self.enabled:
            print("📧 Email alerts disabled (set ALERT_ENABLED=true to enable)")
            return False
        
        try:
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚨 FRAUD ALERT - ${transaction_data['amount']:,.2f} Transaction"
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            
            # Email body (HTML)
            html_body = self._create_alert_email(transaction_data, prediction_details)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Fraud alert sent to {self.recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email alert: {str(e)}")
            return False
    
    def _create_alert_email(self, transaction_data: Dict, prediction_details: Dict) -> str:
        """Create HTML email body"""
        
        error = prediction_details['reconstruction_error']
        threshold = prediction_details['threshold']
        confidence = error - threshold
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
                .container {{ background-color: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }}
                .header {{ background-color: #dc3545; color: white; padding: 20px; border-radius: 5px; text-align: center; }}
                .alert-icon {{ font-size: 48px; }}
                .details {{ margin: 20px 0; }}
                .detail-row {{ padding: 10px; border-bottom: 1px solid #eee; }}
                .detail-label {{ font-weight: bold; color: #333; }}
                .detail-value {{ color: #666; float: right; }}
                .risk-high {{ color: #dc3545; font-weight: bold; }}
                .footer {{ margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="alert-icon">🚨</div>
                    <h1>FRAUD DETECTED</h1>
                    <p>High-risk transaction flagged by AI system</p>
                </div>
                
                <div class="details">
                    <h2>Transaction Details</h2>
                    
                    <div class="detail-row">
                        <span class="detail-label">Amount:</span>
                        <span class="detail-value risk-high">${transaction_data['amount']:,.2f}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Type:</span>
                        <span class="detail-value">{transaction_data['type']}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Time:</span>
                        <span class="detail-value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Origin Account:</span>
                        <span class="detail-value">{transaction_data.get('nameOrig', 'N/A')[:15]}...</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Destination Account:</span>
                        <span class="detail-value">{transaction_data.get('nameDest', 'N/A')[:15]}...</span>
                    </div>
                    
                    <h2>Risk Assessment</h2>
                    
                    <div class="detail-row">
                        <span class="detail-label">Reconstruction Error:</span>
                        <span class="detail-value risk-high">{error:.6f}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Threshold:</span>
                        <span class="detail-value">{threshold:.6f}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Confidence:</span>
                        <span class="detail-value risk-high">{confidence:.6f} above threshold</span>
                    </div>
                    
                    <h2>Account Balances</h2>
                    
                    <div class="detail-row">
                        <span class="detail-label">Origin Before:</span>
                        <span class="detail-value">${transaction_data.get('oldbalanceOrg', 0):,.2f}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Origin After:</span>
                        <span class="detail-value">${transaction_data.get('newbalanceOrig', 0):,.2f}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Dest Before:</span>
                        <span class="detail-value">${transaction_data.get('oldbalanceDest', 0):,.2f}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Dest After:</span>
                        <span class="detail-value">${transaction_data.get('newbalanceDest', 0):,.2f}</span>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This is an automated alert from the AI Fraud Detection System</p>
                    <p>Immediate action recommended - Review transaction and freeze accounts if necessary</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

# Singleton instance
email_alerter = EmailAlerter()
