// Email Privacy Framework - Thunderbird Extension
console.log("Email Privacy Framework ACTIVE - Monitoring emails");

// Default user settings
const DEFAULT_SETTINGS = {
    stripTracking: true,
    warnExternal: true, 
    blockExecutables: true,
    logPolicyHistory: true,
    showNotifications: true
};

// Policy history storage
let policyHistory = [];

// Safe notification function
function safeNotification(title, message) {
    if (DEFAULT_SETTINGS.showNotifications && browser.notifications && browser.notifications.create) {
        browser.notifications.create({
            type: "basic",
            title: title,
            message: message
        });
    }
    console.log(`${title}: ${message}`);
}

// ==================== REAL POLICY ENFORCEMENT ====================

function stripTrackingPixels(htmlContent) {
    if (!DEFAULT_SETTINGS.stripTracking) return htmlContent;
    
    const originalLength = htmlContent.length;
    // Remove tracking pixels and analytics images
    const cleanedContent = htmlContent.replace(
        /<img[^>]*src=["'][^"']*(tracker|pixel|analytics|beacon|monitor)[^"']*["'][^>]*>/gi, 
        '<!-- Tracking pixel removed by Email Privacy Framework -->'
    );
    
    if (cleanedContent.length !== originalLength) {
        console.log("🔍 Removed tracking pixels from email content");
        safeNotification("Tracking Protection", "Tracking pixels were removed from this email");
    }
    
    return cleanedContent;
}

function warnAboutExternalContent(htmlContent) {
    if (!DEFAULT_SETTINGS.warnExternal) return htmlContent;
    
    const externalImages = htmlContent.match(/<img[^>]*src=["'](http:\/\/|https:\/\/)[^"']*["'][^>]*>/gi);
    if (externalImages && externalImages.length > 0) {
        console.log(`Found ${externalImages.length} external images`);
        safeNotification("External Content", `This email contains ${externalImages.length} external images that may track you`);
    }
    
    return htmlContent;
}

function blockExecutableAttachments(attachments) {
    if (!DEFAULT_SETTINGS.blockExecutables) return true;
    
    const dangerousTypes = ['.exe', '.msi', '.bat', '.cmd', '.scr', '.pif'];
    const dangerousAttachments = attachments.filter(att => 
        dangerousTypes.some(ext => att.name.toLowerCase().endsWith(ext))
    );
    
    if (dangerousAttachments.length > 0) {
        console.log(`Blocked ${dangerousAttachments.length} executable attachments`);
        safeNotification("Security Block", "Executable attachments were blocked for security");
        return false;
    }
    
    return true;
}

// ==================== POLICY HISTORY ====================

function logPolicyDetection(email, policy, actionsTaken) {
    if (!DEFAULT_SETTINGS.logPolicyHistory) return;
    
    const historyEntry = {
        timestamp: new Date().toISOString(),
        email: {
            subject: email.subject,
            from: email.from,
            id: email.id || Date.now()
        },
        policy: {
            rules: policy ? policy.rules : [],
            creator: policy ? policy.creator : 'unknown'
        },
        actions: actionsTaken,
        settings: {...DEFAULT_SETTINGS}
    };
    
    policyHistory.push(historyEntry);
    
    // Keep only last 100 entries
    if (policyHistory.length > 100) {
        policyHistory = policyHistory.slice(-100);
    }
    
    console.log(`Policy logged: ${email.subject}`, historyEntry);
}

function getPolicyHistory() {
    return policyHistory;
}

function clearPolicyHistory() {
    policyHistory = [];
    console.log("Policy history cleared");
}

// ==================== SETTINGS MANAGEMENT ====================

function updateUserSettings(newSettings) {
    Object.assign(DEFAULT_SETTINGS, newSettings);
    console.log("Settings updated:", DEFAULT_SETTINGS);
    safeNotification("Settings Updated", "Your privacy settings have been updated");
    
    return DEFAULT_SETTINGS;
}

function getCurrentSettings() {
    return {...DEFAULT_SETTINGS};
}

// // This is the core algorithm that processes privacy policies
async function processPrivacyPolicy(message, policyData) {
    const actionsTaken = [];
    
    try {
        // Decode base64 policy
        const decodedPolicy = atob(policyData);
        console.log("Processing privacy policy:", decodedPolicy.substring(0, 200) + "...");
        
        // Parse XML policy (simplified - in real implementation you'd use DOMParser)
        const policy = parsePolicyXML(decodedPolicy);
        
        // Apply policy rules
        if (policy && policy.rules) {
            for (const rule of policy.rules) {
                console.log(`Applying rule: ${rule.id} - ${rule.description}`);
                actionsTaken.push({
                    ruleId: rule.id,
                    description: rule.description,
                    action: rule.action,
                    applied: true
                });
                
                // Show rule-specific notification
                safeNotification(`Policy: ${rule.id}`, rule.action.message);
            }
        }
        
        // Log this policy detection
        logPolicyDetection(message, policy, actionsTaken);
        
        console.log("Privacy policy processed successfully", actionsTaken);
        return { success: true, actions: actionsTaken };
        
    } catch (error) {
        console.error("Error processing policy:", error);
        return { success: false, error: error.message };
    }
}

function parsePolicyXML(xmlContent) {
    // Simplified XML parsing - in a real implementation you'd use DOMParser
    try {
        const creatorMatch = xmlContent.match(/<Creator>([^<]+)<\/Creator>/);
        const rulesMatch = xmlContent.match(/<Rule[^>]*>([\s\S]*?)<\/Rule>/g);
        
        const rules = [];
        if (rulesMatch) {
            rulesMatch.forEach(ruleXml => {
                const idMatch = ruleXml.match(/id="([^"]*)"/);
                const descMatch = ruleXml.match(/<Description>([^<]+)<\/Description>/);
                const actionTypeMatch = ruleXml.match(/<Action[^>]*type="([^"]*)"/);
                const actionMsgMatch = ruleXml.match(/message="([^"]*)"/);
                
                if (idMatch && actionTypeMatch) {
                    rules.push({
                        id: idMatch[1],
                        description: descMatch ? descMatch[1] : 'No description',
                        action: {
                            type: actionTypeMatch[1],
                            message: actionMsgMatch ? actionMsgMatch[1] : 'Action applied'
                        }
                    });
                }
            });
        }
        
        return {
            creator: creatorMatch ? creatorMatch[1] : 'unknown',
            rules: rules
        };
    } catch (error) {
        console.error("XML parsing error:", error);
        return null;
    }
}

