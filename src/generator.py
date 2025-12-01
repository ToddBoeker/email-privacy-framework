from .policy import PrivacyPolicy, Rule, Condition, Action
import datetime

class PolicyGenerator:
    """Pre-built policy templates for common use cases"""
    
    @staticmethod
    def no_forwarding_policy(creator: str) -> PrivacyPolicy:
        """Policy to prevent email forwarding"""
        policy = PrivacyPolicy(creator=creator)
        
        rule = Rule(
            rule_id="no-forward-1",
            condition=Condition(
                xpath=".//header[@name='Received'] | .//header[@name='Resent-From']"
            ),
            action=Action("warn", "This email should not be forwarded"),
            description="Detect and warn on forwarding attempts",
            scope="at-use"
        )
        policy.add_rule(rule)
        return policy
    
    @staticmethod
    def tracking_protection_policy(creator: str) -> PrivacyPolicy:
        """Policy to block tracking pixels and external content"""
        policy = PrivacyPolicy(creator=creator)
        
        # Search in raw HTML text content
        rule1 = Rule(
            rule_id="block-tracking-1",
            condition=Condition(
                xpath=".//raw-content[contains(., 'tracker.com') or contains(., 'pixel.gif') or contains(., 'analytics.com')]"
            ),
            action=Action("strip", "Tracking pixel detected and removed"),
            description="Remove tracking pixels",
            scope="at-use"
        )
        
        # Search for external image URLs in raw content
        rule2 = Rule(
            rule_id="block-external-2", 
            condition=Condition(
                xpath=".//raw-content[contains(., 'src=\"http')]"
            ),
            action=Action("warn", "External image detected - privacy risk"),
            description="Warn about external images", 
            scope="at-use"
        )
        
        # Add text-based pattern matching as backup
        rule3 = Rule(
            rule_id="text-tracking-3",
            condition=Condition(
                mime_pattern="tracker.com|pixel.gif|analytics.com"
            ),
            action=Action("warn", "Potential tracking content detected"),
            description="Text-based tracking detection",
            scope="at-use"
        )
        
        policy.add_rule(rule1)
        policy.add_rule(rule2)
        policy.add_rule(rule3)
        return policy
    
    @staticmethod
    def attachment_control_policy(creator: str) -> PrivacyPolicy:
        """Policy to control attachment handling"""
        policy = PrivacyPolicy(creator=creator)
        
        rule = Rule(
            rule_id="block-exe-attachments-1",
            condition=Condition(
                mime_pattern="application/x-msdownload|application/x-msdos-program"
            ),
            action=Action("block", "Executable attachments are not allowed"),
            description="Block executable attachments",
            scope="at-use"
        )
        policy.add_rule(rule)
        return policy
    
    @staticmethod
    def strict_privacy_policy(creator: str) -> PrivacyPolicy:
        """Comprehensive privacy policy with multiple protections"""
        policy = PrivacyPolicy(creator=creator)
        
        # Combine all the major rules
        forwarding_policy = PolicyGenerator.no_forwarding_policy(creator)
        tracking_policy = PolicyGenerator.tracking_protection_policy(creator)
        attachment_policy = PolicyGenerator.attachment_control_policy(creator)
        
        # Add all rules to the comprehensive policy
        for rule in forwarding_policy.rules:
            policy.add_rule(rule)
        for rule in tracking_policy.rules:
            policy.add_rule(rule)
        for rule in attachment_policy.rules:
            policy.add_rule(rule)
            
        return policy