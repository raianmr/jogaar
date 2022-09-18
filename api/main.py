from fastapi import FastAPI
from uvicorn import run

from config import env
from logic import auth, funding, fundraising, lookup, social

api = FastAPI()

# api.add_middleware(...)
# ...

api.include_router(auth.router)
api.include_router(funding.router)
api.include_router(fundraising.router)
api.include_router(lookup.router)
api.include_router(social.router)


@api.get("/")
async def root():
    return {"message": "it works!"}


# TODO cli commands
if __name__ == "__main__":
    run("main:api", port=env.API_PORT, log_level="info")
