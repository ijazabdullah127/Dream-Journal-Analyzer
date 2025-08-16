import customtkinter as ctk
from tkinter import messagebox
from auth_manager import AuthManager
from typing import Optional, Callable

class LoginWindow:
    def __init__(self, on_login_success: Callable[[AuthManager], None]):
        self.auth_manager = AuthManager()
        self.on_login_success = on_login_success
        self.window: Optional[ctk.CTk] = None
        self.create_login_window()
    
    def create_login_window(self):
        """Create the login window"""
        self.window = ctk.CTk()
        self.window.title("🌙 Dream Journal - Login")
        self.window.geometry("450x795")
        self.window.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🌙 Dream Journal Analyzer",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Secure Access to Your Dreams",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Create tabview for login/signup
        self.tabview = ctk.CTkTabview(main_frame, width=400, height=400)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Add tabs
        self.tabview.add("Login")
        self.tabview.add("Sign Up")
        self.tabview.add("Reset Password")
        
        # Create login tab
        self.create_login_tab()
        
        # Create signup tab
        self.create_signup_tab()
        
        # Create reset password tab
        self.create_reset_tab()
        
        # Footer
        footer_label = ctk.CTkLabel(
            main_frame,
            text="Your dreams are private and secure 🔒",
            font=ctk.CTkFont(size=12)
        )
        footer_label.pack(pady=(10, 20))
    
    def create_login_tab(self):
        """Create the login tab"""
        login_frame = self.tabview.tab("Login")
        
        # Username field
        ctk.CTkLabel(login_frame, text="Username or Email:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        self.login_username = ctk.CTkEntry(
            login_frame,
            placeholder_text="Enter username or email",
            width=300,
            height=40
        )
        self.login_username.pack(pady=5)
        
        # Password field
        ctk.CTkLabel(login_frame, text="Password:", font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
        self.login_password = ctk.CTkEntry(
            login_frame,
            placeholder_text="Enter password",
            show="*",
            width=300,
            height=40
        )
        self.login_password.pack(pady=5)
        
        # Login button
        login_btn = ctk.CTkButton(
            login_frame,
            text="🔓 Login",
            command=self.handle_login,
            width=300,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        login_btn.pack(pady=20)
        
        # Bind Enter key to login
        self.login_password.bind("<Return>", lambda e: self.handle_login())
        
        # Remember me checkbox
        self.remember_me = ctk.BooleanVar()
        remember_checkbox = ctk.CTkCheckBox(
            login_frame,
            text="Remember me",
            variable=self.remember_me
        )
        remember_checkbox.pack(pady=5)
    
    def create_signup_tab(self):
        """Create the signup tab"""
        signup_frame = self.tabview.tab("Sign Up")
        
        # Username field
        ctk.CTkLabel(signup_frame, text="Username:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.signup_username = ctk.CTkEntry(
            signup_frame,
            placeholder_text="Choose a username",
            width=300,
            height=35
        )
        self.signup_username.pack(pady=2)
        
        # Email field
        ctk.CTkLabel(signup_frame, text="Email:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.signup_email = ctk.CTkEntry(
            signup_frame,
            placeholder_text="Enter your email",
            width=300,
            height=35
        )
        self.signup_email.pack(pady=2)
        
        # Password field
        ctk.CTkLabel(signup_frame, text="Password:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.signup_password = ctk.CTkEntry(
            signup_frame,
            placeholder_text="Create a password (8+ characters)",
            show="*",
            width=300,
            height=35
        )
        self.signup_password.pack(pady=2)
        
        # Confirm password field
        ctk.CTkLabel(signup_frame, text="Confirm Password:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.signup_confirm_password = ctk.CTkEntry(
            signup_frame,
            placeholder_text="Confirm your password",
            show="*",
            width=300,
            height=35
        )
        self.signup_confirm_password.pack(pady=2)
        
        # Security question
        ctk.CTkLabel(signup_frame, text="Security Question (Optional):", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.security_question = ctk.CTkEntry(
            signup_frame,
            placeholder_text="e.g., What was your first pet's name?",
            width=300,
            height=35
        )
        self.security_question.pack(pady=2)
        
        # Security answer
        ctk.CTkLabel(signup_frame, text="Security Answer:", font=ctk.CTkFont(size=14)).pack(pady=(5, 5))
        self.security_answer = ctk.CTkEntry(
            signup_frame,
            placeholder_text="Answer to your security question",
            width=300,
            height=35
        )
        self.security_answer.pack(pady=2)
        
        # Sign up button
        signup_btn = ctk.CTkButton(
            signup_frame,
            text="✨ Create Account",
            command=self.handle_signup,
            width=300,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        signup_btn.pack(pady=15)
    
    def create_reset_tab(self):
        """Create the password reset tab"""
        reset_frame = self.tabview.tab("Reset Password")
        
        # Username field
        ctk.CTkLabel(reset_frame, text="Username or Email:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        self.reset_username = ctk.CTkEntry(
            reset_frame,
            placeholder_text="Enter username or email",
            width=300,
            height=40
        )
        self.reset_username.pack(pady=5)
        
        # Get security question button
        get_question_btn = ctk.CTkButton(
            reset_frame,
            text="Get Security Question",
            command=self.get_security_question,
            width=300,
            height=35
        )
        get_question_btn.pack(pady=10)
        
        # Security question display
        self.security_question_label = ctk.CTkLabel(
            reset_frame,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=280
        )
        self.security_question_label.pack(pady=5)
        
        # Security answer field
        ctk.CTkLabel(reset_frame, text="Security Answer:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.reset_security_answer = ctk.CTkEntry(
            reset_frame,
            placeholder_text="Enter your security answer",
            width=300,
            height=40
        )
        self.reset_security_answer.pack(pady=5)
        
        # New password field
        ctk.CTkLabel(reset_frame, text="New Password:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.reset_new_password = ctk.CTkEntry(
            reset_frame,
            placeholder_text="Enter new password",
            show="*",
            width=300,
            height=40
        )
        self.reset_new_password.pack(pady=5)
        
        # Reset password button
        reset_btn = ctk.CTkButton(
            reset_frame,
            text="🔄 Reset Password",
            command=self.handle_password_reset,
            width=300,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        reset_btn.pack(pady=15)
    
    def center_window(self):
        """Center the window on screen"""
        if self.window:
            self.window.update_idletasks()
            width = self.window.winfo_width()
            height = self.window.winfo_height()
            x = (self.window.winfo_screenwidth() // 2) - (width // 2)
            y = (self.window.winfo_screenheight() // 2) - (height // 2)
            self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def handle_login(self):
        """Handle login attempt"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        success, message = self.auth_manager.authenticate_user(username, password)
        
        if success:
            messagebox.showinfo("Success", message)
            if self.window:
                self.window.destroy()
            self.on_login_success(self.auth_manager)
        else:
            messagebox.showerror("Login Failed", message)
    
    def handle_signup(self):
        """Handle signup attempt"""
        username = self.signup_username.get().strip()
        email = self.signup_email.get().strip()
        password = self.signup_password.get()
        confirm_password = self.signup_confirm_password.get()
        security_question = self.security_question.get().strip()
        security_answer = self.security_answer.get().strip()
        
        # Validation
        if not all([username, email, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if security_question and not security_answer:
            messagebox.showerror("Error", "Please provide an answer to your security question")
            return
        
        # Create account
        success, message = self.auth_manager.create_user(
            username, email, password, 
            security_question if security_question else None,
            security_answer if security_answer else None
        )
        
        if success:
            messagebox.showinfo("Success", f"{message}\nYou can now login with your credentials.")
            # Switch to login tab
            self.tabview.set("Login")
            # Clear signup fields
            self.clear_signup_fields()
        else:
            messagebox.showerror("Signup Failed", message)
    
    def get_security_question(self):
        """Get security question for password reset"""
        username = self.reset_username.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter username or email")
            return
        
        question = self.auth_manager.get_security_question(username)
        
        if question:
            self.security_question_label.configure(text=f"Security Question: {question}")
        else:
            messagebox.showerror("Error", "No security question found for this user")
    
    def handle_password_reset(self):
        """Handle password reset attempt"""
        username = self.reset_username.get().strip()
        security_answer = self.reset_security_answer.get().strip()
        new_password = self.reset_new_password.get()
        
        if not all([username, security_answer, new_password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, message = self.auth_manager.reset_password_with_security_question(
            username, security_answer, new_password
        )
        
        if success:
            messagebox.showinfo("Success", f"{message}\nYou can now login with your new password.")
            # Switch to login tab
            self.tabview.set("Login")
            # Clear reset fields
            self.clear_reset_fields()
        else:
            messagebox.showerror("Reset Failed", message)
    
    def clear_signup_fields(self):
        """Clear signup form fields"""
        self.signup_username.delete(0, "end")
        self.signup_email.delete(0, "end")
        self.signup_password.delete(0, "end")
        self.signup_confirm_password.delete(0, "end")
        self.security_question.delete(0, "end")
        self.security_answer.delete(0, "end")
    
    def clear_reset_fields(self):
        """Clear reset form fields"""
        self.reset_username.delete(0, "end")
        self.reset_security_answer.delete(0, "end")
        self.reset_new_password.delete(0, "end")
        self.security_question_label.configure(text="")
    
    def run(self):
        """Run the login window"""
        if self.window:
            self.window.mainloop()


def show_login_window(on_success: Callable[[AuthManager], None]):
    """Show login window and handle authentication"""
    login_window = LoginWindow(on_success)
    login_window.run()