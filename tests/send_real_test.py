# tests/send_real_test.py - Send REAL test email with privacy policy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

print("🚀 SENDING REAL TEST EMAIL TO YOUR EXTENSION")
print("=" * 60)

def create_privacy_policy():
    """Create a real privacy policy XML"""
    policy_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<PrivacyPolicy xmlns="urn:email:privacy:1.0" version="1.0">
  <Metadata>
    <Creator>security@company.com</Creator>
    <Created>2025-01-16T12:00:00Z</Created>
  </Metadata>
  <Rules>
    <Rule id="block-tracking-1" priority="1">
      <Description>Remove tracking pixels</Description>
      <Condition>
        <XPath>.//img[contains(@src, 'tracker') or contains(@src, 'analytics')]</XPath>
      </Condition>
      <Action type="strip" message="Tracking pixel detected and removed"/>
      <Scope phase="at-use"/>
    </Rule>
    <Rule id="no-forward-1" priority="1">
      <Description>Warn about forwarding attempts</Description>
      <Condition>
        <XPath>.//header[@name='Received'] | .//header[@name='Resent-From']</XPath>
      </Condition>
      <Action type="warn" message="This confidential email should not be forwarded"/>
      <Scope phase="at-use"/>
    </Rule>
  </Rules>
</PrivacyPolicy>'''
    
    encoded_policy = base64.b64encode(policy_xml.encode('utf-8')).decode('utf-8')
    print("📄 Created privacy policy with 2 security rules")
    return encoded_policy

def send_real_email():
    """Send a REAL test email with privacy policy"""
    
    # ========== CONFIGURE THESE SETTINGS ==========
    YOUR_EMAIL = "c24439361@gmail.com"  
    APP_PASSWORD = "sajz qtbt suxi idsw"  
    # ==============================================
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    print("🛡️ SENDING REAL TEST EMAIL")
    print("=" * 60)
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = YOUR_EMAIL
    msg['To'] = YOUR_EMAIL  # Send to yourself
    msg['Subject'] = "🎯 TEST: Thunderbird Extension Detection - Email Privacy Framework"
    
    # Add the privacy policy header (THIS IS WHAT YOUR EXTENSION DETECTS!)
    policy_header = create_privacy_policy()
    msg['X-Privacy-Policy'] = policy_header
    
    # Email body with tracking elements
    html_body = '''
    <html>
    <body>
        <h1 style="color: #2c3e50;">🎉 Thunderbird Extension Test</h1>
        
        <div style="background: #fff3cd; padding: 15px; border-radius: 5px; border: 1px solid #ffeaa7;">
            <h3>⚠️ PRIVACY POLICY DETECTION TEST</h3>
            <p>Your Thunderbird extension should detect the X-Privacy-Policy header and process the embedded privacy rules.</p>
        </div>
        
        <h2>Test Tracking Elements:</h2>
        <ul>
            <li>Tracking pixel: <img src="https://tracker.example.com/pixel.gif" width="1" height="1" style="border: 2px solid red;"></li>
            <li>Analytics image: <img src="http://analytics.test.com/track.png" style="border: 2px solid red;"></li>
        </ul>
        
        <div style="background: #d4edda; padding: 15px; border-radius: 5px; margin-top: 20px;">
            <h3>🎯 EXPECTED RESULTS IN THUNDERBIRD:</h3>
            <p>Your extension should log in Browser Console:</p>
            <ul>
                <li><strong>"🎉 PRIVACY POLICY DETECTED!"</strong></li>
                <li><strong>"📄 Privacy Policy Content: ..."</strong></li>
                <li><strong>Notification popup</strong> saying "Privacy Policy Found!"</li>
            </ul>
        </div>
        
        <p><em>This test validates your complete Email Privacy Framework system.</em></p>
    </body>
    </html>
    '''
    
    # Attach HTML body
    msg.attach(MIMEText(html_body, 'html'))
    
    print(f"📧 Email details:")
    print(f"   From/To: {YOUR_EMAIL}")
    print(f"   Subject: {msg['Subject']}")
    print(f"   SMTP: {smtp_server}:{smtp_port}")
    print(f"   Policy header length: {len(policy_header)} characters")
    
    try:
        # Connect and send
        print(f"\n🔗 Connecting to Gmail SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(YOUR_EMAIL, APP_PASSWORD)
        
        print("✅ Connected! Sending email...")
        server.send_message(msg)
        server.quit()
        
        print("🎉 REAL EMAIL SENT SUCCESSFULLY!")
        print("   Check your Thunderbird inbox and Browser Console!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\n💡 TROUBLESHOOTING:")
        print("   • Make sure you're using the 16-char APP PASSWORD, not your Gmail password")
        print("   • Ensure 2FA is enabled on your Gmail account")
        print("   • Check that 'Less secure app access' is NOT enabled (use app passwords)")
        return False

def main():
    print("🛡️ EMAIL PRIVACY FRAMEWORK - REAL TEST")
    print("Sending actual email to test Thunderbird extension detection")
    print("=" * 60)
    
    success = send_real_email()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 WHAT TO WATCH FOR IN THUNDERBIRD:")
        print("1. Email will arrive in your inbox in 10-60 seconds")
        print("2. Open Browser Console (Tools > Developer Tools > Browser Console)")
        print("3. Look for these messages:")
        print("   • '📧 New email received: 🎯 TEST: ...'")
        print("   • '🔍 Scanning for privacy policy...'")
        print("   • '🎉 PRIVACY POLICY DETECTED!'")
        print("   • '📄 Privacy Policy Content: ...'")
        print("4. You'll get a notification popup!")
    else:
        print("⚠️  Email not sent - check the error message above")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
