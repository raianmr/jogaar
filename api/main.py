from fastapi import FastAPI
from uvicorn import run

from .config import ENV
from .auth import auth
from .funding import funding
from .fundraising import fundraising
from .lookup import lookup
from .people import people
from .social import social

api = FastAPI()

# api.add_middleware(...)
# ...

api.include_router(auth.router)
api.include_router(funding.router)
api.include_router(fundraising.router)
api.include_router(lookup.router)
api.include_router(people.router)
api.include_router(social.router)


@api.get("/")
async def root():
    return {"message": "it works!"}


# TODO cli commands
# TODO fix import errors
if __name__ == "__main__":
    run("main:api", port=ENV.API_PORT, log_level="info")
