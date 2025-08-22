# 🚀 micPlan - Quick Start Guide

## 🎯 What is micPlan?

**micPlan** is your comprehensive platform for microbial genomics planning and analysis, built with the same authentication system and structure as mictools.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test the Application
```bash
python test_app.py
```

### 3. Launch micPlan
```bash
# Option 1: Using the launcher
python run.py

# Option 2: Direct streamlit command
streamlit run app.py
```

## 🔐 Default Login Credentials

- **Admin User**: `admin` / `admin123`
- **Regular User**: `user1` / `user123`

## 📁 Project Structure

```
micPlan/
├── app/                    # Main application package
│   ├── backend/           # Backend services
│   │   ├── auth/         # Authentication system
│   │   ├── logging/      # Activity logging
│   │   └── utils/        # Backend utilities
│   ├── core/             # Core configuration
│   └── frontend/         # Frontend interface
│       ├── auth/         # Frontend authentication
│       ├── pages/        # Application pages
│       └── utils/        # Frontend utilities
├── data/                  # Data storage
├── logs/                  # Application logs
├── resources/             # Static resources
├── app.py                 # Main application file
├── config.py              # Configuration
├── run.py                 # Application launcher
└── test_app.py            # Test suite
```

## 🧪 Testing

Run the test suite to verify everything works:
```bash
python test_app.py
```

## 🔧 Configuration

Edit `config.py` to customize:
- Application settings
- Authentication parameters
- Directory paths
- Contact information

## 📚 Next Steps

1. **Customize the Home Page**: Edit `app/frontend/pages/home.py`
2. **Add New Pages**: Create new modules in `app/frontend/pages/`
3. **Extend Authentication**: Modify `app/backend/auth/user_manager.py`
4. **Add Features**: Build upon the existing structure

## 🆘 Support

- **Contact**: `kelmoussaoui@chuliege.be`
- **Documentation**: Coming soon
- **Issues**: Check the project repository

---

**Built in Liège, Belgium 🇧🇪**
