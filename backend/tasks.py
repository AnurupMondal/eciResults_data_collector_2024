import redis
import json
from celery import Celery
from celery.schedules import crontab
from datetime import datetime
import pytz
from scraping_functions import scrape_election_data  # Assume scraping functions are in this module

# Celery configuration
celery = Celery('tasks', broker='redis://redis:6379/0')

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@celery.task
def scrape_and_store_data():
    election_data = scrape_election_data()
    # Convert to UTC+5.5 timezone
    india_tz = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.now(pytz.utc).astimezone(india_tz).strftime('%d/%m/%y, %I:%M:%S %p')
    redis_client.set('election_data', json.dumps(election_data))
    redis_client.set('election_data_timestamp', timestamp)

    # Set an expiration time of 15mins (900 seconds)
    redis_client.expire('election_data', 900)
    redis_client.expire('election_data_timestamp', 900)
    print(f"Election data stored in Redis at {timestamp}.")

@celery.task
def cleanup_old_data():
    # For example, remove all keys with a certain pattern
    keys = redis_client.keys('election_data_*')
    for key in keys:
        redis_client.delete(key)
    print("Old election data cleaned up.")

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/5'), scrape_and_store_data.s())
    sender.add_periodic_task(crontab(hour='*/1'), cleanup_old_data.s())  # Cleanup every hour
    
    # Run the tasks immediately
    scrape_and_store_data.apply_async()
    cleanup_old_data.apply_async()