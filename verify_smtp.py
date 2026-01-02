import smtplib
import os
from dotenv import load_dotenv

load_dotenv(override=True)

username = os.getenv('MAIL_USERNAME')
password = os.getenv('MAIL_PASSWORD')

print(f"Testing Login...")
print(f"Email: {username}")
print(f"Password: {password}")

try:
    # Try SSL first (Port 465)
    print("\nAttempting SSL connection (Port 465)...")
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    print("Connected. Logging in...")
    server.login(username, password)
    print("✅ SUCCESS! Credentials are valid.")
    server.quit()
except Exception as e:
    print(f"❌ SSL FAILED: {e}")
    
    # Try TLS fallback (Port 587)
    try:
        print("\nAttempting TLS connection (Port 587)...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        print("Connected. Logging in...")
        server.login(username, password)
        print("✅ SUCCESS! Credentials are valid.")
        server.quit()
    except Exception as e2:
         print(f"❌ TLS FAILED: {e2}")
