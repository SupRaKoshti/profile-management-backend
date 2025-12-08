from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.dependencies import get_current_user
from app.database import get_db
from app.models.users import User
from app.schemas.profile import ProfileResponse, ProfileUpdateRequest

from app.logger import logger

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me", response_model=ProfileResponse)
def read_my_profile(
    current_user: User = Depends(get_current_user),
) -> ProfileResponse:
    """
    Return the currently authenticated user's profile.
    """
    logger.info(f"Profile accessed by the user: {current_user.id}")
    return ProfileResponse.model_validate(current_user)


@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    updates: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    """
    Update the authenticated user's profile.
    """
    logger.info(f"Profile update requested by user: {current_user.id}")
    logger.debug(f"Update data: {updates.model_dump()}")

    if updates.name is not None:
        current_user.name = updates.name
    if updates.bio is not None:
        current_user.bio = updates.bio

    db.commit()
    db.refresh(current_user)

    logger.info(f"Profile updated successfully for user: {current_user.id}")

    return ProfileResponse.model_validate(current_user)


@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Soft delete the authenticated user's profile.
    Marks the user as inactive but retains data.
    """
    logger.info(f"Profile deletion requested by user: {current_user.id}")
    current_user.is_active = False
    db.commit()
    logger.info(f"Profile marked as inactive for user: {current_user.id}")
    return {"message": "Profile deleted successfully"}