# 🌙 Dream Journal Analyzer

A unique GUI-based Python application that allows users to record their dreams and provides intelligent analysis of patterns, themes, and emotions over time. This innovative dream journaling tool combines personal reflection with data visualization and psychological insights, featuring **secure user authentication** to keep your dreams private.

## ✨ Features

### 🔐 Security & Privacy
- **User Authentication**: Secure login/signup system with password hashing
- **Private Dream Storage**: Each user has their own encrypted database
- **Password Recovery**: Security question-based password reset
- **Session Management**: Automatic logout and session expiration
- **Data Privacy**: All dreams stored locally with user-specific access

### 🎯 Core Functionality
- **Beautiful GUI**: Modern dark/light theme interface built with CustomTkinter
- **Dream Recording**: Rich text entry with metadata (mood, sleep quality, tags)
- **Intelligent Analysis**: AI-powered emotion detection, theme extraction, and sentiment analysis
- **Data Visualization**: Analytics dashboard with statistics and trends
- **Search & Filter**: Advanced search capabilities across all dream entries
- **Smart Import**: Duplicate detection and handling during dream imports
- **Export/Import**: Backup and restore dreams in JSON format

### 🧠 Advanced Analysis
- **Sentiment Analysis**: Determine emotional tone of dreams
- **Emotion Detection**: Identify specific emotions (fear, joy, sadness, etc.)
- **Theme Recognition**: Detect common dream themes (flying, water, chase, etc.)
- **Entity Extraction**: Identify people, places, colors, and objects
- **Complexity Scoring**: Measure dream narrative complexity
- **Pattern Recognition**: Track recurring elements and trends

### 📊 Analytics Dashboard
- Dream statistics and summaries
- Mood tracking over time
- Sleep quality correlations
- Lucid dream frequency
- Nightmare patterns
- Theme evolution

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup (Recommended)

1. **Download the Project Files**
   - Download all project files to a folder

2. **Run the Setup Script**
   ```bash
   python setup.py
   ```
   This will automatically:
   - Install all required dependencies
   - Download NLTK data for text analysis
   - Create desktop shortcut (Windows)
   - Launch the application

### Manual Setup

1. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download NLTK Data**
   ```bash
   python -m textblob.download_corpora
   ```

3. **Run the Application**
   ```bash
   python main_gui.py
   ```

## 📦 Dependencies

The application requires the following Python packages:

- `customtkinter==5.2.0` - Modern GUI framework
- `pillow==10.0.0` - Image processing
- `matplotlib==3.7.2` - Data visualization
- `pandas==2.0.3` - Data manipulation
- `numpy==1.24.3` - Numerical computing
- `textblob==0.17.1` - Natural language processing
- `wordcloud==1.9.2` - Word cloud generation
- `seaborn==0.12.2` - Statistical visualization
- `tkcalendar==1.6.1` - Calendar widget

## 🎮 Usage Guide

### First Time Setup

1. **Launch the Application**
   - Run `python main_gui.py`
   - The secure login window will appear

2. **Create Your Account**
   - Click the "Sign Up" tab
   - Enter username, email, and password (8+ characters)
   - Optionally set a security question for password recovery
   - Click "Create Account"

3. **Login to Your Account**
   - Switch to "Login" tab
   - Enter your username/email and password
   - Click "Login" to access your private dream journal

### Recording Dreams

1. **Dream Entry Form**
   - The app opens with the "New Dream" tab active
   - Your username is displayed in the title bar

2. **Fill in Dream Details**
   - **Title**: Give your dream a memorable title
   - **Date**: Enter dream date (YYYY-MM-DD) or leave empty for today
   - **Description**: Write your dream narrative in detail
   - **Mood Sliders**: Rate your mood before sleep, after dream, and sleep quality (1-10)
   - **Checkboxes**: Mark if it was a lucid dream, nightmare, or recurring dream
   - **Tags**: Add comma-separated tags for easy categorization

3. **Save or Analyze**
   - Click "Save Dream" to store in your private database
   - Click "Analyze Dream" for instant AI analysis
   - Click "Clear Form" to reset all fields

### Viewing Dreams

1. **Dream List Tab**
   - View all recorded dreams chronologically
   - Double-click any dream to edit
   - Use buttons to edit, delete, or refresh the list

2. **Search Tab**
   - Enter keywords to search across all dreams
   - Results show matching dreams with dates and titles

### Analytics Dashboard

1. **Statistics Overview**
   - Total dreams recorded
   - Lucid dreams count
   - Nightmare frequency
   - Average mood and sleep quality scores

2. **Trends Analysis**
   - Recent activity patterns
   - Mood trends over time
   - Sleep quality correlations

### Settings & Data Management

1. **Appearance**
   - Switch between Dark, Light, and System themes

2. **Data Export/Import**
   - Export all your dreams to JSON file for backup
   - Import dreams from JSON file with smart duplicate detection
   - Choose to update, skip, or add duplicate dreams

