"""
Email service for sending notifications
"""
from flask_mail import Message
from app import mail
from flask import current_app

def send_email(to, subject, body):
    """Send email"""
    try:
        msg = Message(
            subject=subject,
            recipients=[to],
            body=body
        )
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Email sending failed: {str(e)}")
        return False

def send_otp_email(to, otp_code):
    """Send OTP code via email"""
    subject = "Your OTP Code"
    body = f"""
    Your OTP code is: {otp_code}
    
    This code will expire in {current_app.config['OTP_EXPIRY_MINUTES']} minutes.
    
    If you didn't request this code, please ignore this email.
    """
    return send_email(to, subject, body)

def send_transaction_confirmation(to, transaction):
    """Send transaction confirmation email"""
    subject = "Transaction Confirmation"
    body = f"""
    Transaction Completed Successfully
    
    Reference: {transaction.reference}
    Amount: {transaction.amount} {transaction.currency}
    To: {transaction.to_account.account_number}
    Date: {transaction.completed_at}
    Description: {transaction.description or 'N/A'}
    
    Thank you for using our services.
    """
    return send_email(to, subject, body)
