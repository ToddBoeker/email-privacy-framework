#!/usr/bin/env python3
"""
Debug script to see the actual email structure
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enforcer import PolicyEnforcer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def debug_email_structure():
    """See what the email actually looks like in XML form"""
    
    # Create the same test email
    test_email = MIMEMultipart()
    test_email['From'] = 'alice@company.com'
    test_email['To'] = 'bob@company.com'
    test_email['Subject'] = 'Test email with tracking pixels'
    
    body = """
    <html>
    <body>
        <h1>Important Information</h1>
        <p>This email contains tracking elements.</p>
        <img src="https://tracker.com/pixel.gif" width="1" height="1">
        <img src="http://analytics.com/track.png">
        <img src="https://example.com/logo.jpg">
    </body>
    </html>
    """
    test_email.attach(MIMEText(body, 'html'))
    
    # Convert to XML and print
    enforcer = PolicyEnforcer()
    email_xml = enforcer.parse_email_to_xml(test_email)
    
    print("EMAIL STRUCTURE IN XML:")
    print("=" * 50)
    
    # Pretty print the XML
    from lxml import etree as ET
    print(ET.tostring(email_xml, encoding='unicode', pretty_print=True))
    
    print("\nXPATH TEST RESULTS:")
    print("=" * 50)
    
    # Test different XPath expressions
    test_xpaths = [
        "//img",
        "//img[@src]",
        "//img[contains(@src, 'track')]",
        "//img[contains(@src, 'pixel')]",
        "//img[contains(@src, 'analytics')]",
        "//part[contains(content, 'tracker')]",
        "//content[contains(., 'tracker')]",
        "//filename",  # See if attachments are being parsed
        "//header[@name='Subject']"
    ]
    
    for xpath in test_xpaths:
        try:
            matches = email_xml.xpath(xpath)
            print(f"{xpath}: {len(matches)} matches")
            if matches and len(matches) > 0:
                for i, match in enumerate(matches[:2]):  # Show first 2 matches
                    try:
                        text = ET.tostring(match, encoding='unicode')[:100]
                        print(f"  Match {i+1}: {text}")
                    except:
                        print(f"  Match {i+1}: [can't display]")
        except Exception as e:
            print(f"{xpath}: ERROR - {e}")

if __name__ == "__main__":
    debug_email_structure()