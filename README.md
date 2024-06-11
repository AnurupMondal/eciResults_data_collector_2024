![image](https://github.com/AnurupMondal/eciResults_data_collector_2024/assets/45717023/1af89516-04ea-4b00-8449-5e2935a99dd9)
Model for the above Project

# eciResults_data_collector_2024

eciResults_data_collector_2024 is a web application that scrapes election data, stores it in Redis, and displays it using a Streamlit frontend. The backend is built with FastAPI and Celery, and the entire application is containerized using Docker.

Dark Mode
![image](https://github.com/AnurupMondal/eciResults_data_collector_2024/assets/45717023/eb50dfbd-6fa2-4053-8ac0-c4a51e55725d)
![image](https://github.com/AnurupMondal/eciResults_data_collector_2024/assets/45717023/d229a673-a30f-47fb-93be-8f467901a731)

Light Mode
![image](https://github.com/AnurupMondal/eciResults_data_collector_2024/assets/45717023/f32aee97-3d37-47e9-a36c-7175365a6ece)
![image](https://github.com/AnurupMondal/eciResults_data_collector_2024/assets/45717023/8e9e24dd-dd76-4837-b6a3-ab10ba9699f7)


## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Docker Configuration](#docker-configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Scrapes election data every 5 minutes and stores it in Redis.
- Displays election data in a tabular format using Streamlit.
- Highlights vote changes in green (positive) or red (negative).
- Automatically updates the frontend with the latest data.

## Architecture

The project is structured into two main components:

- **Backend**: Responsible for scraping election data, storing it in Redis, and serving it via a FastAPI endpoint.
- **Frontend**: A Streamlit app that fetches data from the backend and displays it in a table.

The backend uses Celery for periodic data scraping tasks, and Docker Compose is used to orchestrate the services.

### Prerequisites

- Docker
- Docker Compose

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/eciResults_data_collector_2024.git
   cd eciResults_data_collector_2024

2. **Build and start the Docker containers:**
   ```sh
   docker-compose up --build
  This will start the Redis server, the backend service, the Celery workers, and the Streamlit frontend.
  
## Usage

Once the containers are up and running, open your web browser and navigate to:
    ```sh
    http://localhost:8501

The Streamlit app will display the election data, with the most recent fetch timestamp shown at the top left corner.

## Project Structure
     
      ├── backend/
      │   ├── main.py
      │   ├── tasks.py
      │   ├── scraping_functions.py
      │   ├── requirements.txt
      │   ├── Dockerfile
      ├── frontend/
      │   ├── streamlit_app.py
      │   ├── requirements.txt
      │   ├── Dockerfile
      ├── docker-compose.yml
      └── README.md

## Docker Configuration

      version: '3.8'
      services:
        redis:
          image: redis:6.0-alpine
          container_name: redis
          ports:
            - "6379:6379"
      
        backend:
          build: ./backend
          container_name: backend
          depends_on:
            - redis
          environment:
            - CELERY_BROKER_URL=redis://redis:6379/0
            - CELERY_RESULT_BACKEND=redis://redis:6379/0
          ports:
            - "8000:8000"
      
        celery:
          build: ./backend
          container_name: celery
          depends_on:
            - redis
          command: celery -A tasks worker --loglevel=info
      
        celery-beat:
          build: ./backend
          container_name: celery-beat
          depends_on:
            - redis
          command: celery -A tasks beat --loglevel=info
      
        frontend:
          build: ./frontend
          container_name: frontend
          depends_on:
            - redis
            - backend
          ports:
            - "8501:8501"

## Contributing
  Contributions are welcome! Please follow these steps to contribute:

  1. Fork the repository.
  2. Create a new branch with a descriptive name.
  3. Make your changes and commit them with clear and concise messages.
  4. Push your changes to your fork.
  5. Create a pull request to the main repository.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
