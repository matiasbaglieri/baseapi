"""
Core package for application configuration and initialization.
"""

from .celery_app import celery_app, init_celery, shutdown_celery
from .config import settings

__all__ = ["celery_app", "init_celery", "shutdown_celery", "settings"] 