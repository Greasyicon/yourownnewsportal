# celery_config.py

from datetime import timedelta
from urllib.parse import urlparse
import os

BROKER_URL = os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@localhost:5672//")
result_backend = BROKER_URL#os.environ.get("REDIS_URL", "redis://localhost:6379/0")

parsed_url = urlparse(BROKER_URL)
CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_BACKEND = result_backend

CELERYBEAT_SCHEDULE = {
    "update_content_task": {
        "task": "app.update_content_task",
        "schedule": timedelta(hours=10)
    }
}
