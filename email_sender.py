import os
import smtplib
from logger import Logger
from email.mime.text import MIMEText
from smtplib import SMTPException

# Configure logging for this module
logger = Logger.get_logger()

class EmailSender:
    """Handles the process of sending emails with secure credentials."""

    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.receiver_email = os.getenv("RECEIVER_EMAIL")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.port = 465

        if not self.sender_email or not self.receiver_email or not self.password:
            raise EnvironmentError("Environment variables for email credentials are not set.")

    def send_email(self, price, is_exception=False):
        """Sends an email notification for price alert or exception."""
        try:
            # Create email content
            subject = "Exception!" if is_exception else "Price Alert: Deal Found Below 599 ILS!"
            body = f"The price has dropped below 599 ILS! Current price: {price} ILS."
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email

            # Set up the SMTP server and send the email
            logger.info("Connecting to the email server...")
            with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
                logger.info("Email sent successfully!")

        except SMTPException as exception:
            logger.error(f"Failed to send email: {exception}")
            raise
        except Exception as exception:
            logger.error(f"An unexpected error occurred: {exception}")
            raise

# Usage example
if __name__ == "__main__":
    try:
        # Example usage: Set your email, password, and receiver in the environment variables
        email_sender = EmailSender()
        email_sender.send_email(550)  # For a normal price alert
        # email_sender.send_email(0, is_exception=True)  # For an exception case

    except EnvironmentError as e:
        logger.error(f"Environment setup error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
