import hashlib
import sqlite3
import secrets
import os
from typing import Optional, Tuple
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.current_user = None
        self.session_token = None
        self.init_database()
    
    def init_database(self):
        """Initialize the user authentication database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                security_question TEXT,
                security_answer_hash TEXT
            )
        ''')
        
        # Create sessions table for login sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create user preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                theme TEXT DEFAULT 'dark',
                auto_backup BOOLEAN DEFAULT TRUE,
                backup_frequency INTEGER DEFAULT 7,
                privacy_mode BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Use PBKDF2 for secure password hashing
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)  # 100,000 iterations
        
        return password_hash.hex(), salt
    
    def create_user(self, username: str, email: str, password: str, 
                   security_question: Optional[str] = None, security_answer: Optional[str] = None) -> Tuple[bool, str]:
        """Create a new user account"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not self.is_valid_email(email):
            return False, "Invalid email format"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if username or email already exists
            cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                         (username, email))
            if cursor.fetchone():
                conn.close()
                return False, "Username or email already exists"
            
            # Hash password
            password_hash, salt = self.hash_password(password)
            
            # Hash security answer if provided
            security_answer_hash = None
            if security_answer:
                security_answer_hash, _ = self.hash_password(security_answer.lower().strip(), salt)
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, salt, 
                                 security_question, security_answer_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, salt, security_question, security_answer_hash))
            
            user_id = cursor.lastrowid
            
            # Create default preferences
            cursor.execute('''
                INSERT INTO user_preferences (user_id) VALUES (?)
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            return True, "Account created successfully"
            
        except sqlite3.Error as e:
            conn.close()
            return False, f"Database error: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get user data
            cursor.execute('''
                SELECT id, username, password_hash, salt, is_active 
                FROM users WHERE username = ? OR email = ?
            ''', (username, username))
            
            user_data = cursor.fetchone()
            if not user_data:
                conn.close()
                return False, "Invalid username or password"
            
            user_id, db_username, stored_hash, salt, is_active = user_data
            
            if not is_active:
                conn.close()
                return False, "Account is deactivated"
            
            # Verify password
            password_hash, _ = self.hash_password(password, salt)
            
            if password_hash != stored_hash:
                conn.close()
                return False, "Invalid username or password"
            
            # Create session
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)  # 24-hour session
            
            cursor.execute('''
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            ''', (user_id, session_token, expires_at))
            
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            # Set current session
            self.current_user = {
                'id': user_id,
                'username': db_username
            }
            self.session_token = session_token
            
            return True, "Login successful"
            
        except sqlite3.Error as e:
            conn.close()
            return False, f"Database error: {str(e)}"
    
    def logout(self) -> bool:
        """Logout current user"""
        if not self.session_token:
            return True
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Deactivate session
            cursor.execute('''
                UPDATE user_sessions SET is_active = FALSE 
                WHERE session_token = ?
            ''', (self.session_token,))
            
            conn.commit()
            conn.close()
            
            # Clear current session
            self.current_user = None
            self.session_token = None
            
            return True
            
        except sqlite3.Error:
            conn.close()
            return False
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in"""
        if not self.session_token or not self.current_user:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT expires_at FROM user_sessions 
                WHERE session_token = ? AND is_active = TRUE
            ''', (self.session_token,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False
            
            expires_at = datetime.fromisoformat(result[0])
            if datetime.now() > expires_at:
                self.logout()
                return False
            
            return True
            
        except sqlite3.Error:
            conn.close()
            return False
    
    def get_current_user(self) -> Optional[dict]:
        """Get current logged-in user info"""
        if self.is_logged_in():
            return self.current_user
        return None
    
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        if not self.is_logged_in():
            return False, "Not logged in"
        
        if len(new_password) < 8:
            return False, "New password must be at least 8 characters long"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Verify old password
            cursor.execute('''
                SELECT password_hash, salt FROM users WHERE id = ?
            ''', (self.current_user['id'],))  # type: ignore
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False, "User not found"
            
            stored_hash, salt = result
            old_password_hash, _ = self.hash_password(old_password, salt)
            
            if old_password_hash != stored_hash:
                conn.close()
                return False, "Current password is incorrect"
            
            # Hash new password
            new_password_hash, new_salt = self.hash_password(new_password)
            
            # Update password
            cursor.execute('''
                UPDATE users SET password_hash = ?, salt = ? WHERE id = ?
            ''', (new_password_hash, new_salt, self.current_user['id']))  # type: ignore
            
            conn.commit()
            conn.close()
            
            return True, "Password changed successfully"
            
        except sqlite3.Error as e:
            conn.close()
            return False, f"Database error: {str(e)}"
    
    def reset_password_with_security_question(self, username: str, security_answer: str, 
                                            new_password: str) -> Tuple[bool, str]:
        """Reset password using security question"""
        if len(new_password) < 8:
            return False, "New password must be at least 8 characters long"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get user data
            cursor.execute('''
                SELECT id, salt, security_answer_hash FROM users 
                WHERE username = ? OR email = ?
            ''', (username, username))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False, "User not found"
            
            user_id, salt, stored_answer_hash = result
            
            if not stored_answer_hash:
                conn.close()
                return False, "No security question set for this account"
            
            # Verify security answer
            answer_hash, _ = self.hash_password(security_answer.lower().strip(), salt)
            
            if answer_hash != stored_answer_hash:
                conn.close()
                return False, "Security answer is incorrect"
            
            # Hash new password
            new_password_hash, new_salt = self.hash_password(new_password)
            
            # Update password
            cursor.execute('''
                UPDATE users SET password_hash = ?, salt = ? WHERE id = ?
            ''', (new_password_hash, new_salt, user_id))
            
            conn.commit()
            conn.close()
            
            return True, "Password reset successfully"
            
        except sqlite3.Error as e:
            conn.close()
            return False, f"Database error: {str(e)}"
    
    def get_security_question(self, username: str) -> Optional[str]:
        """Get security question for password reset"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT security_question FROM users WHERE username = ? OR email = ?
            ''', (username, username))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
            
        except sqlite3.Error:
            conn.close()
            return None
    
    def is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def get_user_database_path(self) -> str:
        """Get user-specific database path"""
        if not self.is_logged_in():
            return "dreams.db"  # Default database
        
        user_id = self.current_user['id']  # type: ignore
        return f"dreams_user_{user_id}.db"
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE user_sessions SET is_active = FALSE 
                WHERE expires_at < CURRENT_TIMESTAMP
            ''')
            conn.commit()
            conn.close()
        except sqlite3.Error:
            conn.close()