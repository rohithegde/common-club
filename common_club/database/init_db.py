"""
Database Initialization

Script to create database tables and seed initial data.
"""

from .base import Base
from .connection import get_common_engine
from ..models import User, SharedCategory, AppSettings
import logging

logger = logging.getLogger(__name__)


# Predefined categories to seed
PREDEFINED_CATEGORIES = [
    # Income categories (all apps)
    {"name": "Salary", "type": "income", "icon": "mdi-cash", "app_scope": "all"},
    {"name": "Bonus", "type": "income", "icon": "mdi-gift", "app_scope": "all"},
    {"name": "Freelance", "type": "income", "icon": "mdi-briefcase", "app_scope": "all"},
    {"name": "Investment Income", "type": "income", "icon": "mdi-trending-up", "app_scope": "coin"},
    {"name": "Other Income", "type": "income", "icon": "mdi-cash-plus", "app_scope": "all"},
    
    # Expense categories - Utilities
    {"name": "Utilities", "type": "expense", "icon": "mdi-lightbulb", "app_scope": "coin"},
    {"name": "Electricity", "type": "expense", "icon": "mdi-flash", "app_scope": "coin"},
    {"name": "Water", "type": "expense", "icon": "mdi-water", "app_scope": "coin"},
    {"name": "Gas", "type": "expense", "icon": "mdi-fire", "app_scope": "coin"},
    {"name": "Internet", "type": "expense", "icon": "mdi-wifi", "app_scope": "coin"},
    {"name": "Phone", "type": "expense", "icon": "mdi-phone", "app_scope": "coin"},
    
    # Expense categories - Housing
    {"name": "Housing", "type": "expense", "icon": "mdi-home", "app_scope": "coin"},
    {"name": "Rent", "type": "expense", "icon": "mdi-home-account", "app_scope": "coin"},
    {"name": "Mortgage", "type": "expense", "icon": "mdi-home-city", "app_scope": "coin"},
    {"name": "Home Insurance", "type": "expense", "icon": "mdi-shield-home", "app_scope": "coin"},
    {"name": "Property Tax", "type": "expense", "icon": "mdi-home-currency-usd", "app_scope": "coin"},
    {"name": "Maintenance", "type": "expense", "icon": "mdi-tools", "app_scope": "coin"},
    
    # Expense categories - Transportation
    {"name": "Transportation", "type": "expense", "icon": "mdi-car", "app_scope": "coin"},
    {"name": "Fuel", "type": "expense", "icon": "mdi-gas-station", "app_scope": "coin"},
    {"name": "Public Transit", "type": "expense", "icon": "mdi-bus", "app_scope": "coin"},
    {"name": "Car Insurance", "type": "expense", "icon": "mdi-shield-car", "app_scope": "coin"},
    {"name": "Car Maintenance", "type": "expense", "icon": "mdi-car-wrench", "app_scope": "coin"},
    {"name": "Parking", "type": "expense", "icon": "mdi-parking", "app_scope": "coin"},
    
    # Expense categories - Food
    {"name": "Food & Dining", "type": "expense", "icon": "mdi-food", "app_scope": "coin"},
    {"name": "Groceries", "type": "expense", "icon": "mdi-cart", "app_scope": "coin"},
    {"name": "Restaurants", "type": "expense", "icon": "mdi-silverware-fork-knife", "app_scope": "coin"},
    {"name": "Takeout", "type": "expense", "icon": "mdi-food-takeout-box", "app_scope": "coin"},
    {"name": "Coffee", "type": "expense", "icon": "mdi-coffee", "app_scope": "coin"},
    
    # Expense categories - Healthcare (cross-app)
    {"name": "Healthcare", "type": "expense", "icon": "mdi-hospital", "app_scope": "all"},
    {"name": "Medical Bills", "type": "expense", "icon": "mdi-medical-bag", "app_scope": "all"},
    {"name": "Dental", "type": "expense", "icon": "mdi-tooth", "app_scope": "all"},
    {"name": "Vision", "type": "expense", "icon": "mdi-glasses", "app_scope": "all"},
    {"name": "Pharmacy", "type": "expense", "icon": "mdi-pill", "app_scope": "all"},
    {"name": "Insurance", "type": "expense", "icon": "mdi-shield", "app_scope": "all"},
    
    # Expense categories - Entertainment
    {"name": "Entertainment", "type": "expense", "icon": "mdi-gamepad-variant", "app_scope": "coin"},
    {"name": "Movies", "type": "expense", "icon": "mdi-movie", "app_scope": "coin"},
    {"name": "Streaming Services", "type": "expense", "icon": "mdi-play-network", "app_scope": "coin"},
    {"name": "Gaming", "type": "expense", "icon": "mdi-controller", "app_scope": "coin"},
    {"name": "Books", "type": "expense", "icon": "mdi-book", "app_scope": "coin"},
    {"name": "Hobbies", "type": "expense", "icon": "mdi-palette", "app_scope": "coin"},
    
    # Expense categories - Shopping
    {"name": "Shopping", "type": "expense", "icon": "mdi-shopping", "app_scope": "coin"},
    {"name": "Clothing", "type": "expense", "icon": "mdi-tshirt-crew", "app_scope": "coin"},
    {"name": "Electronics", "type": "expense", "icon": "mdi-devices", "app_scope": "coin"},
    {"name": "Home & Garden", "type": "expense", "icon": "mdi-home-variant", "app_scope": "coin"},
    {"name": "Personal Care", "type": "expense", "icon": "mdi-face-woman", "app_scope": "coin"},
    
    # Expense categories - Education
    {"name": "Education", "type": "expense", "icon": "mdi-school", "app_scope": "all"},
    {"name": "Tuition", "type": "expense", "icon": "mdi-school", "app_scope": "all"},
    {"name": "Books & Supplies", "type": "expense", "icon": "mdi-book-open", "app_scope": "all"},
    {"name": "Courses", "type": "expense", "icon": "mdi-certificate", "app_scope": "all"},
    
    # Expense categories - Other
    {"name": "Taxes", "type": "expense", "icon": "mdi-bank", "app_scope": "coin"},
    {"name": "Gifts", "type": "expense", "icon": "mdi-gift", "app_scope": "coin"},
    {"name": "Donations", "type": "expense", "icon": "mdi-hand-heart", "app_scope": "coin"},
    {"name": "Other", "type": "expense", "icon": "mdi-dots-horizontal", "app_scope": "all"},
]


