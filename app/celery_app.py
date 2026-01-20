from celery import Celery
from app.core.config import settings
from app.tasks import collect_prices


celery = Celery(
    "app",
    broker=f"redis://{settings.redis_host}:{settings.redis_port}/0",
)


celery.conf.beat_schedule = {
    "collect-every-minute": {
        "task": "app.celery_app.collect_prices_task",
        "schedule": 60.0,
    }
}
celery.conf.timezone = "UTC"


@celery.task(name="app.celery_app.collect_prices_task")
def collect_prices_task():
    collect_prices()
