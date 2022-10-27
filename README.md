# Jogaar

Jogaar is a crowdfunding platform for future small business owners.

The project is in its infancy, and this is literally my very first attempt at
RESTful APIs. The gate of suggestions is always open.

# Running locally

For development, make a `.env.dev` in `./Jogaar` and run

```
docker compose up -d --build
```

For production, make a `.env.prod` in `./Jogaar` and run

```
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Refer to ./api/app/core/config.py for the contents of these .env* files.

For non-dockerized environments, create and activate a Python virtual environment
and run

```
cd ./api/
pip install -U -r requirements.txt
uvicorn app.main:app --reload
```

Creation of databases isn't handled from within the application. To create the tables, run

```
alembic upgrade head
```
