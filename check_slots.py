import requests
import json
import os
import sys
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class VTUSlotChecker:
    def __init__(self, username, password):
        self.base_url = "https://online.vtu.ac.in/api/v1"
        self.username = username
        self.password = password
        self.access_token = None
        self.session = requests.Session()
        
        # Set headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://online.vtu.ac.in',
            'Referer': 'https://online.vtu.ac.in/',
            'X-Requested-With': 'XMLHttpRequest'
        })
    
    def login(self):
        """Login to VTU portal"""
        def login(self):
            login_url = f"{self.base_url}/auth/login"
        
            payload = {
                "username": self.username,
                "password": self.password
            }
        
            try:
                print(f"Trying login URL: {login_url}")
        
                response = self.session.post(
                    login_url,
                    json=payload,
                    timeout=30
                )
        
                print("Status Code:", response.status_code)
                print("Response Text:", response.text)
                print("Cookies:", response.cookies.get_dict())
        
                response.raise_for_status()
        
                data = response.json()
        
                if data.get('success'):
                    cookies = response.cookies.get_dict()
                    self.access_token = cookies.get('access_token')
        
                    print(f"✓ Login successful for {self.username}")
                    return True
        
                else:
                    print(f"✗ Login failed: {data.get('message')}")
                    return False
        
            except Exception as e:
                print(f"✗ Login error: {str(e)}")
                return False
    
    def check_slots(self, course_id, exam_type=1):
        """Check for available exam slots"""
        slots_url = f"{self.base_url}/student/slots/get-enabled-dates"
        payload = {
            "course_id": course_id,
            "exam_type": exam_type
        }
        
        try:
            response = self.session.post(slots_url, json=payload, timeout=30)
            data = response.json()
            return data
        except Exception as e:
            print(f"✗ Error checking slots for course {course_id}: {str(e)}")
            return None

def send_email_alert(to_email, from_email, password, course_id, slot_data):
    """Send email alert when slots are found"""
    try:
        subject = f"🎉 VTU Exam Slots Available - Course {course_id}"
        
        # Create HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .alert-box {{ background: #4caf50; color: white; padding: 20px; 
                              border-radius: 5px; margin: 20px 0; text-align: center; font-size: 18px; }}
                .details {{ background: white; padding: 20px; border-radius: 5px; 
                           border-left: 4px solid #667eea; margin: 20px 0; }}
                .button {{ display: inline-block; background: #667eea; color: white; 
                          padding: 15px 30px; text-decoration: none; border-radius: 5px; 
                          margin: 20px 0; font-weight: bold; }}
                .timestamp {{ color: #666; font-size: 14px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; 
                       overflow-x: auto; font-size: 13px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 VTU Exam Slot Alert</h1>
                    <p>Slots are now available!</p>
                </div>
                <div class="content">
                    <div class="alert-box">
                        ✅ Exam slots are NOW AVAILABLE for Course ID {course_id}
                    </div>
                    
                    <div class="details">
                        <h3>📋 Details:</h3>
                        <p><strong>Course ID:</strong> {course_id}</p>
                        <p><strong>Time Detected:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>
                        <p><strong>Status:</strong> <span style="color: #4caf50;">AVAILABLE</span></p>
                    </div>
                    
                    <div class="details">
                        <h3>📊 Slot Data:</h3>
                        <pre>{json.dumps(slot_data, indent=2)}</pre>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="https://online.vtu.ac.in" class="button">
                            🔗 Book Your Slot Now
                        </a>
                    </div>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                        <p class="timestamp">⏰ This alert was sent automatically by your VTU Slot Monitor</p>
                        <p class="timestamp">📧 Monitoring started from GitHub Actions</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Attach HTML
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send email via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
        
        print(f"✓ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"✗ Email sending failed: {str(e)}")
        return False

def main():
    # Get credentials from environment variables
    VTU_USERNAME = os.environ.get('VTU_USERNAME')
    VTU_PASSWORD = os.environ.get('VTU_PASSWORD')
    EMAIL_TO = os.environ.get('EMAIL_TO')
    EMAIL_FROM = os.environ.get('EMAIL_FROM')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    
    # Course IDs to check (get from env or use defaults)
    COURSE_IDS = os.environ.get('COURSE_IDS', '189,18').split(',')
    COURSE_IDS = [int(x.strip()) for x in COURSE_IDS]
    
    print("=" * 60)
    print("VTU Slot Checker - GitHub Actions")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print(f"Monitoring courses: {COURSE_IDS}")
    print("=" * 60)
    
    # Validate environment variables
    if not all([VTU_USERNAME, VTU_PASSWORD, EMAIL_TO, EMAIL_FROM, EMAIL_PASSWORD]):
        print("✗ Missing required environment variables!")
        print("Required: VTU_USERNAME, VTU_PASSWORD, EMAIL_TO, EMAIL_FROM, EMAIL_PASSWORD")
        sys.exit(1)
    
    # Create checker instance
    checker = VTUSlotChecker(VTU_USERNAME, VTU_PASSWORD)
    
    # Login
    if not checker.login():
        print("✗ Failed to login. Exiting...")
        sys.exit(1)
    
    # Check each course
    slots_found = False
    
    for course_id in COURSE_IDS:
        print(f"\n--- Checking Course ID: {course_id} ---")
        result = checker.check_slots(course_id)
        
        if result:
            if result.get('success') and result.get('data'):
                # SLOTS AVAILABLE!
                print(f"🎉 SLOTS AVAILABLE for Course ID {course_id}!")
                print(f"Data: {json.dumps(result['data'], indent=2)}")
                
                # Send email
                email_sent = send_email_alert(
                    to_email=EMAIL_TO,
                    from_email=EMAIL_FROM,
                    password=EMAIL_PASSWORD,
                    course_id=course_id,
                    slot_data=result['data']
                )
                
                if email_sent:
                    slots_found = True
                    print(f"✓ Alert sent for course {course_id}")
                
            else:
                status_msg = result.get('message', 'Unknown status')
                print(f"✗ Course {course_id}: {status_msg}")
        else:
            print(f"? Course {course_id}: Failed to get response")
    
    print("\n" + "=" * 60)
    if slots_found:
        print("✓ Check completed - SLOTS FOUND and alerts sent!")
    else:
        print("✓ Check completed - No slots available yet")
    print("=" * 60)

if __name__ == "__main__":
    main()
