#!/usr/bin/env python3
"""
Enhanced Demo with MIME Integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.policy import PrivacyPolicy, Rule, Condition, Action
from src.generator import PolicyGenerator
from src.email_client import PrivacyAwareEmailClient

def demo_complete_email_flow():
    """Demonstrate complete email flow with MIME integration"""
    
    print("🎯 DEMONSTRATING MIME INTEGRATION WITH EMAIL CLIENTS")
    print("=" * 60)
    
    # Create test content with tracking
    test_body = """
    <html>
    <body>
        <h1>Confidential Report</h1>
        <p>This email contains sensitive information and tracking elements.</p>
        
        <!-- Tracking elements -->
        <img src="https://tracker.com/pixel.gif" width="1" height="1">
        <img src="http://analytics.com/track.png">
        
        <p>Please do not forward this email.</p>
        <p>Best regards,<br>Security Team</p>
    </body>
    </html>
    """
    
    # Create comprehensive privacy policy
    policy = PolicyGenerator.strict_privacy_policy("security@company.com")
    
    # Initialize privacy-aware email client
    client = PrivacyAwareEmailClient()
    
    # Simulate complete email flow
    result = client.simulate_email_flow(
        from_addr="security@company.com",
        to_addr="employee@company.com", 
        subject="Confidential Security Report",
        body_html=test_body,
        policy=policy
    )
    
    return result

def demo_policy_attachment_methods():
    """Demonstrate different policy attachment methods"""
    
    print("\n🔧 DEMONSTRATING POLICY ATTACHMENT METHODS")
    print("=" * 60)
    
    from src.mime_handler import MIMEPrivacyHandler
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    # Create test email
    test_email = MIMEMultipart()
    test_email['From'] = 'test@company.com'
    test_email['To'] = 'test@example.com'
    test_email['Subject'] = 'Test Policy Attachment'
    test_email.attach(MIMEText('<p>Test content</p>', 'html'))
    
    # Create test policy
    policy = PolicyGenerator.tracking_protection_policy("test@company.com")
    policy_xml = policy.to_string()
    
    # Test different attachment methods
    methods = ['header', 'mime', 'both']
    
    for method in methods:
        print(f"\nTesting attachment method: {method.upper()}")
        print("-" * 40)
        
        email_copy = MIMEMultipart()
        for key, value in test_email.items():
            email_copy[key] = value
        for part in test_email.get_payload():
            email_copy.attach(part)
        
        # Attach policy
        enhanced_email = MIMEPrivacyHandler.attach_policy(email_copy, policy_xml, method)
        
        # Validate
        validation = MIMEPrivacyHandler.validate_policy_integrity(enhanced_email)
        print(f"  Header attached: {validation['has_header']}")
        print(f"  MIME part attached: {validation['has_mime_part']}")
        print(f"  Policy extractable: {validation['policy_extractable']}")
        
        # Test extraction
        extracted = MIMEPrivacyHandler.extract_policy(enhanced_email)
        print(f"  Extraction successful: {extracted is not None}")
        print(f"  Extraction method: {'header' if validation['has_header'] and extracted else 'mime' if validation['has_mime_part'] and extracted else 'failed'}")

def demo_real_world_scenarios():
    """Demonstrate real-world email scenarios"""
    
    print("\n🌍 REAL-WORLD SCENARIOS")
    print("=" * 60)
    
    scenarios = [
        {
            'name': 'Marketing Email',
            'body': '''
            <html><body>
            <h1>Special Offer!</h1>
            <img src="https://tracker.marketing.com/pixel.png">
            <img src="http://ads.com/banner.jpg">
            <p>Limited time offer!</p>
            </body></html>
            ''',
            'policy': 'tracking_protection_policy'
        },
        {
            'name': 'HR Confidential',
            'body': '''
            <html><body>
            <h1>Confidential: Employee Reviews</h1>
            <p>This contains sensitive employee information.</p>
            <p>DO NOT FORWARD</p>
            </body></html>
            ''',
            'policy': 'strict_privacy_policy'
        }
    ]
    
    client = PrivacyAwareEmailClient()
    
    for scenario in scenarios:
        print(f"\n📧 Scenario: {scenario['name']}")
        print("-" * 40)
        
        # Get policy
        policy_method = getattr(PolicyGenerator, scenario['policy'])
        policy = policy_method("sender@company.com")
        
        # Simulate flow
        result = client.simulate_email_flow(
            "sender@company.com",
            "recipient@company.com",
            f"Test: {scenario['name']}",
            scenario['body'],
            policy
        )
        
        print(f"  Result: {'SUCCESS' if result['flow_complete'] else 'FAILED'}")
        if result.get('receive_result', {}).get('enforcement_results'):
            actions = result['receive_result']['enforcement_results']['actions_taken']
            print(f"  Actions triggered: {len(actions)}")

if __name__ == "__main__":
    print("🚀 ENHANCED PRIVACY FRAMEWORK DEMO")
    print("Focus: MIME Integration & Email Client Compatibility")
    print("=" * 60)
    
    # Run demos
    demo_complete_email_flow()
    demo_policy_attachment_methods() 
    demo_real_world_scenarios()
    
    print("\n" + "=" * 60)
    print("🎉 MIME INTEGRATION DEMONSTRATION COMPLETE!")
    print("Your framework now supports real email client integration.")
    print("=" * 60)