"""
Celery configuration file.
Contains task annotations, rate limits, and other Celery settings.
"""

# Task annotations for rate limiting and other settings
task_annotations = {
    'tasks.email_tasks.send_email': {
        'rate_limit': '10/m',  # Maximum 10 emails per minute
        'time_limit': 30,      # 30 seconds timeout
        'soft_time_limit': 25, # Soft timeout at 25 seconds
        'retry_backoff': True, # Enable exponential backoff for retries
        'max_retries': 3       # Maximum number of retries
    },
    'tasks.user_tasks.cleanup_inactive_users': {
        'rate_limit': '1/h',   # Run once per hour
        'time_limit': 300,     # 5 minutes timeout
        'soft_time_limit': 240 # Soft timeout at 4 minutes
    }
}

# Task routing
task_routes = {
    'tasks.email_tasks.*': {'queue': 'email'},
    'tasks.user_tasks.*': {'queue': 'user'}
}

# Task serialization
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'

# Timezone settings
timezone = 'UTC'
enable_utc = True

# Worker settings
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000
worker_max_memory_per_child = 150000  # 150MB

# Result backend settings
result_expires = 3600  # Results expire after 1 hour

# Broker settings
broker_connection_retry_on_startup = True
broker_connection_max_retries = 10

# Logging
worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
worker_task_log_format = '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s' 