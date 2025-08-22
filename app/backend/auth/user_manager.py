# app/backend/auth/user_manager.py
# User management and authentication

import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any
import streamlit as st

class UserManager:
    """Manages user authentication and sessions"""
    
    def __init__(self):
        # In a real application, this would be stored in a database
        # For now, we'll use a simple in-memory storage
        self.users = {
            "admin": {
                "id": 1,
                "username": "admin",
                "password_hash": self._hash_password("admin123"),
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin",
                "is_active": True,
                "created_at": datetime.now(),
                "last_login": None
            },
            "user1": {
                "id": 2,
                "username": "user1",
                "password_hash": self._hash_password("user123"),
                "first_name": "Regular",
                "last_name": "User",
                "role": "user",
                "is_active": True,
                "created_at": datetime.now(),
                "last_login": None
            }
        }
        
        # Session storage (in-memory for demo)
        self.sessions = {}
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        return self._hash_password(password) == password_hash
    
    def authenticate_user(self, username: str, password: str, 
                         ip_address: Optional[str] = None, 
                         user_agent: Optional[str] = None) -> Tuple[bool, str, Optional[Dict]]:
        """Authenticate a user with username and password"""
        try:
            if username not in self.users:
                return False, "Invalid username or password", None
            
            user = self.users[username]
            
            if not user["is_active"]:
                return False, "Account is deactivated", None
            
            if not self._verify_password(password, user["password_hash"]):
                return False, "Invalid username or password", None
            
            # Update last login
            user["last_login"] = datetime.now()
            
            # Log successful authentication
            self._log_auth_attempt(username, True, ip_address, user_agent)
            
            return True, "Authentication successful", user
            
        except Exception as e:
            self._log_auth_attempt(username, False, ip_address, user_agent, str(e))
            return False, f"Authentication error: {str(e)}", None
    
    def create_session(self, user_id: int) -> Tuple[str, str]:
        """Create a new session for a user"""
        try:
            # Generate session token
            session_token = secrets.token_urlsafe(32)
            refresh_token = secrets.token_urlsafe(32)
            
            # Store session
            self.sessions[session_token] = {
                "user_id": user_id,
                "created_at": datetime.now(),
                "expires_at": datetime.now() + timedelta(hours=24),
                "refresh_token": refresh_token,
                "is_active": True
            }
            
            return session_token, refresh_token
            
        except Exception as e:
            raise Exception(f"Failed to create session: {str(e)}")
    
    def validate_session(self, session_token: str) -> Optional[Dict]:
        """Validate a session token"""
        try:
            if session_token not in self.sessions:
                return None
            
            session = self.sessions[session_token]
            
            # Check if session is active
            if not session["is_active"]:
                return None
            
            # Check if session has expired
            if datetime.now() > session["expires_at"]:
                session["is_active"] = False
                return None
            
            # Get user information
            user_id = session["user_id"]
            user = next((u for u in self.users.values() if u["id"] == user_id), None)
            
            if not user or not user["is_active"]:
                session["is_active"] = False
                return None
            
            return {
                "user_id": user_id,
                "username": user["username"],
                "role": user["role"],
                "is_active": user["is_active"],
                "session_data": session
            }
            
        except Exception as e:
            return None
    
    def invalidate_session(self, session_token: str) -> bool:
        """Invalidate a session"""
        try:
            if session_token in self.sessions:
                self.sessions[session_token]["is_active"] = False
                return True
            return False
        except Exception:
            return False
    
    def refresh_session(self, refresh_token: str) -> Optional[str]:
        """Refresh a session using a refresh token"""
        try:
            # Find session with matching refresh token
            for session_token, session in self.sessions.items():
                if session.get("refresh_token") == refresh_token and session["is_active"]:
                    # Generate new session token
                    new_session_token = secrets.token_urlsafe(32)
                    new_refresh_token = secrets.token_urlsafe(32)
                    
                    # Update session
                    session["refresh_token"] = new_refresh_token
                    session["expires_at"] = datetime.now() + timedelta(hours=24)
                    
                    # Create new session entry
                    self.sessions[new_session_token] = {
                        "user_id": session["user_id"],
                        "created_at": datetime.now(),
                        "expires_at": session["expires_at"],
                        "refresh_token": new_refresh_token,
                        "is_active": True
                    }
                    
                    # Invalidate old session
                    session["is_active"] = False
                    
                    return new_session_token
            
            return None
            
        except Exception as e:
            return None
    
    def _log_auth_attempt(self, username: str, success: bool, 
                          ip_address: Optional[str], user_agent: Optional[str], 
                          error_message: Optional[str] = None):
        """Log authentication attempts"""
        try:
            # In a real application, this would be logged to a database or log file
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = "SUCCESS" if success else "FAILED"
            
            log_entry = f"[{timestamp}] AUTH {status} - User: {username}"
            if ip_address:
                log_entry += f" - IP: {ip_address}"
            if error_message:
                log_entry += f" - Error: {error_message}"
            
            print(log_entry)  # Replace with proper logging
            
        except Exception:
            pass  # Don't let logging errors break authentication
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user information by ID"""
        return next((u for u in self.users.values() if u["id"] == user_id), None)
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user information by username"""
        return self.users.get(username)
    
    def update_user(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update user information"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            # Update allowed fields
            allowed_fields = ["first_name", "last_name", "role", "is_active"]
            for field, value in updates.items():
                if field in allowed_fields:
                    user[field] = value
            
            return True
            
        except Exception:
            return False
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            # Verify old password
            if not self._verify_password(old_password, user["password_hash"]):
                return False
            
            # Update password
            user["password_hash"] = self._hash_password(new_password)
            return True
            
        except Exception:
            return False
