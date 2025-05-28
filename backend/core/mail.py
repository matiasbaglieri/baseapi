import requests
from core.config import settings
from core.logger import logger
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class MailService:
    def __init__(self):
        self.api_key = settings.MAILGUN_API_KEY
        self.domain = settings.MAILGUN_DOMAIN
        self.from_email = settings.MAILGUN_FROM_EMAIL
        self.api_url = f"https://api.mailgun.net/v3/{self.domain}/messages"
        self.dev_mode = os.getenv("DEV_MODE", "true").lower() == "true"
        
        # Log configuration status
        logger.info("Initializing MailService with configuration:")
        logger.info(f"Domain: {self.domain}")
        logger.info(f"From Email: {self.from_email}")
        logger.info(f"API Key: {'Configured' if self.api_key and self.api_key != 'your-api-key-here' else 'Not configured'}")
        logger.info(f"Development Mode: {'Enabled' if self.dev_mode else 'Disabled'}")
        
        # Validate required settings
        missing_settings = []
        if not self.api_key or self.api_key == "your-api-key-here":
            missing_settings.append("MAILGUN_API_KEY")
        if not self.domain or self.domain == "your-domain.com":
            missing_settings.append("MAILGUN_DOMAIN")
        if not self.from_email or self.from_email == "noreply@your-domain.com":
            missing_settings.append("MAILGUN_FROM_EMAIL")
            
        if missing_settings and not self.dev_mode:
            error_msg = f"Missing or invalid Mailgun configuration: {', '.join(missing_settings)}. Please update your .env-local file with proper values."
            logger.error(error_msg)
            raise ValueError(error_msg)

    def send_email(self, to_email: str, subject: str, body: str) -> dict:
        """
        Send an email using Mailgun API or log it in development mode.
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Email body
            
        Returns:
            dict: Response from Mailgun API or development mode response
        """
        try:
            # Validate email address
            if not to_email or "@" not in to_email:
                raise ValueError(f"Invalid email address: {to_email}")

            if self.dev_mode:
                # In development mode, log the email instead of sending it
                email_data = {
                    "from": self.from_email,
                    "to": to_email,
                    "subject": subject,
                    "body": body,
                    "timestamp": datetime.now().isoformat()
                }
                logger.info("Development Mode - Email would have been sent:")
                logger.info(json.dumps(email_data, indent=2))
                return {
                    "status": "success",
                    "message": "Email logged (development mode)",
                    "data": email_data
                }

            # Production mode - send actual email
            data = {
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "text": body
            }

            logger.info(f"Sending email to {to_email} using Mailgun API")
            logger.debug(f"Mailgun API URL: {self.api_url}")
            logger.debug(f"Mailgun Domain: {self.domain}")

            response = requests.post(
                self.api_url,
                auth=("api", self.api_key),
                data=data
            )
            
            if response.status_code != 200:
                error_msg = f"Mailgun API error (Status {response.status_code}): {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)

            logger.info(f"Email sent successfully to {to_email}")
            return response.json()

        except ValueError as e:
            logger.error(f"Configuration error: {str(e)}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Mailgun API request failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise

# Create a singleton instance
try:
    mail_service = MailService()
except ValueError as e:
    logger.error(f"Failed to initialize MailService: {str(e)}")
    mail_service = None 