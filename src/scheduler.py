from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pytz import utc
from src.config import get_config

config = get_config()

jobstores = {
  'default': SQLAlchemyJobStore(url=config.SQLALCHEMY_DATABASE_URI)
}

executors = {
  'default': ThreadPoolExecutor(20),
  'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
  'coalesce': False,
  'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors,
                                job_defaults=job_defaults, timezone=utc)