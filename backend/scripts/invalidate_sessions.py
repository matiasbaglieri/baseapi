import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = str(Path(__file__).parent.parent)
sys.path.append(backend_dir)

from tasks.session_tasks import invalidate_all_sessions
from core.logger import logger

def main():
    """
    Main function to invalidate all sessions.
    This is useful when rotating JWT secret keys or during security incidents.
    """
    try:
        logger.info("Starting session invalidation...")
        invalidate_all_sessions.delay()
        logger.info("Session invalidation task has been queued")
    except Exception as e:
        logger.error(f"Error queuing session invalidation task: {str(e)}")
        raise

if __name__ == "__main__":
    main() 