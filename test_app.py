#!/usr/bin/env python3
# test_app.py
# Test script for micPlan

def test_imports():
    """Test that all modules can be imported"""
    try:
        print("🧪 Testing micPlan imports...")
        
        # Test main modules
        import app
        print("✅ Main app module imported")
        
        import app.frontend.pages.home
        print("✅ Home page module imported")
        
        import app.frontend.auth.secure_auth
        print("✅ Authentication module imported")
        
        import app.backend.auth.user_manager
        print("✅ User manager module imported")
        
        import app.backend.logging.logger
        print("✅ Logging module imported")
        
        import app.frontend.utils.utils
        print("✅ Utils module imported")
        
        print("\n🎉 All imports successful! micPlan is ready to run.")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        print("\n⚙️ Testing configuration...")
        
        import config
        print(f"✅ Configuration loaded: {config.APP_NAME} v{config.APP_VERSION}")
        print(f"✅ Contact: {config.CONTACT_EMAIL}")
        print(f"✅ Institution: {config.INSTITUTION}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧬 micPlan Test Suite")
    print("=" * 40)
    
    success = True
    
    # Run tests
    if not test_imports():
        success = False
    
    if not test_config():
        success = False
    
    # Summary
    print("\n" + "=" * 40)
    if success:
        print("🎉 All tests passed! micPlan is ready to launch.")
        print("\n🚀 To start micPlan, run:")
        print("   python run.py")
        print("   or")
        print("   streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
