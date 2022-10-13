# Jogaar

Jogaar is a crowdfunding platform for future small business owners.

The project is in its infancy, and as this is quite literally my very first
attempt at RESTful APIs, the gate of suggestions is always open.

# Running locally

For development, make a `.env.dev` in `./Jogaar` and run

```
docker compose up -d --build
```

For production, make a `.env.prod` in `./Jogaar` and run

```
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Creation of databases isn't handled programmatically.
