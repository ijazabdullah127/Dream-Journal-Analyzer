import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, date
import json
import threading
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import os

from database import DreamDatabase
from dream_analyzer import DreamAnalyzer
from auth_manager import AuthManager

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DreamJournalApp:
    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.root = ctk.CTk()
        user = auth_manager.get_current_user()
        username = user['username'] if user else "Unknown User"
        self.root.title(f"Dream Journal Analyzer - {username}")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 800)
        
        # Initialize database with user-specific path
        db_path = auth_manager.get_user_database_path()
        self.db = DreamDatabase(db_path)
        self.analyzer = DreamAnalyzer()
        
        # Current dream being edited
        self.current_dream_id = None
        
        # Setup the main interface
        self.setup_main_interface()
        
        # Load initial data
        self.refresh_dream_list()
        self.update_statistics()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_main_interface(self):
        """Setup the main application interface"""
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
        # Create status bar
        self.create_status_bar()

    def create_sidebar(self):
        """Create the sidebar with navigation and statistics"""
        self.sidebar_frame = ctk.CTkFrame(self.root, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        # App title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🌙 Dream Journal", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("📝 New Dream", self.show_dream_entry),
            ("📚 Dream List", self.show_dream_list),
            ("📊 Analytics", self.show_analytics),
            ("🔍 Search", self.show_search),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for i, (text, command) in enumerate(nav_items, 1):
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.grid(row=i, column=0, padx=20, pady=10, sticky="ew")
            self.nav_buttons[text] = btn
        
        # Statistics section
        self.stats_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="📈 Quick Stats", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.stats_label.grid(row=6, column=0, padx=20, pady=(20, 10))
        
        # Stats display
        self.stats_frame = ctk.CTkFrame(self.sidebar_frame)
        self.stats_frame.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        
        self.total_dreams_label = ctk.CTkLabel(self.stats_frame, text="Total Dreams: 0")
        self.total_dreams_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.lucid_dreams_label = ctk.CTkLabel(self.stats_frame, text="Lucid Dreams: 0")
        self.lucid_dreams_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.avg_mood_label = ctk.CTkLabel(self.stats_frame, text="Avg Mood: 0.0")
        self.avg_mood_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    def create_main_content(self):
        """Create the main content area"""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create different content frames
        self.create_dream_entry_frame()
        self.create_dream_list_frame()
        self.create_analytics_frame()
        self.create_search_frame()
        self.create_settings_frame()
        
        # Show dream entry by default
        self.show_dream_entry()

    def create_dream_entry_frame(self):
        """Create the dream entry form"""
        self.dream_entry_frame = ctk.CTkFrame(self.main_frame)
        self.dream_entry_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self.dream_entry_frame, 
            text="✨ Record Your Dream", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        
        # Dream title
        ctk.CTkLabel(self.dream_entry_frame, text="Dream Title:", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, padx=20, pady=10, sticky="w"
        )
        self.dream_title_entry = ctk.CTkEntry(
            self.dream_entry_frame, 
            placeholder_text="Give your dream a title...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.dream_title_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        
        # Dream date
        ctk.CTkLabel(self.dream_entry_frame, text="Dream Date:", font=ctk.CTkFont(size=14)).grid(
            row=2, column=0, padx=20, pady=10, sticky="w"
        )
        self.dream_date_entry = ctk.CTkEntry(
            self.dream_entry_frame,
            placeholder_text="YYYY-MM-DD (leave empty for today)",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.dream_date_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        
        # Dream content
        ctk.CTkLabel(self.dream_entry_frame, text="Dream Description:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, padx=20, pady=10, sticky="nw"
        )
        self.dream_content_text = ctk.CTkTextbox(
            self.dream_entry_frame,
            height=200,
            font=ctk.CTkFont(size=12)
        )
        self.dream_content_text.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        
        # Mood and quality sliders
        sliders_frame = ctk.CTkFrame(self.dream_entry_frame)
        sliders_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        sliders_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Mood before sleep
        ctk.CTkLabel(sliders_frame, text="Mood Before Sleep:", font=ctk.CTkFont(size=12)).grid(
            row=0, column=0, padx=10, pady=5
        )
        self.mood_before_slider = ctk.CTkSlider(sliders_frame, from_=1, to=10, number_of_steps=9)
        self.mood_before_slider.set(5)
        self.mood_before_slider.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.mood_before_label = ctk.CTkLabel(sliders_frame, text="5")
        self.mood_before_label.grid(row=2, column=0, padx=10, pady=5)
        self.mood_before_slider.configure(command=lambda v: self.mood_before_label.configure(text=f"{int(v)}"))
        
        # Mood after dream
        ctk.CTkLabel(sliders_frame, text="Mood After Dream:", font=ctk.CTkFont(size=12)).grid(
            row=0, column=1, padx=10, pady=5
        )
        self.mood_after_slider = ctk.CTkSlider(sliders_frame, from_=1, to=10, number_of_steps=9)
        self.mood_after_slider.set(5)
        self.mood_after_slider.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.mood_after_label = ctk.CTkLabel(sliders_frame, text="5")
        self.mood_after_label.grid(row=2, column=1, padx=10, pady=5)
        self.mood_after_slider.configure(command=lambda v: self.mood_after_label.configure(text=f"{int(v)}"))
        
        # Sleep quality
        ctk.CTkLabel(sliders_frame, text="Sleep Quality:", font=ctk.CTkFont(size=12)).grid(
            row=0, column=2, padx=10, pady=5
        )
        self.sleep_quality_slider = ctk.CTkSlider(sliders_frame, from_=1, to=10, number_of_steps=9)
        self.sleep_quality_slider.set(5)
        self.sleep_quality_slider.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        self.sleep_quality_label = ctk.CTkLabel(sliders_frame, text="5")
        self.sleep_quality_label.grid(row=2, column=2, padx=10, pady=5)
        self.sleep_quality_slider.configure(command=lambda v: self.sleep_quality_label.configure(text=f"{int(v)}"))
        
        # Checkboxes
        checkbox_frame = ctk.CTkFrame(self.dream_entry_frame)
        checkbox_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        self.lucid_var = ctk.BooleanVar()
        self.nightmare_var = ctk.BooleanVar()
        self.recurring_var = ctk.BooleanVar()
        
        ctk.CTkCheckBox(checkbox_frame, text="Lucid Dream", variable=self.lucid_var).grid(
            row=0, column=0, padx=20, pady=10
        )
        ctk.CTkCheckBox(checkbox_frame, text="Nightmare", variable=self.nightmare_var).grid(
            row=0, column=1, padx=20, pady=10
        )
        ctk.CTkCheckBox(checkbox_frame, text="Recurring Dream", variable=self.recurring_var).grid(
            row=0, column=2, padx=20, pady=10
        )
        
        # Tags entry
        ctk.CTkLabel(self.dream_entry_frame, text="Tags (comma-separated):", font=ctk.CTkFont(size=14)).grid(
            row=6, column=0, padx=20, pady=10, sticky="w"
        )
        self.tags_entry = ctk.CTkEntry(
            self.dream_entry_frame,
            placeholder_text="flying, water, family, scary...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.tags_entry.grid(row=6, column=1, padx=20, pady=10, sticky="ew")
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dream_entry_frame)
        button_frame.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        self.save_button = ctk.CTkButton(
            button_frame,
            text="💾 Save Dream",
            command=self.save_dream,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.save_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.analyze_button = ctk.CTkButton(
            button_frame,
            text="🔍 Analyze Dream",
            command=self.analyze_current_dream,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.analyze_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear Form",
            command=self.clear_dream_form,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.clear_button.grid(row=0, column=2, padx=10, pady=10)

    def create_dream_list_frame(self):
        """Create the dream list view"""
        self.dream_list_frame = ctk.CTkFrame(self.main_frame)
        self.dream_list_frame.grid_columnconfigure(0, weight=1)
        self.dream_list_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self.dream_list_frame, 
            text="📚 Your Dream Collection", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Dream list with scrollbar
        self.dream_listbox = tk.Listbox(
            self.dream_list_frame,
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="white",
            selectbackground="#1f538d",
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0
        )
        
        scrollbar = tk.Scrollbar(self.dream_list_frame, orient="vertical")
        self.dream_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.dream_listbox.yview)
        
        self.dream_listbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns", pady=10)
        
        # Bind double-click to edit dream
        self.dream_listbox.bind("<Double-Button-1>", self.edit_selected_dream)
        
        # Buttons
        list_button_frame = ctk.CTkFrame(self.dream_list_frame)
        list_button_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        ctk.CTkButton(
            list_button_frame,
            text="✏️ Edit Selected",
            command=self.edit_selected_dream,
            height=40
        ).grid(row=0, column=0, padx=10, pady=10)
        
        ctk.CTkButton(
            list_button_frame,
            text="🗑️ Delete Selected",
            command=self.delete_selected_dream,
            height=40
        ).grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkButton(
            list_button_frame,
            text="🔄 Refresh List",
            command=self.refresh_dream_list,
            height=40
        ).grid(row=0, column=2, padx=10, pady=10)

    def create_analytics_frame(self):
        """Create the analytics dashboard"""
        self.analytics_frame = ctk.CTkFrame(self.main_frame)
        self.analytics_frame.grid_columnconfigure(0, weight=1)
        self.analytics_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self.analytics_frame, 
            text="📊 Dream Analytics Dashboard", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Analytics content will be populated when shown
        self.analytics_content = ctk.CTkFrame(self.analytics_frame)
        self.analytics_content.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    def create_search_frame(self):
        """Create the search interface"""
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_rowconfigure(2, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self.search_frame, 
            text="🔍 Search Your Dreams", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Search controls
        search_controls = ctk.CTkFrame(self.search_frame)
        search_controls.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        search_controls.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(search_controls, text="Search:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, padx=10, pady=10
        )
        
        self.search_entry = ctk.CTkEntry(
            search_controls,
            placeholder_text="Enter keywords to search...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkButton(
            search_controls,
            text="🔍 Search",
            command=self.perform_search,
            height=40
        ).grid(row=0, column=2, padx=10, pady=10)
        
        # Search results
        self.search_results = tk.Listbox(
            self.search_frame,
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="white",
            selectbackground="#1f538d",
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0
        )
        self.search_results.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    def create_settings_frame(self):
        """Create the settings interface"""
        self.settings_frame = ctk.CTkFrame(self.main_frame)
        
        # Title
        title_label = ctk.CTkLabel(
            self.settings_frame, 
            text="⚙️ Settings", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Settings content
        settings_content = ctk.CTkFrame(self.settings_frame)
        settings_content.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Theme selection
        ctk.CTkLabel(settings_content, text="Appearance Mode:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, padx=20, pady=10, sticky="w"
        )
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            settings_content,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_menu.grid(row=0, column=1, padx=20, pady=10)
        
        # Export/Import buttons
        ctk.CTkButton(
            settings_content,
            text="📤 Export Dreams",
            command=self.export_dreams,
            height=40
        ).grid(row=1, column=0, padx=20, pady=10)
        
        ctk.CTkButton(
            settings_content,
            text="📥 Import Dreams",
            command=self.import_dreams,
            height=40
        ).grid(row=1, column=1, padx=20, pady=10)
        
        # Logout button
        ctk.CTkButton(
            settings_content,
            text="🚪 Logout",
            command=self.logout,
            height=40,
            fg_color="red",
            hover_color="darkred"
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = ctk.CTkFrame(self.root, height=30)
        self.status_bar.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 20))
        
        self.status_label = ctk.CTkLabel(
            self.status_bar, 
            text="Ready", 
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def show_dream_entry(self):
        """Show the dream entry form"""
        self.hide_all_frames()
        self.dream_entry_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.highlight_nav_button("📝 New Dream")

    def show_dream_list(self):
        """Show the dream list"""
        self.hide_all_frames()
        self.dream_list_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.highlight_nav_button("📚 Dream List")
        self.refresh_dream_list()

    def show_analytics(self):
        """Show the analytics dashboard"""
        self.hide_all_frames()
        self.analytics_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.highlight_nav_button("📊 Analytics")
        self.load_analytics()

    def show_search(self):
        """Show the search interface"""
        self.hide_all_frames()
        self.search_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.highlight_nav_button("🔍 Search")

    def show_settings(self):
        """Show the settings interface"""
        self.hide_all_frames()
        self.settings_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.highlight_nav_button("⚙️ Settings")

    def hide_all_frames(self):
        """Hide all content frames"""
        for frame in [self.dream_entry_frame, self.dream_list_frame, 
                     self.analytics_frame, self.search_frame, self.settings_frame]:
            frame.grid_remove()

    def highlight_nav_button(self, button_text):
        """Highlight the active navigation button"""
        for text, button in self.nav_buttons.items():
            if text == button_text:
                button.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            else:
                button.configure(fg_color=("#3a7ebf", "#1f538d"))

    def save_dream(self):
        """Save the current dream entry"""
        try:
            # Get form data
            title = self.dream_title_entry.get().strip()
            content = self.dream_content_text.get("1.0", "end-1c").strip()
            
            if not title or not content:
                messagebox.showerror("Error", "Please fill in both title and content!")
                return
            
            # Parse date
            date_str = self.dream_date_entry.get().strip()
            if date_str:
                try:
                    dream_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                    return
            else:
                dream_date = date.today()
            
            # Parse tags
            tags_str = self.tags_entry.get().strip()
            tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()] if tags_str else []
            
            # Create dream data
            dream_data = {
                'title': title,
                'content': content,
                'date_recorded': date.today(),
                'dream_date': dream_date,
                'mood_before': int(self.mood_before_slider.get()),
                'mood_after': int(self.mood_after_slider.get()),
                'sleep_quality': int(self.sleep_quality_slider.get()),
                'lucid_dream': self.lucid_var.get(),
                'nightmare': self.nightmare_var.get(),
                'recurring': self.recurring_var.get(),
                'tags': tags
            }
            
            # Save to database
            if self.current_dream_id:
                success = self.db.update_dream(self.current_dream_id, dream_data)
                if success:
                    messagebox.showinfo("Success", "Dream updated successfully!")
                    self.current_dream_id = None
                else:
                    messagebox.showerror("Error", "Failed to update dream!")
            else:
                dream_id = self.db.add_dream(dream_data)
                if dream_id:
                    messagebox.showinfo("Success", "Dream saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save dream!")
            
            # Clear form and refresh
            self.clear_dream_form()
            self.update_statistics()
            self.update_status("Dream saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def analyze_current_dream(self):
        """Analyze the current dream content"""
        title = self.dream_title_entry.get().strip()
        content = self.dream_content_text.get("1.0", "end-1c").strip()
        
        if not content:
            messagebox.showerror("Error", "Please enter dream content to analyze!")
            return
        
        try:
            # Show loading message
            self.update_status("Analyzing dream...")
            
            # Perform analysis in a separate thread to avoid blocking UI
            def analyze():
                analysis = self.analyzer.analyze_dream(content, title)
                insights = self.analyzer.generate_insights(analysis)
                
                # Show results in a new window
                self.root.after(0, lambda: self.show_analysis_results(analysis, insights))
            
            threading.Thread(target=analyze, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            self.update_status("Analysis failed")

    def show_analysis_results(self, analysis: Dict, insights: List[str]):
        """Show analysis results in a popup window"""
        result_window = ctk.CTkToplevel(self.root)
        result_window.title("Dream Analysis Results")
        result_window.geometry("800x600")
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(result_window)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            scrollable_frame, 
            text="🔍 Dream Analysis Results", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Insights section
        insights_label = ctk.CTkLabel(
            scrollable_frame, 
            text="💡 Key Insights", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        insights_label.pack(pady=(20, 10), anchor="w")
        
        for insight in insights:
            insight_label = ctk.CTkLabel(
                scrollable_frame, 
                text=f"• {insight}", 
                font=ctk.CTkFont(size=12),
                wraplength=700,
                justify="left"
            )
            insight_label.pack(pady=2, anchor="w")
        
        # Detailed analysis sections
        sections = [
            ("🎭 Sentiment Analysis", analysis['sentiment_analysis']),
            ("😊 Emotion Analysis", analysis['emotion_analysis']),
            ("🎨 Theme Analysis", analysis['theme_analysis']),
            ("📊 Complexity Analysis", analysis['complexity_score'])
        ]
        
        for section_title, section_data in sections:
            section_label = ctk.CTkLabel(
                scrollable_frame, 
                text=section_title, 
                font=ctk.CTkFont(size=16, weight="bold")
            )
            section_label.pack(pady=(20, 10), anchor="w")
            
            # Format section data
            formatted_data = self.format_analysis_section(section_data)
            data_label = ctk.CTkLabel(
                scrollable_frame, 
                text=formatted_data, 
                font=ctk.CTkFont(size=12),
                wraplength=700,
                justify="left"
            )
            data_label.pack(pady=2, anchor="w")
        
        self.update_status("Analysis complete")

    def format_analysis_section(self, data: Dict) -> str:
        """Format analysis data for display"""
        if isinstance(data, dict):
            formatted = []
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    formatted.append(f"{key.replace('_', ' ').title()}: {value}")
                elif isinstance(value, str):
                    formatted.append(f"{key.replace('_', ' ').title()}: {value}")
                elif isinstance(value, list) and value:
                    formatted.append(f"{key.replace('_', ' ').title()}: {', '.join(value)}")
            return "\n".join(formatted)
        return str(data)

    def clear_dream_form(self):
        """Clear all form fields"""
        self.dream_title_entry.delete(0, "end")
        self.dream_date_entry.delete(0, "end")
        self.dream_content_text.delete("1.0", "end")
        self.tags_entry.delete(0, "end")
        
        # Reset sliders
        self.mood_before_slider.set(5)
        self.mood_after_slider.set(5)
        self.sleep_quality_slider.set(5)
        
        # Reset checkboxes
        self.lucid_var.set(False)
        self.nightmare_var.set(False)
        self.recurring_var.set(False)
        
        # Reset current dream ID
        self.current_dream_id = None
        
        # Update button text
        self.save_button.configure(text="💾 Save Dream")

    def refresh_dream_list(self):
        """Refresh the dream list"""
        try:
            self.dream_listbox.delete(0, "end")
            dreams = self.db.get_all_dreams(limit=100)  # Limit for performance
            
            for dream in dreams:
                date_str = dream['date_recorded']
                title = dream['title'][:50] + "..." if len(dream['title']) > 50 else dream['title']
                display_text = f"{date_str} - {title}"
                self.dream_listbox.insert("end", display_text)
            
            self.update_status(f"Loaded {len(dreams)} dreams")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dreams: {str(e)}")

    def edit_selected_dream(self, event=None):
        """Edit the selected dream"""
        try:
            selection = self.dream_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a dream to edit!")
                return
            
            # Get all dreams and find the selected one
            dreams = self.db.get_all_dreams(limit=100)
            selected_index = selection[0]
            
            if selected_index >= len(dreams):
                messagebox.showerror("Error", "Invalid selection!")
                return
            
            dream = dreams[selected_index]
            
            # Populate form with dream data
            self.dream_title_entry.delete(0, "end")
            self.dream_title_entry.insert(0, dream['title'])
            
            self.dream_date_entry.delete(0, "end")
            self.dream_date_entry.insert(0, str(dream['dream_date']))
            
            self.dream_content_text.delete("1.0", "end")
            self.dream_content_text.insert("1.0", dream['content'])
            
            self.tags_entry.delete(0, "end")
            if dream['tags']:
                self.tags_entry.insert(0, ", ".join(dream['tags']))
            
            # Set sliders
            self.mood_before_slider.set(dream['mood_before'] or 5)
            self.mood_after_slider.set(dream['mood_after'] or 5)
            self.sleep_quality_slider.set(dream['sleep_quality'] or 5)
            
            # Set checkboxes
            self.lucid_var.set(dream['lucid_dream'] or False)
            self.nightmare_var.set(dream['nightmare'] or False)
            self.recurring_var.set(dream['recurring'] or False)
            
            # Set current dream ID for updating
            self.current_dream_id = dream['id']
            
            # Update button text
            self.save_button.configure(text="💾 Update Dream")
            
            # Switch to dream entry view
            self.show_dream_entry()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dream: {str(e)}")

    def delete_selected_dream(self):
        """Delete the selected dream"""
        try:
            selection = self.dream_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a dream to delete!")
                return
            
            # Confirm deletion
            if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this dream?"):
                return
            
            # Get all dreams and find the selected one
            dreams = self.db.get_all_dreams(limit=100)
            selected_index = selection[0]
            
            if selected_index >= len(dreams):
                messagebox.showerror("Error", "Invalid selection!")
                return
            
            dream = dreams[selected_index]
            
            # Delete from database
            if self.db.delete_dream(dream['id']):
                messagebox.showinfo("Success", "Dream deleted successfully!")
                self.refresh_dream_list()
                self.update_statistics()
            else:
                messagebox.showerror("Error", "Failed to delete dream!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete dream: {str(e)}")

    def perform_search(self):
        """Perform search based on user input"""
        try:
            search_term = self.search_entry.get().strip()
            if not search_term:
                messagebox.showwarning("Warning", "Please enter a search term!")
                return
            
            # Clear previous results
            self.search_results.delete(0, "end")
            
            # Perform search
            results = self.db.search_dreams(search_term)
            
            if not results:
                self.search_results.insert("end", "No dreams found matching your search.")
                return
            
            # Display results
            for dream in results:
                date_str = dream['date_recorded']
                title = dream['title'][:40] + "..." if len(dream['title']) > 40 else dream['title']
                display_text = f"{date_str} - {title}"
                self.search_results.insert("end", display_text)
            
            self.update_status(f"Found {len(results)} matching dreams")
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def load_analytics(self):
        """Load and display analytics"""
        try:
            # Clear previous analytics
            for widget in self.analytics_content.winfo_children():
                widget.destroy()
            
            # Get statistics
            stats = self.db.get_statistics()
            trends = self.db.get_dream_trends(30)
            
            # Create analytics widgets
            self.create_analytics_widgets(stats, trends)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load analytics: {str(e)}")

    def create_analytics_widgets(self, stats: Dict, trends: Dict):
        """Create analytics visualization widgets"""
        # Statistics summary
        stats_frame = ctk.CTkFrame(self.analytics_content)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            stats_frame,
            text="📈 Dream Statistics",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(fill="x", padx=20, pady=10)
        
        # Create stat labels
        stat_items = [
            ("Total Dreams", stats['total_dreams']),
            ("Lucid Dreams", stats['lucid_dreams']),
            ("Nightmares", stats['nightmares']),
            ("Recurring Dreams", stats['recurring_dreams']),
            ("Avg Mood Before", f"{stats['avg_mood_before']:.1f}"),
            ("Avg Mood After", f"{stats['avg_mood_after']:.1f}"),
            ("Avg Sleep Quality", f"{stats['avg_sleep_quality']:.1f}")
        ]
        
        for i, (label, value) in enumerate(stat_items):
            row = i // 3
            col = i % 3
            
            stat_widget = ctk.CTkFrame(stats_grid)
            stat_widget.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(stat_widget, text=str(value), font=ctk.CTkFont(size=24, weight="bold")).pack()
            ctk.CTkLabel(stat_widget, text=label, font=ctk.CTkFont(size=12)).pack()
        
        # Configure grid weights
        for i in range(3):
            stats_grid.grid_columnconfigure(i, weight=1)
        
        # Trends visualization (simplified text-based for now)
        if trends['dates']:
            trends_frame = ctk.CTkFrame(self.analytics_content)
            trends_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                trends_frame,
                text="📊 Recent Trends (Last 30 Days)",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(pady=10)
            
            # Simple trend summary
            total_recent = sum(trends['dream_counts'])
            avg_mood = sum(trends['avg_moods']) / len(trends['avg_moods']) if trends['avg_moods'] else 0
            
            trend_text = f"Dreams recorded: {total_recent}\nAverage mood: {avg_mood:.1f}"
            
            ctk.CTkLabel(
                trends_frame,
                text=trend_text,
                font=ctk.CTkFont(size=14)
            ).pack(pady=10)

    def update_statistics(self):
        """Update the sidebar statistics"""
        try:
            stats = self.db.get_statistics()
            
            self.total_dreams_label.configure(text=f"Total Dreams: {stats['total_dreams']}")
            self.lucid_dreams_label.configure(text=f"Lucid Dreams: {stats['lucid_dreams']}")
            self.avg_mood_label.configure(text=f"Avg Mood: {stats['avg_mood_after']:.1f}")
            
        except Exception as e:
            print(f"Failed to update statistics: {e}")

    def update_status(self, message: str):
        """Update the status bar message"""
        self.status_label.configure(text=message)

    def change_appearance_mode(self, new_appearance_mode: str):
        """Change the appearance mode"""
        ctk.set_appearance_mode(new_appearance_mode.lower())

    def export_dreams(self):
        """Export dreams to JSON file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
            
            dreams = self.db.get_all_dreams()
            
            # Convert dates to strings for JSON serialization
            for dream in dreams:
                for key, value in dream.items():
                    if isinstance(value, date):
                        dream[key] = str(value)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(dreams, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Dreams exported to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

    def import_dreams(self):
        """Import dreams from JSON file with duplicate checking"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                dreams = json.load(f)
            
            imported_count = 0
            updated_count = 0
            skipped_count = 0
            
            # Show progress dialog
            progress_window = ctk.CTkToplevel(self.root)
            progress_window.title("Importing Dreams")
            progress_window.geometry("400x200")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            progress_label = ctk.CTkLabel(progress_window, text="Processing dreams...")
            progress_label.pack(pady=20)
            
            progress_bar = ctk.CTkProgressBar(progress_window, width=300)
            progress_bar.pack(pady=10)
            progress_bar.set(0)
            
            status_label = ctk.CTkLabel(progress_window, text="")
            status_label.pack(pady=10)
            
            total_dreams = len(dreams)
            
            for i, dream_data in enumerate(dreams):
                try:
                    # Update progress
                    progress = (i + 1) / total_dreams
                    progress_bar.set(progress)
                    status_label.configure(text=f"Processing dream {i + 1} of {total_dreams}")
                    progress_window.update()
                    
                    # Convert string dates back to date objects
                    if 'date_recorded' in dream_data:
                        dream_data['date_recorded'] = datetime.strptime(dream_data['date_recorded'], '%Y-%m-%d').date()
                    if 'dream_date' in dream_data:
                        dream_data['dream_date'] = datetime.strptime(dream_data['dream_date'], '%Y-%m-%d').date()
                    
                    # Check for duplicate based on title, content, and dream_date
                    existing_dream = self.find_duplicate_dream(dream_data)
                    
                    if existing_dream:
                        # Ask user what to do with duplicate
                        choice = self.ask_duplicate_action(dream_data['title'], existing_dream['id'])
                        
                        if choice == "update":
                            # Update existing dream
                            dream_data_copy = dream_data.copy()
                            if 'id' in dream_data_copy:
                                del dream_data_copy['id']
                            
                            if self.db.update_dream(existing_dream['id'], dream_data_copy):
                                updated_count += 1
                            else:
                                skipped_count += 1
                        elif choice == "skip":
                            skipped_count += 1
                        else:  # "add_anyway"
                            # Remove ID to avoid conflicts and add as new
                            if 'id' in dream_data:
                                del dream_data['id']
                            
                            if self.db.add_dream(dream_data):
                                imported_count += 1
                            else:
                                skipped_count += 1
                    else:
                        # No duplicate found, add as new dream
                        if 'id' in dream_data:
                            del dream_data['id']
                        
                        if self.db.add_dream(dream_data):
                            imported_count += 1
                        else:
                            skipped_count += 1
                    
                except Exception as e:
                    print(f"Failed to import dream: {e}")
                    skipped_count += 1
                    continue
            
            # Close progress window
            progress_window.destroy()
            
            # Show results
            result_message = f"Import completed!\n\n"
            result_message += f"New dreams imported: {imported_count}\n"
            result_message += f"Existing dreams updated: {updated_count}\n"
            result_message += f"Dreams skipped: {skipped_count}\n"
            result_message += f"Total processed: {total_dreams}"
            
            messagebox.showinfo("Import Results", result_message)
            self.refresh_dream_list()
            self.update_statistics()
            
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {str(e)}")
    
    def find_duplicate_dream(self, dream_data: Dict) -> Optional[Dict]:
        """Find duplicate dream based on title, content, and date"""
        try:
            # Search for dreams with same title and date
            existing_dreams = self.db.get_all_dreams()
            
            for existing in existing_dreams:
                # Check if title and dream_date match
                if (existing['title'].lower().strip() == dream_data.get('title', '').lower().strip() and
                    str(existing['dream_date']) == str(dream_data.get('dream_date', ''))):
                    
                    # Also check if content is very similar (first 100 characters)
                    existing_content = existing['content'][:100].lower().strip()
                    new_content = dream_data.get('content', '')[:100].lower().strip()
                    
                    if existing_content == new_content:
                        return existing
            
            return None
            
        except Exception as e:
            print(f"Error finding duplicate: {e}")
            return None
    
    def ask_duplicate_action(self, dream_title: str, existing_id: int) -> str:
        """Ask user what to do with duplicate dream"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Duplicate Dream Found")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"500x300+{x}+{y}")
        
        result = {"action": "skip"}  # Default action
        
        # Message
        message_label = ctk.CTkLabel(
            dialog,
            text=f"A dream with similar title and date already exists:\n\n'{dream_title}'\n\nWhat would you like to do?",
            font=ctk.CTkFont(size=14),
            wraplength=450
        )
        message_label.pack(pady=20)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=20)
        
        def set_action(action):
            result["action"] = action
            dialog.destroy()
        
        # Update button
        update_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Update Existing",
            command=lambda: set_action("update"),
            width=120,
            height=40
        )
        update_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Skip button
        skip_btn = ctk.CTkButton(
            button_frame,
            text="⏭️ Skip This Dream",
            command=lambda: set_action("skip"),
            width=120,
            height=40
        )
        skip_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Add anyway button
        add_btn = ctk.CTkButton(
            button_frame,
            text="➕ Add Anyway",
            command=lambda: set_action("add_anyway"),
            width=120,
            height=40
        )
        add_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Wait for user choice
        dialog.wait_window()
        
        return result["action"]
    
    def logout(self):
        """Logout current user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.auth_manager.logout()
            self.root.destroy()
            # Restart the application with login screen
            from login_gui import show_login_window
            show_login_window(lambda auth: DreamJournalApp(auth).run())
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit Dream Journal Analyzer?"):
            self.auth_manager.logout()
            self.root.destroy()

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main function to run the application"""
    # Show login window first
    from login_gui import show_login_window
    
    def on_login_success(auth_manager: AuthManager):
        app = DreamJournalApp(auth_manager)
        app.run()
    
    show_login_window(on_login_success)


if __name__ == "__main__":
    main()