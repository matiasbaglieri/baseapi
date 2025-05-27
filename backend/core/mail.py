from mailgun import Mailgun
from core.config import settings
from core.logger import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MailService:
    def __init__(self):
        self.mailgun = Mailgun(
            api_key=os.getenv("MAILGUN_API_KEY"),
            domain=os.getenv("MAILGUN_DOMAIN")
        )
        self.from_email = os.getenv("MAILGUN_FROM_EMAIL", f"noreply@{os.getenv('MAILGUN_DOMAIN')}")

    def send_email(self, to_email: str, subject: str, body: str, html_body: str = None) -> dict:
        """
        Send an email using Mailgun.
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Plain text email body
            html_body (str, optional): HTML email body
            
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
            
            if html_body:
                data["html"] = html_body

            response = self.mailgun.send_message(data)
            logger.info(f"Email sent successfully to {to_email}")
            return response

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise

# Create a singleton instance
mail_service = MailService() 