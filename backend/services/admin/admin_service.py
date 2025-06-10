from sqlalchemy.orm import Session
from sqlalchemy import or_, func, extract
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from models.subscription_user import SubscriptionUser
from models.subscription import Subscription
from models.user import User
from models.payment import Payment
from core.roles import UserRole
from core.logger import logger
from schemas.user import UserResponse
from services.user.user_service import UserService
from datetime import datetime, timedelta

class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def get_current_user(self, access_token: str):
        """Get current user using UserService"""
        return self.user_service.get_current_user(access_token)

    def get_users(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """
        Get paginated list of users.
        
        Args:
            skip (int): Number of records to skip
            limit (int): Maximum number of records to return
            
        Returns:
            Dict[str, Any]: Dictionary containing total count and list of users
        """
        try:
            # Get total count
            total = self.db.query(User).count()
            
            # Get paginated users
            users = self.db.query(User).offset(skip).limit(limit).all()
            
            # Convert to response models
            user_responses = [UserResponse.from_orm(user) for user in users]
            
            return {
                "total": total,
                "items": user_responses,
                "skip": skip,
                "limit": limit
            }
            
        except Exception as e:
            logger.error(f"Error getting users: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An error occurred while fetching users"
            )

    def get_subscription_users(
        self,
        skip: int = 0,
        limit: int = 10,
        subscription_name: Optional[str] = None,
        status: Optional[str] = None,
        user_email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get paginated list of subscription users with filtering options.
        
        Args:
            skip (int): Number of records to skip
            limit (int): Maximum number of records to return
            subscription_name (str, optional): Filter by subscription name
            status (str, optional): Filter by subscription status
            user_email (str, optional): Filter by user email
            
        Returns:
            Dict[str, Any]: Dictionary containing total count and list of subscription users
        """
        try:
            # Start with base query
            query = self.db.query(SubscriptionUser).join(
                Subscription, SubscriptionUser.subscription_id == Subscription.id
            ).join(
                User, SubscriptionUser.user_id == User.id
            )

            # Apply filters if provided
            if subscription_name:
                query = query.filter(Subscription.name.ilike(f"%{subscription_name}%"))
            
            if status:
                query = query.filter(SubscriptionUser.status == status)
            
            if user_email:
                query = query.filter(User.email.ilike(f"%{user_email}%"))

            # Get total count
            total = query.count()
            
            # Apply pagination
            subscription_users = query.offset(skip).limit(limit).all()
            
            # Convert to response models
            items = []
            for sub_user in subscription_users:
                item = {
                    "id": sub_user.id,
                    "user_id": sub_user.user_id,
                    "subscription_id": sub_user.subscription_id,
                    "status": sub_user.status,
                    "start_date": sub_user.start_date,
                    "end_date": sub_user.end_date,
                    "created_at": sub_user.created_at,
                    "updated_at": sub_user.updated_at,
                    "stripe_subscription_id": sub_user.stripe_subscription_id,
                    "stripe_customer_id": sub_user.stripe_customer_id,
                    "client_secret": sub_user.client_secret,
                    "subscription_data": sub_user.subscription_data,
                    "data_json": sub_user.data_json,
                    "user": {
                        "id": sub_user.user.id,
                        "email": sub_user.user.email,
                        "role": sub_user.user.role,
                        "is_active": sub_user.user.is_active
                    },
                    "subscription": {
                        "id": sub_user.subscription.id,
                        "name": sub_user.subscription.name,
                        "subscription_type": sub_user.subscription.subscription_type,
                        "price": sub_user.subscription.price,
                        "currency": sub_user.subscription.currency,
                        "duration": sub_user.subscription.duration,
                        "features": sub_user.subscription.features,
                        "is_active": sub_user.subscription.is_active,
                        "stripe_price_id": sub_user.subscription.stripe_price_id,
                        "stripe_product_id": sub_user.subscription.stripe_product_id,
                        "created_at": sub_user.subscription.created_at,
                        "updated_at": sub_user.subscription.updated_at
                    }
                }
                items.append(item)
            
            return {
                "total": total,
                "items": items,
                "skip": skip,
                "limit": limit
            }
            
        except Exception as e:
            logger.error(f"Error getting subscription users: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An error occurred while fetching subscription users"
            )

    def get_payments(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
        payment_type: Optional[str] = None,
        user_email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get paginated list of payments with filtering options.
        
        Args:
            skip (int): Number of records to skip
            limit (int): Maximum number of records to return
            status (str, optional): Filter by payment status
            payment_type (str, optional): Filter by payment type
            user_email (str, optional): Filter by user email
            
        Returns:
            Dict[str, Any]: Dictionary containing total count and list of payments
        """
        try:
            # Start with base query
            query = self.db.query(Payment).join(
                User, Payment.user_id == User.id
            )

            # Apply filters if provided
            if status:
                query = query.filter(Payment.status == status)
            
            if payment_type:
                query = query.filter(Payment.payment_type == payment_type)
            
            if user_email:
                query = query.filter(User.email.ilike(f"%{user_email}%"))

            # Get total count
            total = query.count()
            
            # Apply pagination
            payments = query.offset(skip).limit(limit).all()
            
            # Convert to response models
            items = []
            for payment in payments:
                item = {
                    "id": payment.id,
                    "user_id": payment.user_id,
                    "subscription_id": payment.subscription_id,
                    "subscription_user_id": payment.subscription_user_id,
                    "amount": payment.amount,
                    "currency": payment.currency,
                    "status": payment.status,
                    "stripe_payment_intent_id": payment.stripe_payment_intent_id,
                    "stripe_customer_id": payment.stripe_customer_id,
                    "payment_data": payment.payment_data,
                    "payment_method": payment.payment_method,
                    "payment_type": payment.payment_type,
                    "created_at": payment.created_at,
                    "updated_at": payment.updated_at,
                    "date": payment.date,
                    "data_json": payment.data_json,
                    "user": {
                        "id": payment.user.id,
                        "email": payment.user.email,
                        "role": payment.user.role,
                        "is_active": payment.user.is_active
                    }
                }
                
                # Add subscription info if available
                if payment.subscription:
                    item["subscription"] = {
                        "id": payment.subscription.id,
                        "name": payment.subscription.name,
                        "subscription_type": payment.subscription.subscription_type,
                        "price": payment.subscription.price,
                        "currency": payment.subscription.currency,
                        "duration": payment.subscription.duration,
                        "features": payment.subscription.features,
                        "is_active": payment.subscription.is_active
                    }
                
                items.append(item)
            
            return {
                "total": total,
                "items": items,
                "skip": skip,
                "limit": limit
            }
            
        except Exception as e:
            logger.error(f"Error getting payments: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An error occurred while fetching payments"
            )

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get dashboard statistics including user counts, subscription counts, and payment counts.
        
        Returns:
            Dict[str, Any]: Dictionary containing various statistics
        """
        try:
            # Get current date and first day of current month
            now = datetime.utcnow()
            first_day_of_month = datetime(now.year, now.month, 1)
            first_day_of_last_month = (first_day_of_month - timedelta(days=1)).replace(day=1)

            # User statistics
            active_users = self.db.query(func.count(User.id)).filter(User.is_active == True).scalar()
            inactive_users = self.db.query(func.count(User.id)).filter(User.is_active == False).scalar()
            new_users_this_month = self.db.query(func.count(User.id)).filter(
                User.created_at >= first_day_of_month
            ).scalar()
            
            # Subscription statistics
            subscription_stats = self.db.query(
                SubscriptionUser.status,
                func.count(SubscriptionUser.id)
            ).group_by(SubscriptionUser.status).all()
            
            subscription_counts = {
                "pending": 0,
                "active": 0,
                "cancelled": 0
            }
            
            for status, count in subscription_stats:
                if status in subscription_counts:
                    subscription_counts[status] = count

            # This month's subscription statistics
            this_month_subscription_stats = self.db.query(
                SubscriptionUser.status,
                func.count(SubscriptionUser.id)
            ).filter(
                SubscriptionUser.start_date >= first_day_of_month
            ).group_by(SubscriptionUser.status).all()
            
            this_month_subscription_counts = {
                "pending": 0,
                "active": 0,
                "cancelled": 0
            }
            
            for status, count in this_month_subscription_stats:
                if status in this_month_subscription_counts:
                    this_month_subscription_counts[status] = count
            
            # Payment statistics
            payment_stats = self.db.query(
                Payment.status,
                func.count(Payment.id)
            ).group_by(Payment.status).all()
            
            payment_counts = {
                "pending": 0,
                "completed": 0,
                "cancelled": 0
            }
            
            for status, count in payment_stats:
                if status in payment_counts:
                    payment_counts[status] = count

            # Last month's payment statistics
            last_month_payment_stats = self.db.query(
                Payment.status,
                func.count(Payment.id)
            ).filter(
                Payment.created_at >= first_day_of_last_month,
                Payment.created_at < first_day_of_month
            ).group_by(Payment.status).all()
            
            last_month_payment_counts = {
                "pending": 0,
                "completed": 0,
                "cancelled": 0
            }
            
            for status, count in last_month_payment_stats:
                if status in last_month_payment_counts:
                    last_month_payment_counts[status] = count
            
            return {
                "users": {
                    "active": active_users,
                    "inactive": inactive_users,
                    "total": active_users + inactive_users,
                    "new_this_month": new_users_this_month
                },
                "subscriptions": {
                    "all_time": subscription_counts,
                    "this_month": this_month_subscription_counts
                },
                "payments": {
                    "all_time": payment_counts,
                    "last_month": last_month_payment_counts
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An error occurred while fetching dashboard statistics"
            ) 