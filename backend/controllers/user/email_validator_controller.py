from fastapi import APIRouter, HTTPException, Depends, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db
from services.user.user_service import UserService
from services.email.email_service import EmailService
from schemas.user import EmailVerificationRequest
from core.mail import MailService
from core.logger import logger
import requests

class EmailValidatorController:
    def __init__(self):
        self.router = APIRouter(tags=["email"])
        self.setup_routes()

    def setup_routes(self):
        @self.router.post("/send-verification")
        async def send_verification(
            authorization: Optional[str] = Header(None),
            db: Session = Depends(get_db)
        ):
            try:
                if not authorization or not authorization.startswith("Bearer "):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authorization header"
                    )

                token = authorization.split(" ")[1]
                user_service = UserService(db)
                user = user_service.get_current_user(token)

                if user.is_verified:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already verified"
                    )

                email_service = EmailService(db)
                verification_token = email_service.generate_verification_token(user.id)
                
                # Send verification email directly
                mail_service = MailService()
                subject = "Verify Your Email"
                body = f"""
                Hello,
                
                Thank you for registering. Please use the following token to verify your email:
                
                {verification_token}
                
                This token will expire in 24 hours.
                
                Best regards,
                Your App Team
                """
                try:
                    mail_service.send_email(user.email, subject, body)
                except ValueError as e:
                    logger.error(f"Email configuration error: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Email service is not properly configured"
                    )
                except requests.exceptions.RequestException as e:
                    logger.error(f"Email service request failed: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Email service is currently unavailable"
                    )
                except Exception as e:
                    logger.error(f"Unexpected error sending email: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="An error occurred while sending verification email"
                    )
                
                return {"message": "Verification email sent successfully"}

            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error in send_verification: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while processing your request"
                )

        @self.router.post("/verify")
        async def verify_email(
            request: EmailVerificationRequest,
            db: Session = Depends(get_db)
        ):
            try:
                email_service = EmailService(db)
                user = email_service.verify_email_token(request.token)
                
                return {
                    "message": "Email verified successfully",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "is_verified": user.is_verified
                    }
                }

            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error verifying email: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while verifying email"
                )

# Create router instance
email_validator_controller = EmailValidatorController()
router = email_validator_controller.router 