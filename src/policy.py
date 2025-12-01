import uuid
import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from lxml import etree as ET

@dataclass
class Condition:
    xpath: Optional[str] = None
    mime_pattern: Optional[str] = None
    composite: Optional[List['Condition']] = None
    operator: Optional[str] = None  # 'and', 'or', 'not'
    
    def to_xml(self) -> ET.Element:
        condition_elem = ET.Element("Condition")
        if self.xpath:
            xpath_elem = ET.SubElement(condition_elem, "XPath")
            xpath_elem.text = self.xpath
        elif self.mime_pattern:
            pattern_elem = ET.SubElement(condition_elem, "MIMEPattern")
            pattern_elem.text = self.mime_pattern
        elif self.composite:
            composite_elem = ET.SubElement(condition_elem, "Composite")
            for cond in self.composite:
                composite_elem.append(cond.to_xml())
        return condition_elem

@dataclass
class Action:
    action_type: str  # 'allow', 'warn', 'strip', 'block', 'encrypt', 'log'
    message: Optional[str] = None
    
    def to_xml(self) -> ET.Element:
        action_elem = ET.Element("Action", type=self.action_type)
        if self.message:
            action_elem.set("message", self.message)
        return action_elem

@dataclass
class Rule:
    rule_id: str
    condition: Condition
    action: Action
    description: Optional[str] = None
    priority: int = 1
    scope: str = "at-use"  # 'at-rest', 'in-transit', 'at-use'
    
    def to_xml(self) -> ET.Element:
        rule_elem = ET.Element("Rule", id=self.rule_id, priority=str(self.priority))
        
        if self.description:
            desc_elem = ET.SubElement(rule_elem, "Description")
            desc_elem.text = self.description
            
        rule_elem.append(self.condition.to_xml())
        rule_elem.append(self.action.to_xml())
        
        scope_elem = ET.SubElement(rule_elem, "Scope", phase=self.scope)
        return rule_elem

@dataclass
class PrivacyPolicy:
    policy_id: str = field(default_factory=lambda: f"policy-{uuid.uuid4()}")
    version: str = "1.0"
    creator: str = "unknown"
    created: datetime.datetime = field(default_factory=datetime.datetime.now)
    expires: Optional[datetime.datetime] = None
    rules: List[Rule] = field(default_factory=list)
    
    def add_rule(self, rule: Rule):
        self.rules.append(rule)
    
    def to_xml(self) -> ET.Element:
        nsmap = {None: "urn:email:privacy:1.0"}
        root = ET.Element("PrivacyPolicy", version=self.version, nsmap=nsmap)
        
        # Metadata
        metadata_elem = ET.SubElement(root, "Metadata")
        creator_elem = ET.SubElement(metadata_elem, "Creator")
        creator_elem.text = self.creator
        created_elem = ET.SubElement(metadata_elem, "Created")
        created_elem.text = self.created.isoformat()
        
        if self.expires:
            expires_elem = ET.SubElement(metadata_elem, "Expires")
            expires_elem.text = self.expires.isoformat()
        
        # Rules
        rules_elem = ET.SubElement(root, "Rules")
        for rule in self.rules:
            rules_elem.append(rule.to_xml())
            
        return root
    
    def to_string(self) -> str:
        xml_elem = self.to_xml()
        return ET.tostring(xml_elem, encoding="unicode", pretty_print=True)