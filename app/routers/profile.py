from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user
from app.database import get_db
from app.models.users import User
from app.schemas.profile import ProfileResponse, ProfileUpdateRequest, ProfileDeleteRequest


router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me", response_model=ProfileResponse)
def read_my_profile(
    current_user: User = Depends(get_current_user),
) -> ProfileResponse:
    """
    Return the currently authenticated user's profile.
    """
    return ProfileResponse.model_validate(current_user)


@router.patch("/me", response_model=ProfileResponse)
def update_my_profile(
    updates: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    """
    Partially update the authenticated user's profile.
    Only the fields provided in the request body will be updated.
    """
    if updates.name is not None:
        current_user.name = updates.name
    if updates.bio is not None:
        current_user.bio = updates.bio

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return ProfileResponse.model_validate(current_user)

@router.delete("/me", response_model=ProfileResponse)
def delete_my_profile(
    delete: ProfileDeleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ProfileResponse:
    """
    Soft delete the authenticated user's profile.
    The user's profile will be marked as deleted but the data will be retained for future reference.
    """
    if delete.id is not None:
        current_user.id = delete.id
    if delete.name is not None:
        current_user.name = delete.name
    
    current_user.is_active = False
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return ProfileResponse.model_validate(current_user)
