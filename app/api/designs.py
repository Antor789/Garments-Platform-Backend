from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.design import DesignCreate, DesignResponse
from app.models.design import Design
from app.models.user import User
from app.api.deps import get_current_user # Now active thanks to our fixes!

router = APIRouter(prefix="/designs", tags=["Designs"])

@router.post("/", response_model=DesignResponse)
def create_design(
    design_in: DesignCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Protected Route
):
    """
    Creates a new garment design linked to the authenticated user.
    Uses the JSON 'specifications' field for flexible measurement data.
    """
    new_design = Design(
        title=design_in.title,
        category=design_in.category,
        specifications=design_in.specifications,
        creator_id=current_user.id # Dynamically linked to the logged-in Buyer
    )
    db.add(new_design)
    db.commit()
    db.refresh(new_design)
    return new_design

@router.get("/my-designs", response_model=list[DesignResponse])
def get_user_designs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves only the designs belonging to the current user.
    """
    return db.query(Design).filter(Design.creator_id == current_user.id).all()