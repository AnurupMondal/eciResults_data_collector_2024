import redis
import json
from celery import Celery
from celery.schedules import crontab
from scraping_functions import scrape_election_data  # Assume scraping functions are in this module

# Celery configuration
celery = Celery('tasks', broker='redis://redis:6379/0')

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@celery.task
def scrape_and_store_data():
    election_data = scrape_election_data()
    redis_client.set('election_data', json.dumps(election_data))
    print("Election data stored in Redis.")
    
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/5'), scrape_and_store_data.s())