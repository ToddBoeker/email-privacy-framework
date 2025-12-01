import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import base64
import quopri
from lxml import etree as ET

class MIMEPrivacyHandler:
    """Handles attaching and extracting privacy policies from emails"""
    
    PRIVACY_HEADER = "X-Privacy-Policy"
    PRIVACY_MIME_TYPE = "application/xml+privacy-policy"
    PRIVACY_NAMESPACE = "urn:email:privacy:1.0"
    
    @staticmethod
    def attach_policy(email_msg: MIMEMultipart, policy_xml: str, method: str = "both") -> MIMEMultipart:
        """
        Attach privacy policy to email using specified method
        
        Args:
            email_msg: The email message
            policy_xml: The privacy policy XML as string
            method: "header", "mime", or "both"
        """
        
        if method in ["header", "both"]:
            # Method A: Add as X-Header (base64 encoded)
            encoded_policy = base64.b64encode(policy_xml.encode('utf-8')).decode('ascii')
            email_msg[MIMEPrivacyHandler.PRIVACY_HEADER] = encoded_policy
        
        if method in ["mime", "both"]:
            # Method B: Add as dedicated MIME part
            policy_part = MIMEApplication(
                policy_xml.encode('utf-8'),
                _subtype='xml+privacy-policy'
            )
            policy_part.add_header(
                'Content-Type',
                f'{MIMEPrivacyHandler.PRIVACY_MIME_TYPE}; charset="utf-8"'
            )
            policy_part.add_header(
                'Content-Disposition',
                'attachment; filename="privacy-policy.xml"'
            )
            policy_part.add_header(
                'Content-Description',
                'Email Privacy Policy Metadata'
            )
            
            # Add to email
            email_msg.attach(policy_part)
        
        return email_msg
    
    @staticmethod
    def extract_policy(email_msg: email.message.Message) -> str:
        """
        Extract privacy policy from email, trying multiple methods
        
        Returns:
            Policy XML as string, or None if not found
        """
        policy_xml = None
        
        # Method 1: Try X-Header first (fastest)
        if MIMEPrivacyHandler.PRIVACY_HEADER in email_msg:
            try:
                encoded_policy = email_msg[MIMEPrivacyHandler.PRIVACY_HEADER]
                policy_xml = base64.b64decode(encoded_policy).decode('utf-8')
                print("✓ Extracted policy from X-Header")
                return policy_xml
            except Exception as e:
                print(f"✗ Failed to decode header policy: {e}")
        
        # Method 2: Try MIME parts
        for part in email_msg.walk():
            content_type = part.get_content_type()
            filename = part.get_filename()
            
            is_policy_part = (
                content_type == MIMEPrivacyHandler.PRIVACY_MIME_TYPE or
                filename == 'privacy-policy.xml' or
                (content_type == 'application/xml' and 'privacy' in str(part.get('Content-Description', '')).lower())
            )
            
            if is_policy_part:
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        policy_xml = payload.decode('utf-8')
                        print("✓ Extracted policy from MIME part")
                        return policy_xml
                except Exception as e:
                    print(f"✗ Failed to decode MIME policy: {e}")
        
        # Method 3: Try embedded in body (fallback)
        policy_xml = MIMEPrivacyHandler._extract_from_body(email_msg)
        if policy_xml:
            print("✓ Extracted policy from email body")
            return policy_xml
        
        print("✗ No privacy policy found in email")
        return None
    
    @staticmethod
    def _extract_from_body(email_msg: email.message.Message) -> str:
        """Extract policy from email body comments or hidden elements"""
        for part in email_msg.walk():
            if part.get_content_type() == 'text/html':
                payload = part.get_payload(decode=True)
                if payload:
                    html_content = payload.decode('utf-8', errors='ignore')
                    
                    # Look for policy in HTML comments
                    import re
                    comment_pattern = r'<!--\s*PRIVACY-POLICY-START(.*?)PRIVACY-POLICY-END\s*-->'
                    matches = re.findall(comment_pattern, html_content, re.DOTALL)
                    if matches:
                        return matches[0].strip()
        
        return None
    
    @staticmethod
    def create_email_with_policy(from_addr: str, to_addr: str, subject: str, 
                                body_html: str, policy_xml: str) -> MIMEMultipart:
        """
        Create a complete email with privacy policy attached
        """
        # Create base email
        msg = MIMEMultipart('mixed')
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        
        # Create HTML body part
        html_part = MIMEText(body_html, 'html')
        
        # Create multipart/alternative for body
        body_multipart = MIMEMultipart('alternative')
        body_multipart.attach(html_part)
        
        # Attach body to main message
        msg.attach(body_multipart)
        
        # Attach privacy policy
        msg = MIMEPrivacyHandler.attach_policy(msg, policy_xml, method="both")
        
        return msg
    
    @staticmethod
    def validate_policy_integrity(email_msg: email.message.Message) -> dict:
        """
        Validate that privacy policy is properly attached and accessible
        """
        validation_result = {
            'has_header': False,
            'has_mime_part': False,
            'policy_extractable': False,
            'policy_xml': None,
            'errors': []
        }
        
        # Check header
        if MIMEPrivacyHandler.PRIVACY_HEADER in email_msg:
            validation_result['has_header'] = True
            try:
                encoded = email_msg[MIMEPrivacyHandler.PRIVACY_HEADER]
                decoded = base64.b64decode(encoded).decode('utf-8')
                # Quick XML validation
                ET.fromstring(decoded)
                validation_result['policy_extractable'] = True
            except Exception as e:
                validation_result['errors'].append(f"Header policy invalid: {e}")
        
        # Check MIME parts
        for part in email_msg.walk():
            if part.get_content_type() == MIMEPrivacyHandler.PRIVACY_MIME_TYPE:
                validation_result['has_mime_part'] = True
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        policy_xml = payload.decode('utf-8')
                        ET.fromstring(policy_xml)  # Validate XML
                        validation_result['policy_extractable'] = True
                        validation_result['policy_xml'] = policy_xml
                except Exception as e:
                    validation_result['errors'].append(f"MIME policy invalid: {e}")
        
        return validation_result