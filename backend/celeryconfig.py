from celery.schedules import crontab

# Task settings
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

# Beat schedule
beat_schedule = {
    'cleanup-expired-sessions': {
        'task': 'cleanup_expired_sessions',
        # Run every day at midnight UTC
        'schedule': crontab(hour=0, minute=0),
    },
} 