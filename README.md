# Common Club - Shared Services for Club Apps

Shared backend utilities, authentication, and common data management for all club applications (coin-club, care-club, career-club, campfire-club, etc.).

## Features

- 🔐 **JWT Authentication** - Secure user authentication across all club apps
- 🗄️ **Database Management** - SQLite database utilities and migrations
- 📊 **Shared Categories** - Common categories usable across all apps
- 🔄 **Data Sync** - Utilities for syncing data across apps
- 🛡️ **Security Utilities** - Password hashing, token management
- 📦 **Base Models** - Reusable SQLAlchemy models
- 🎨 **Common Schemas** - Pydantic schemas for validation

## Installation

### From PyPI (when published)
```bash
pip install common-club
```

### From Source (Development)
```bash
git clone https://github.com/yourusername/common-club.git
cd common-club
pip install -e .
```

## Usage in Club Apps

### 1. Authentication
```python
from common_club.auth import create_access_token, verify_token, get_current_user
from fastapi import Depends

@app.post("/login")
async def login(credentials: LoginSchema):
    token = create_access_token(user_id=user.id)
    return {"access_token": token}

@app.get("/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {"user": current_user}
```

### 2. Database Setup
```python
from common_club.database import CommonDatabase, get_app_database

# Get common database connection
common_db = CommonDatabase("~/ClubApps/data/common-club.db")

# Get app-specific database
app_db = get_app_database("coin-club", "~/ClubApps/data/coin-club.db")
```

### 3. Shared Categories
```python
from common_club.services import CategoryService

# Get categories for specific app
categories = CategoryService.get_categories_for_app(
    db=common_db,
    app_name="coin-club",
    user_id=current_user.id
)
```

## Database Structure

### common-club.db
- `users` - User accounts (shared across all apps)
- `shared_categories` - Predefined and user-created categories
- `app_settings` - Settings for each club app
- `sync_metadata` - Track installed apps and sync status

### {app-name}-club.db
- App-specific tables
- References common-club.db for users and categories

## Architecture

```
┌─────────────────────────────────────────────────┐
│           common-club (Python Package)          │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │   Auth   │  │ Database │  │   Services   │  │
│  │          │  │  Utils   │  │  (Category,  │  │
│  │  - JWT   │  │          │  │   Settings)  │  │
│  │  - Hash  │  │ - SQLite │  │              │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │         common-club.db                   │   │
│  │  users | shared_categories | settings    │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
           │              │              │
           ▼              ▼              ▼
    ┌───────────┐  ┌───────────┐  ┌───────────┐
    │coin-club  │  │care-club  │  │career-club│
    │  + API    │  │  + API    │  │  + API    │
    │  + DB     │  │  + DB     │  │  + DB     │
    └───────────┘  └───────────┘  └───────────┘
```

## Google Drive Backup

All databases are stored in `~/ClubApps/data/` which can be symlinked to Google Drive for automatic backup:

```bash
# Link data folder to Google Drive
ln -s ~/ClubApps/data ~/Google\ Drive/ClubApps-Backup
```

Or use the built-in backup service:

```python
from common_club.backup import BackupService

backup = BackupService(
    data_dir="~/ClubApps/data",
    backup_dir="~/Google Drive/ClubApps-Backup"
)
backup.create_backup()  # Creates timestamped backup of all .db files
```

## Development

```bash
# Setup development environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black common_club/
flake8 common_club/
```

## License

MIT License
