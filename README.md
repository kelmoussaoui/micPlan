# micPlan

🧬 **micPlan** is your comprehensive platform for microbial genomics planning and analysis.

## Overview

micPlan is a modular and evolving platform designed to streamline your research workflows with intuitive tools for experimental design, sample management, and data analysis — from project conception to publication-ready results.

## Features

- 🧰 **Generic Tools**: Fastp, SPAdes, BLAST, MLST, and more
- 🧬 **Pathogen-specific pipelines**: HIV, GBS, dermatophytes, and other specialized workflows
- 🧫 **Sample Management**: Upload, filter, and track sequencing data
- 📊 **Interactive Reports**: PDF generation, metadata views, and advanced filtering
- 📋 **Activity Logging**: Track all system activities and user actions
- 🔐 **Secure Authentication**: Enterprise-grade security with role-based access control

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Streamlit 1.28.0 or higher

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd micPlan
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### Default Credentials

- **Admin User**: `admin` / `admin123`
- **Regular User**: `user1` / `user123`

## Project Structure

```
micPlan/
├── app/
│   ├── backend/
│   │   ├── auth/          # Authentication system
│   │   ├── logging/       # Activity logging
│   │   └── utils/         # Backend utilities
│   ├── core/              # Core configuration
│   └── frontend/
│       ├── auth/          # Frontend authentication
│       ├── components/    # Reusable UI components
│       ├── pages/         # Application pages
│       ├── resources/     # Static resources
│       └── utils/         # Frontend utilities
├── data/                  # Data storage
├── logs/                  # Application logs
├── resources/             # Images and static files
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Development

### Adding New Pages

1. Create a new Python file in `app/frontend/pages/`
2. Implement a `run()` function
3. Add the page to the `PAGE_MAP` in `app.py`

### Adding New Tools

1. Create a new module in the appropriate directory
2. Implement the required interface
3. Update the navigation and routing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

© 2025 CHU Liège. All rights reserved.

## Contact

For questions or support, contact: `kelmoussaoui@chuliege.be`

---

**Built in Liège, Belgium 🇧🇪**
