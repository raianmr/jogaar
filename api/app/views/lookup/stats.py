from app.data.crud import campaign
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
            "campaigns": campaign.greenlit_count(db),
            "campaigners": campaign.successful_campaigner_count(db),
            "pledgers": campaign.successful_pledger_count(db),
            "raised": campaign.successfully_raised(db),
        },
        "failures": {},
    }
