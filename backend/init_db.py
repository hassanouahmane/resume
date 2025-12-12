"""
Database initialization script
Creates the resume_db database and tables
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Get database credentials from .env
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "resume_db")

# MySQL connection string without database (to create it)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"

try:
    # Connect to MySQL server
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Create database if not exists
        print(f"Creating database '{DB_NAME}'...")
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        connection.commit()
        print(f"✅ Database '{DB_NAME}' created successfully!")
        
        # Switch to the database
        connection.execute(text(f"USE {DB_NAME}"))
        connection.commit()
        
        # Create users table
        print("Creating 'users' table...")
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) UNIQUE NOT NULL,
            full_name VARCHAR(255),
            hashed_password VARCHAR(255) NOT NULL,
            role VARCHAR(50) DEFAULT 'user' NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_role (role)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        connection.execute(text(create_users_table))
        connection.commit()
        print("✅ Table 'users' created successfully!")
        
    print("\n✅ Database initialization completed successfully!")
    print(f"Database: {DB_NAME}")
    print(f"Host: {DB_HOST}:{DB_PORT}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n⚠️  Make sure:")
    print("1. MySQL server is running")
    print("2. Credentials in .env are correct (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)")
    print("3. You have permission to create databases")
    sys.exit(1)
