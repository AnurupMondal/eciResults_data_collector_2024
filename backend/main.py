from fastapi import FastAPI, HTTPException
import redis
import json

app = FastAPI()

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.get('/fetch_election_data')
def fetch_election_data():
    data = redis_client.get('election_data')
    timestamp = redis_client.get('election_data_timestamp')
    if data and timestamp:
        return {"data": json.loads(data), "timestamp": timestamp}
    else:
        raise HTTPException(status_code=404, detail="No data found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)