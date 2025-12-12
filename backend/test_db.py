"""Quick test script to check database connection and signup"""
import sys
import traceback

sys.path.insert(0, 'c:\\Users\\hassa\\Desktop\\resume\\backend')

try:
    from app.core.database import get_db, engine
    from app.models.user import User
    from sqlalchemy import inspect
    
    print("✅ Imports successful")
    
    # Check database connection
    print("\nTesting database connection...")
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ Database connected")
    
    # Check tables
    print("\nChecking tables...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")
    
    if 'users' in tables:
        print("✅ 'users' table exists")
        columns = inspector.get_columns('users')
        print(f"Columns: {[col['name'] for col in columns]}")
    else:
        print("❌ 'users' table NOT found")
    
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
    sys.exit(1)
