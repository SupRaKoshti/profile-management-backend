from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.dependencies import get_current_user
from app.database import get_db
from app.schemas.auth import SignUpRequest, LoginRequest, ChangePasswordRequest, TokenResponse
from app.models.users import User
from app.utils.auth import create_access_token
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def sign_up(request: SignUpRequest, db: Session = Depends(get_db)):
    exiting_user = db.query(User).filter(User.email == request.email).first()
    if exiting_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(request.password)

    new_user = User(
        email=request.email,
        name=request.name,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"user_id": new_user.id})

    return TokenResponse(access_token=token, token_type="bearer")

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token = create_access_token(data={"user_id": user.id})

    return TokenResponse(access_token=token, token_type="bearer")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    _: User = Depends(get_current_user),
) -> Response:
    """
    Stateless logout endpoint.
    It only validates the current token; the client must delete the token
    from storage (e.g. localStorage / cookies) to complete logout.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    """
    Change the authenticated user's password.
    Requires the correct old password and a new password.
    """
    if not verify_password(payload.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )

    current_user.password = hash_password(payload.new_password)
    db.add(current_user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/me", response_model=str)
def get_current_user_info():
    return "Hello, World!"
