import email
from email import policy
from email.parser import BytesParser
from lxml import etree as ET
import logging
from typing import List, Dict, Any

class PolicyEnforcer:
    """Enforces privacy policies on email messages"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ns = {"pp": "urn:email:privacy:1.0"}
    
    def parse_email_to_xml(self, email_msg):
        """Convert MIME email to XML representation for XPath processing"""
        root = ET.Element("email")
        
        # Headers
        headers_elem = ET.SubElement(root, "headers")
        for key, value in email_msg.items():
            header_elem = ET.SubElement(headers_elem, "header", name=key)
            header_elem.text = value
        
        # Body parts - FIXED VERSION
        body_elem = ET.SubElement(root, "body")
        for part in email_msg.walk():
            if part.is_multipart():
                continue
                
            content_type = part.get_content_type()
            payload = part.get_payload(decode=True)
            
            if payload and content_type == 'text/html':
                try:
                    html_content = payload.decode('utf-8', errors='ignore')
                    part_elem = ET.SubElement(body_elem, "html-part")
                    ET.SubElement(part_elem, "content-type").text = content_type
                    
                    # Add the RAW HTML as text for text-based searching
                    raw_content_elem = ET.SubElement(part_elem, "raw-content")
                    raw_content_elem.text = html_content
                    
                    # Also try to parse HTML and create actual XML elements
                    try:
                        # Wrap in root element and parse
                        wrapped_html = f"<html-wrapper>{html_content}</html-wrapper>"
                        html_wrapper = ET.fromstring(wrapped_html)
                        
                        # Add all child elements as actual XML
                        for child in html_wrapper:
                            part_elem.append(child)
                            
                    except ET.ParseError as e:
                        # If HTML parsing fails, we'll rely on text searching
                        ET.SubElement(part_elem, "parse-error").text = str(e)
                        
                except Exception as e:
                    part_elem = ET.SubElement(body_elem, "part", error=str(e))
            
            elif payload:
                # Handle other content types
                part_elem = ET.SubElement(body_elem, "part")
                ET.SubElement(part_elem, "content-type").text = content_type
                try:
                    text_content = payload.decode('utf-8', errors='ignore')
                    content_elem = ET.SubElement(part_elem, "content")
                    content_elem.text = text_content
                except:
                    content_elem = ET.SubElement(part_elem, "content")
                    content_elem.text = "[binary data]"
        
        return root
    
    def enforce_policy(self, email_msg: email.message.Message, 
                      policy_xml: str) -> Dict[str, Any]:
        """Enforce privacy policy on email message"""
        results = {
            'actions_taken': [],
            'warnings': [],
            'blocks': [],
            'stripped_elements': []
        }
        
        try:
            # Parse policy
            policy_root = ET.fromstring(policy_xml.encode('utf-8'))
            
            # Convert email to XML for XPath processing
            email_xml = self.parse_email_to_xml(email_msg)
            
            # DEBUG: Print the XML structure to see what we're working with
            print("DEBUG - Email XML Structure:")
            print(ET.tostring(email_xml, encoding='unicode', pretty_print=True))
            print("=" * 50)
            
            # Process each rule
            for rule_elem in policy_root.findall(".//pp:Rule", self.ns):
                rule_id = rule_elem.get('id')
                scope = rule_elem.find('./pp:Scope', self.ns)
                
                if scope is not None and scope.get('phase') != 'at-use':
                    continue  # Skip rules not for current phase
                
                condition_elem = rule_elem.find('./pp:Condition', self.ns)
                action_elem = rule_elem.find('./pp:Action', self.ns)
                
                if condition_elem is None or action_elem is None:
                    continue
                
                # Evaluate XPath condition
                xpath_elem = condition_elem.find('./pp:XPath', self.ns)
                if xpath_elem is not None and xpath_elem.text:
                    xpath_expr = xpath_elem.text.strip()
                    try:
                        print(f"DEBUG - Testing rule {rule_id} with XPath: {xpath_expr}")
                        matches = email_xml.xpath(xpath_expr)
                        print(f"DEBUG - Found {len(matches)} matches")
                        
                        if matches:
                            action_type = action_elem.get('type')
                            action_msg = action_elem.get('message', '')
                            
                            self._execute_action(
                                action_type, rule_id, action_msg, 
                                matches, results, email_msg
                            )
                    except ET.XPathError as e:
                        print(f"DEBUG - XPath error in rule {rule_id}: {e}")
                        self.logger.warning(f"XPath error in rule {rule_id}: {e}")
            
        except ET.ParseError as e:
            print(f"DEBUG - Policy XML parsing error: {e}")
            self.logger.error(f"Policy XML parsing error: {e}")
            results['warnings'].append("Invalid policy format")
        
        return results
    
    def _execute_action(self, action_type: str, rule_id: str, message: str,
                       matches: List, results: Dict[str, Any],
                       email_msg: email.message.Message):
        """Execute the appropriate action based on policy"""
        
        if action_type == 'warn':
            results['warnings'].append({
                'rule': rule_id,
                'message': message,
                'matches': len(matches)
            })
            results['actions_taken'].append(f"warn:{rule_id}")
            
        elif action_type == 'strip':
            # In a real implementation, this would modify the email
            results['stripped_elements'].extend([
                f"{rule_id}:{ET.tostring(match, encoding='unicode')[:100]}"
                for match in matches
            ])
            results['actions_taken'].append(f"strip:{rule_id}")
            
        elif action_type == 'block':
            results['blocks'].append({
                'rule': rule_id,
                'message': message,
                'reason': 'Policy violation'
            })
            results['actions_taken'].append(f"block:{rule_id}")
            
        elif action_type == 'allow':
            results['actions_taken'].append(f"allow:{rule_id}")