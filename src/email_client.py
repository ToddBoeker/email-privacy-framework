#!/usr/bin/env python3
"""
Email client integration layer
"""

import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from .mime_handler import MIMEPrivacyHandler
from .enforcer import PolicyEnforcer
from .policy import PrivacyPolicy

class PrivacyAwareEmailClient:
    """
    Enhanced email client with privacy policy support
    """
    
    def __init__(self):
        self.enforcer = PolicyEnforcer()
        self.mime_handler = MIMEPrivacyHandler()
    
    def send_email(self, from_addr: str, to_addr: str, subject: str,
                  body_html: str, policy: PrivacyPolicy, 
                  smtp_server: str = "localhost", smtp_port: int = 587,
                  username: str = None, password: str = None) -> Dict[str, Any]:
        """
        Send email with privacy policy enforcement
        """
        try:
            # Convert policy to XML
            policy_xml = policy.to_string()
            
            # Create email with policy attached
            email_msg = self.mime_handler.create_email_with_policy(
                from_addr, to_addr, subject, body_html, policy_xml
            )
            
            # Validate policy attachment
            validation = self.mime_handler.validate_policy_integrity(email_msg)
            if not validation['policy_extractable']:
                return {
                    'success': False,
                    'error': 'Policy attachment failed',
                    'validation': validation
                }
            
            # Connect to SMTP server (simulated - replace with real SMTP)
            print(f"[SMTP] Connecting to {smtp_server}:{smtp_port}")
            print(f"[SMTP] Sending email from {from_addr} to {to_addr}")
            print(f"[SMTP] Subject: {subject}")
            print(f"[SMTP] Privacy policy attached: {len(policy_xml)} bytes")
            
            # In real implementation, you would:
            # server = smtplib.SMTP(smtp_server, smtp_port)
            # server.starttls()
            # server.login(username, password)
            # server.send_message(email_msg)
            # server.quit()
            
            return {
                'success': True,
                'message_id': f"<{id(email_msg)}@privacy-system>",
                'validation': validation,
                'policy_size': len(policy_xml)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def receive_email(self, raw_email: bytes) -> Dict[str, Any]:
        """
        Process incoming email with policy enforcement
        """
        try:
            # Parse email
            email_msg = email.message_from_bytes(raw_email)
            
            # Extract privacy policy
            policy_xml = self.mime_handler.extract_policy(email_msg)
            
            if policy_xml:
                print("✓ Privacy policy found, enforcing rules...")
                
                # Enforce policy
                enforcement_results = self.enforcer.enforce_policy(email_msg, policy_xml)
                
                return {
                    'success': True,
                    'policy_found': True,
                    'enforcement_results': enforcement_results,
                    'processed_email': email_msg
                }
            else:
                print("ℹ️  No privacy policy found, processing as normal email")
                return {
                    'success': True,
                    'policy_found': False,
                    'enforcement_results': None,
                    'processed_email': email_msg
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def simulate_email_flow(self, from_addr: str, to_addr: str, 
                           subject: str, body_html: str, policy: PrivacyPolicy) -> Dict[str, Any]:
        """
        Simulate complete email flow: send → transmit → receive → enforce
        """
        print("=" * 60)
        print("SIMULATING COMPLETE EMAIL FLOW WITH PRIVACY POLICY")
        print("=" * 60)
        
        # Step 1: Send email with policy
        print("\n1. SENDING EMAIL WITH PRIVACY POLICY")
        send_result = self.send_email(from_addr, to_addr, subject, body_html, policy)
        
        if not send_result['success']:
            return {'flow_complete': False, 'error': send_result['error']}
        
        # Step 2: Simulate transmission (convert to bytes and back)
        print("\n2. TRANSMITTING EMAIL")
        email_msg = self.mime_handler.create_email_with_policy(
            from_addr, to_addr, subject, body_html, policy.to_string()
        )
        raw_email = email_msg.as_bytes()
        print(f"✓ Email transmitted: {len(raw_email)} bytes")
        
        # Step 3: Receive and process email
        print("\n3. RECEIVING AND ENFORCING POLICY")
        receive_result = self.receive_email(raw_email)
        
        # Combine results
        result = {
            'flow_complete': True,
            'send_result': send_result,
            'receive_result': receive_result,
            'policy_attached': send_result['validation']['policy_extractable'],
            'policy_enforced': receive_result.get('policy_found', False)
        }
        
        print("\n" + "=" * 60)
        print("FLOW COMPLETE - SUMMARY:")
        print(f"  Policy Attached: {'✓' if result['policy_attached'] else '✗'}")
        print(f"  Policy Enforced: {'✓' if result['policy_enforced'] else '✗'}")
        if receive_result.get('enforcement_results'):
            actions = receive_result['enforcement_results']['actions_taken']
            print(f"  Actions Taken: {len(actions)}")
            for action in actions:
                print(f"    - {action}")
        print("=" * 60)
        
        return result