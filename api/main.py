import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from config import env
from logic import auth, funding, fundraising, lookup, social

api = FastAPI(
    title="Jogaar",
    description="""Jogaar is a crowdfunding platform for future small business owners.""",
    version="0.0.1",
)

api.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [
    auth.router,
    funding.router,
    fundraising.router,
    lookup.router,
    social.router,
]:
    api.include_router(router)


@api.get("/")
async def root():
    return RedirectResponse(api.docs_url) if api.docs_url else {"message": "no docs"}


# TODO cli
if __name__ == "__main__":
    uvicorn.run("main:api", port=env.API_PORT, log_level="info")
