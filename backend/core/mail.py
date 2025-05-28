import requests
from core.config import settings
from core.logger import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MailService:
    def __init__(self):
        self.api_key = settings.MAILGUN_API_KEY
        self.domain = settings.MAILGUN_DOMAIN
        self.from_email = settings.MAILGUN_FROM_EMAIL
        self.api_url = f"https://api.mailgun.net/v3/{self.domain}/messages"

    def send_email(self, to_email: str, subject: str, body: str) -> dict:
        """
        Send an email using Mailgun API.
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Email body
            
        Returns:
            dict: Response from Mailgun API
            
        Raises:
            Exception: If email sending fails
        """
        try:
            data = {
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "text": body
            }

            response = requests.post(
                self.api_url,
                auth=("api", self.api_key),
                data=data
            )
            
            if response.status_code != 200:
                raise Exception(f"Mailgun API error: {response.text}")

            logger.info(f"Email sent successfully to {to_email}")
            return response.json()

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise

# Create a singleton instance
mail_service = MailService() 