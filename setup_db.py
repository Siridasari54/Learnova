"""
Learnova Database Setup Script
Run this AFTER starting XAMPP MySQL:
  python setup_db.py
"""
import pymysql

HOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWORD = ''

try:
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS learnova_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    cursor.execute("SHOW DATABASES;")
    databases = [db[0] for db in cursor.fetchall()]
    if 'learnova_db' in databases:
        print("✅ Database 'learnova_db' is ready!")
    else:
        print("❌ Failed to create database.")
    cursor.close()
    conn.close()
    print("\n🚀 Next steps:")
    print("   python manage.py migrate")
    print("   python manage.py createsuperuser")
    print("   python manage.py runserver")
except Exception as e:
    print(f"❌ Could not connect to MySQL: {e}")
    print("\n⚠️  Make sure XAMPP is running and MySQL service is started.")
    print("    Open XAMPP Control Panel and click 'Start' next to MySQL.")