def create_tables(engine=None):
    """
    Create all database tables.
    
    Args:
        engine: SQLAlchemy engine (uses common db engine if None)
    """
    if engine is None:
        engine = get_common_engine()
    
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


def seed_predefined_categories(db_session):
    """
    Seed database with predefined categories.
    
    Args:
        db_session: Database session
    """
    logger.info("Seeding predefined categories...")
    
    # Check if categories already exist
    existing_count = db_session.query(SharedCategory).filter(
        SharedCategory.is_predefined == True
    ).count()
    
    if existing_count > 0:
        logger.info(f"Predefined categories already exist ({existing_count} found). Skipping seed.")
        return
    
    # Create predefined categories
    for cat_data in PREDEFINED_CATEGORIES:
        category = SharedCategory(
            name=cat_data["name"],
            type=cat_data["type"],
            icon=cat_data["icon"],
            app_scope=cat_data["app_scope"],
            is_predefined=True,
            user_id=None  # Predefined categories have no user
        )
        db_session.add(category)
    
    db_session.commit()
    logger.info(f"Seeded {len(PREDEFINED_CATEGORIES)} predefined categories")


def initialize_database(db_path: str = None, seed_data: bool = True):
    """
    Initialize the database with tables and optional seed data.
    
    Args:
        db_path: Path to database file (uses default if None)
        seed_data: Whether to seed predefined categories
    
    Example:
        >>> from common_club.database import initialize_database
        >>> initialize_database("./common-club.db")
    """
    from .connection import init_common_db
    
    # Initialize database connection
    engine = init_common_db(db_path)
    
    # Create tables
    create_tables(engine)
    
    # Seed data if requested
    if seed_data:
        from .connection import get_common_db
        db = next(get_common_db())
        try:
            seed_predefined_categories(db)
        finally:
            db.close()
    
    logger.info("Database initialization complete")


if __name__ == "__main__":
    # Run initialization when executed directly
    logging.basicConfig(level=logging.INFO)
    initialize_database()
