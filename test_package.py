#!/usr/bin/env python3
"""
Test script for common-club package

Verifies that the package is set up correctly by:
1. Creating database and tables
2. Seeding predefined categories
3. Creating a test user
4. Testing authentication
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        from common_club import create_access_token, verify_token, get_current_user_id
        from common_club.auth import hash_password, verify_password
        from common_club.database import get_common_db, get_app_db, init_common_db
        from common_club.models import User, SharedCategory, AppSettings
        from common_club.schemas.user import UserCreate, UserLogin, UserResponse
        from common_club.schemas.category import CategoryCreate, CategoryResponse
        logger.info("✅ All imports successful")
        return True
    except Exception as e:
        logger.error(f"❌ Import failed: {e}")
        return False


def test_database_init():
    """Test database initialization."""
    logger.info("Testing database initialization...")
    
    try:
        from common_club.database.init_db import initialize_database
        
        # Initialize with test database
        test_db_path = "./test-common-club.db"
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
        
        initialize_database(test_db_path, seed_data=True)
        
        # Verify database file was created
        assert os.path.exists(test_db_path), "Database file not created"
        
        logger.info("✅ Database initialization successful")
        return True, test_db_path
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_user_creation(db_path):
    """Test creating a user."""
    logger.info("Testing user creation...")
    
    try:
        from common_club.auth import hash_password
        from common_club.models import User
        from common_club.database import init_common_db, get_common_db
        
        # Initialize with test database
        init_common_db(db_path)
        db = next(get_common_db())
        
        # Create test user
        test_user = User(
            email="test@example.com",
            password_hash=hash_password("testpassword123"),
            name="Test User"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        # Verify user was created
        user = db.query(User).filter(User.email == "test@example.com").first()
        assert user is not None, "User not found in database"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        
        logger.info(f"✅ User created successfully: {user}")
        return True, user.id
    except Exception as e:
        logger.error(f"❌ User creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None
    finally:
        db.close()


def test_authentication(user_id):
    """Test JWT token creation and verification."""
    logger.info("Testing authentication...")
    
    try:
        from common_club.auth import create_access_token, verify_token
        
        # Create token
        token = create_access_token(user_id=user_id, email="test@example.com")
        logger.info(f"Token created: {token[:50]}...")
        
        # Verify token
        payload = verify_token(token)
        assert int(payload["sub"]) == user_id
        assert payload["email"] == "test@example.com"
        
        logger.info("✅ Authentication test successful")
        return True
    except Exception as e:
        logger.error(f"❌ Authentication test failed: {e}")
        return False


def test_categories(db_path):
    """Test predefined categories."""
    logger.info("Testing categories...")
    
    try:
        from common_club.models import SharedCategory
        from common_club.database import init_common_db, get_common_db
        
        init_common_db(db_path)
        db = next(get_common_db())
        
        # Count predefined categories
        predefined = db.query(SharedCategory).filter(
            SharedCategory.is_predefined == True
        ).all()
        
        logger.info(f"Found {len(predefined)} predefined categories")
        
        # Show some examples
        coin_categories = [c for c in predefined if c.app_scope == "coin"]
        all_categories = [c for c in predefined if c.app_scope == "all"]
        
        logger.info(f"  - {len(coin_categories)} coin-specific categories")
        logger.info(f"  - {len(all_categories)} cross-app categories")
        
        # Show first 5 categories
        logger.info("Sample categories:")
        for cat in predefined[:5]:
            logger.info(f"  - {cat.name} ({cat.type}, {cat.app_scope})")
        
        assert len(predefined) > 0, "No predefined categories found"
        
        logger.info("✅ Categories test successful")
        return True
    except Exception as e:
        logger.error(f"❌ Categories test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def main():
    """Run all tests."""
    logger.info("="*60)
    logger.info("Common Club Package Test Suite")
    logger.info("="*60)
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: Database Init
    success, db_path = test_database_init()
    results.append(("Database Init", success))
    
    if not success:
        logger.error("Cannot continue without database")
        return False
    
    # Test 3: User Creation
    success, user_id = test_user_creation(db_path)
    results.append(("User Creation", success))
    
    if success and user_id:
        # Test 4: Authentication
        results.append(("Authentication", test_authentication(user_id)))
    
    # Test 5: Categories
    results.append(("Categories", test_categories(db_path)))
    
    # Summary
    logger.info("="*60)
    logger.info("Test Results Summary:")
    logger.info("="*60)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        logger.info("="*60)
        logger.info("🎉 All tests passed! Package is working correctly.")
        logger.info("="*60)
    else:
        logger.error("="*60)
        logger.error("❌ Some tests failed. Please check the errors above.")
        logger.error("="*60)
    
    # Cleanup
    if db_path and os.path.exists(db_path):
        os.remove(db_path)
        logger.info(f"Cleaned up test database: {db_path}")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