3. **Account Management**
   - Click "Logout" to securely exit your account
   - Password reset available via security questions

### Password Recovery

1. **Forgot Password**
   - Click "Reset Password" tab on login screen
   - Enter your username or email
   - Click "Get Security Question"
   - Answer your security question
   - Enter new password and click "Reset Password"

## 🏗️ Project Structure

```
dream-journal-analyzer/
├── main_gui.py          # Main GUI application with authentication
├── login_gui.py         # Secure login/signup interface
├── auth_manager.py      # User authentication and session management
├── database.py          # SQLite database management
├── dream_analyzer.py    # AI analysis engine
├── setup.py            # Automated setup script
├── requirements.txt     # Python dependencies
├── README.md           # This documentation
├── TEST_CASES.md       # Comprehensive testing guide
├── users.db            # User authentication database
└── dreams_user_X.db    # User-specific dream databases
```

## 🔧 Technical Details

### Security Features

- **Password Hashing**: PBKDF2 with SHA-256 and 100,000 iterations
- **Session Management**: Secure tokens with 24-hour expiration
- **Data Isolation**: Each user has a separate encrypted database
- **Input Validation**: Comprehensive validation for all user inputs

### Database Schema

The application uses multiple SQLite databases:

**User Authentication (users.db):**
1. **users**: User accounts with hashed passwords
2. **user_sessions**: Active login sessions
3. **user_preferences**: User-specific settings

**Dream Data (dreams_user_X.db):**
1. **dreams**: Core dream entries with metadata
2. **dream_analysis**: AI analysis results
3. **dream_statistics**: Aggregated statistics

### Analysis Engine

The dream analyzer uses:
- **TextBlob** for sentiment analysis and NLP
- **Keyword matching** for theme and emotion detection
- **Statistical analysis** for complexity scoring
- **Pattern recognition** for recurring elements

### GUI Framework

Built with **CustomTkinter** for:
- Modern, responsive interface
- Dark/light theme support
- Cross-platform compatibility
- Professional appearance

## 🎨 Unique Features

This Dream Journal Analyzer is unique because it:

1. **Secure & Private**: Multi-user authentication system keeps dreams completely private
2. **Combines Journaling with AI**: Unlike simple text editors, it provides intelligent analysis
3. **Focuses on Dreams**: Specialized for dream content with relevant themes and emotions
4. **Beautiful Interface**: Modern GUI that's pleasant to use daily
5. **Smart Import System**: Advanced duplicate detection prevents data duplication
6. **Comprehensive Analysis**: Multi-dimensional analysis including sentiment, themes, and complexity
7. **Data Visualization**: Transform personal dreams into meaningful insights
8. **Privacy-First**: All data stored locally with user-specific encryption, no cloud dependencies
9. **User Management**: Complete account system with password recovery

## 🔮 Future Enhancements

Potential improvements could include:
- Advanced dream pattern visualization with interactive charts
- Optional encrypted cloud backup for premium users
- Integration with sleep tracking devices and wearables
- Advanced ML models for dream interpretation
- Voice recording capabilities for dream dictation
- Dream symbol dictionary and interpretation guide
- Meditation and lucid dreaming training modules
- Dream sharing with privacy controls
- Mobile companion app

## 🐛 Troubleshooting

### Common Issues

1. **Login/Authentication Issues**
   - Ensure `users.db` has write permissions
   - Try creating a new account if login fails
   - Use password reset if you forget your password

2. **Import Errors**
   - Run the setup script: `python setup.py`
   - Manually install: `pip install -r requirements.txt`
   - Download NLTK data: `python -m textblob.download_corpora`

3. **Database Issues**
   - Check file permissions in project directory
   - Each user has their own database file
   - Logout and login again if data doesn't appear

4. **GUI Display Issues**
   - Update graphics drivers
   - Try different appearance modes in settings
   - Ensure screen resolution is at least 1000x700

5. **Analysis Errors**
   - NLTK data should auto-download on first run
   - Fallback analysis works without TextBlob
   - Check console for detailed error messages

### Getting Help

If you encounter issues:
1. Check the error message in the status bar
2. Try the automated setup script first: `python setup.py`
3. Verify all dependencies are installed
4. Ensure you have write permissions in the project directory
5. Check that your user account is properly created
6. Try logging out and back in
7. Review the comprehensive test cases in `TEST_CASES.md`

## 🧪 Testing

A comprehensive testing guide is available in [`TEST_CASES.md`](TEST_CASES.md) with:
- 7 major test categories
- 20+ detailed test scenarios
- Step-by-step instructions
- Expected results for each test
- Bug reporting template

### Quick Test Checklist
- [ ] Create new user account
- [ ] Login with credentials
- [ ] Record a dream with analysis
- [ ] Search for dreams
- [ ] Export and import data
- [ ] Test duplicate detection
- [ ] Logout securely

---

**Sweet Dreams and Secure Journaling! 🌙🔒✨**
