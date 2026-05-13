import requests
import os
import sys

# These values are pulled from the hidden 'Secrets' tab, NOT the code
EMAIL = os.environ.get('VTU_EMAIL')
PASSWORD = os.environ.get('VTU_PASSWORD')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

COURSES = [
    {"id": 18, "name": "Wastewater Treatment and Recycling"}
]

def send_alert(msg):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram credentials missing!")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Failed to send Telegram: {e}")

def run_check():
    if not EMAIL or not PASSWORD:
        print("Error: VTU Credentials not found in Secrets!")
        return

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    })

    # Login Phase
    try:
        login_res = session.post("https://online.vtu.ac.in/api/v1/auth/login", 
                                 json={"email": EMAIL, "password": PASSWORD})
        
        login_data = login_res.json()
        if not login_data.get("success"):
            print(f"Login failed: {login_data.get('message')}")
            return
        
        print(f"Login successful for {login_data['data']['name']}")

        # Slot Check Phase
        for course in COURSES:
            res = session.post("https://online.vtu.ac.in/api/v1/student/slots/get-enabled-dates", 
                               json={"course_id": course['id'], "exam_type": 1})
            
            if res.status_code == 200:
                data = res.json()
                if data.get("success") and data.get("data"):
                    send_alert(f"✅ SLOTS OPEN: {course['name']} check now!")
                else:
                    print(f"Checked {course['name']}: No slots found.")
            else:
                print(f"Course {course['id']} check failed (Status {res.status_code})")

    except Exception as e:
        print(f"Script Error: {e}")

if __name__ == "__main__":
    run_check()
