from app.data.crud import misc
from app.data.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

# stats should contain:
# + number of greenlit campaigns
# + total pledged from greenlit campaigns
# + number of successful campaigners
# + number of successful pledgers


@router.get("/stats")
async def get_stats(
    db: Session = Depends(get_db),
):
    return {
        "successes": {
            "campaigns": misc.greenlit_count(db),
            "campaigners": misc.successful_campaigner_count(db),
            "pledgers": misc.successful_pledger_count(db),
            "raised": misc.successfully_raised(db),
        },
        "failures": {},
        "technical": {},
    }
