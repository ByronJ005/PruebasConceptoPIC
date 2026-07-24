import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from src.models.user import User
from src.models.password_reset_token import PasswordResetToken
from src.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    db_user = User(email=email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def generate_recovery_token(db: Session, email: str) -> Optional[str]:
    user = get_user_by_email(db, email)
    if not user:
        return None  # Or we return None and let the router handle it
    
    # Generate token
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    # Set expiration time (15 minutes from now)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # Save to db
    db_token = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    
    return token

def verify_and_use_recovery_token(db: Session, token: str, new_password: str) -> bool:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    db_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_hash,
        PasswordResetToken.is_used == False
    ).first()
    
    if not db_token:
        return False
        
    # Check expiration
    now = datetime.now(timezone.utc)
    if db_token.expires_at < now:
        return False
        
    # Use the token and update user password
    user = db_token.user
    user.password_hash = get_password_hash(new_password)
    db_token.is_used = True
    
    db.commit()
    return True