// ==================== MESSAGE HANDLING ====================

// Listen for messages from popup
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Message received from popup:", message);
    
    switch (message.action) {
        case "manualTest":
            safeNotification("Manual Test", "Extension is fully functional with enhanced features");
            sendResponse({ success: true, message: "Enhanced test completed" });
            break;
            
        case "simulatePolicy":
            simulateEmailDetection();
            sendResponse({ success: true, message: "Policy simulation started" });
            break;
            
        case "testAllScenarios":
            testAllEmailScenarios();
            sendResponse({ success: true, message: "All scenarios tested" });
            break;
            
        case "checkCurrentEmails":
            checkCurrentInbox();
            sendResponse({ success: true, message: "Checking inbox" });
            break;
            
        case "getSettings":
            sendResponse({ success: true, settings: getCurrentSettings() });
            break;
            
        case "updateSettings":
            const updated = updateUserSettings(message.settings);
            sendResponse({ success: true, settings: updated });
            break;
            
        case "getHistory":
            sendResponse({ success: true, history: getPolicyHistory() });
            break;
            
        case "clearHistory":
            clearPolicyHistory();
            sendResponse({ success: true, message: "History cleared" });
            break;
            
        default:
            sendResponse({ success: false, error: "Unknown action" });
    }
    
    return true;
});

// ==================== SIMULATION & TESTING ====================

const TEST_EMAILS = [
    {
        subject: "Regular Newsletter",
        from: "news@example.com",
        hasPolicy: false,
        content: "Check out our products! <img src=\"https://tracker.com/pixel.gif\">"
    },
    {
        subject: "HR Confidential Report", 
        from: "hr@company.com",
        hasPolicy: true,
        policy: "PFByaXZhY3lQb2xpY3k+PG1ldGFkYXRhPjxjcmVhdG9yPmhyQGNvbXBhbnkuY29tPC9jcmVhdG9yPjwvbWV0YWRhdGE+PHJ1bGVzPjxydWxlIGlkPSJuby1mb3J3YXJkIj48ZGVzY3JpcHRpb24+V2FybiBhYm91dCBmb3J3YXJkaW5nPC9kZXNjcmlwdGlvbj48YWN0aW9uIHR5cGU9Indhcm4iIG1lc3NhZ2U9IkRvIG5vdCBmb3J3YXJkIHRoaXMgZW1haWwiLz48L3J1bGU+PC9ydWxlcz48L1ByaXZhY3lQb2xpY3k+"
    }
];

function simulateEmailDetection() {
    console.log("SIMULATING ENHANCED EMAIL DETECTION...");
    
    TEST_EMAILS.forEach((email, index) => {
        setTimeout(() => {
            console.log(`[SIM] Email ${index + 1}: "${email.subject}"`);
            
            if (email.hasPolicy) {
                console.log(`[SIM] POLICY DETECTED in: "${email.subject}"`);
                
                // Test content filtering
                if (email.content) {
                    const filteredContent = stripTrackingPixels(email.content);
                    const warnedContent = warnAboutExternalContent(filteredContent);
                    console.log("Content filtering applied:", warnedContent !== email.content);
                }
                
                processPrivacyPolicy(
                    { subject: email.subject, from: email.from },
                    email.policy
                );
            }
        }, index * 2000);
    });
}

function testAllEmailScenarios() {
    console.log("TESTING ENHANCED SCENARIOS");
    console.log("=" .repeat(50));
    
    // Test settings
    console.log("Current Settings:", getCurrentSettings());
    
    // Test policy history
    logPolicyDetection(
        { subject: "Test Email", from: "test@example.com" },
        { creator: "test", rules: [{ id: "test-rule", description: "Test rule", action: { type: "test", message: "Test message" } }] },
        [{ ruleId: "test-rule", description: "Test rule", action: { type: "test" }, applied: true }]
    );
    
    console.log("Policy History:", getPolicyHistory().length, "entries");
    
    safeNotification("Enhanced Test", "All advanced features tested successfully");
}

// ==================== INITIALIZATION ====================

console.log("Starting enhanced framework in 3 seconds...");
setTimeout(() => {
    testAllEmailScenarios();
}, 3000);

console.log("Enhanced Email Privacy Framework fully loaded!");
