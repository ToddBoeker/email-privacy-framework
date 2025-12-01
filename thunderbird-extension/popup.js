// Enhanced popup with tabs and settings
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    loadSettings();
    setupEventListeners();
    addActivity('Enhanced framework loaded');
});

function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Deactivate all tabs
            tabs.forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Activate current tab
            this.classList.add('active');
            const tabName = this.getAttribute('data-tab');
            document.getElementById(tabName).classList.add('active');
        });
    });
}

function loadSettings() {
    browser.runtime.sendMessage({ action: "getSettings" })
        .then(response => {
            if (response.success) {
                const settings = response.settings;
                document.getElementById('stripTracking').checked = settings.stripTracking;
                document.getElementById('warnExternal').checked = settings.warnExternal;
                document.getElementById('blockExecutables').checked = settings.blockExecutables;
                document.getElementById('logPolicyHistory').checked = settings.logPolicyHistory;
                document.getElementById('showNotifications').checked = settings.showNotifications;
            }
        })
        .catch(error => {
            console.error('Settings load error:', error);
        });
}

function setupEventListeners() {
    // Settings
    document.getElementById('saveSettings').addEventListener('click', saveSettings);
    document.getElementById('getSettings').addEventListener('click', showCurrentSettings);
    
    // History
    document.getElementById('refreshHistory').addEventListener('click', refreshHistory);
    document.getElementById('clearHistory').addEventListener('click', clearHistory);
    
    // Testing
    document.getElementById('manualTest').addEventListener('click', manualTest);
    document.getElementById('simulatePolicy').addEventListener('click', simulatePolicy);
    document.getElementById('testAll').addEventListener('click', testAll);
}

function saveSettings() {
    const settings = {
        stripTracking: document.getElementById('stripTracking').checked,
        warnExternal: document.getElementById('warnExternal').checked,
        blockExecutables: document.getElementById('blockExecutables').checked,
        logPolicyHistory: document.getElementById('logPolicyHistory').checked,
        showNotifications: document.getElementById('showNotifications').checked
    };
    
    browser.runtime.sendMessage({ action: "updateSettings", settings: settings })
        .then(response => {
            if (response.success) {
                addActivity('Settings saved successfully');
            }
        })
        .catch(error => {
            console.error('Settings save error:', error);
            addActivity('Settings save failed');
        });
}

function showCurrentSettings() {
    browser.runtime.sendMessage({ action: "getSettings" })
        .then(response => {
            if (response.success) {
                console.log('Current settings:', response.settings);
                addActivity('Settings retrieved - check console');
            }
        });
}

function refreshHistory() {
    browser.runtime.sendMessage({ action: "getHistory" })
        .then(response => {
            if (response.success) {
                displayHistory(response.history);
                addActivity(`History refreshed: ${response.history.length} entries`);
            }
        });
}

function clearHistory() {
    browser.runtime.sendMessage({ action: "clearHistory" })
        .then(response => {
            if (response.success) {
                displayHistory([]);
                addActivity('History cleared');
            }
        });
}

function displayHistory(history) {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '';
    
    if (history.length === 0) {
        historyList.innerHTML = '<div class="history-entry">No policy history yet...</div>';
        return;
    }
    
    history.slice(-10).reverse().forEach(entry => {
        const entryEl = document.createElement('div');
        entryEl.className = 'history-entry';
        entryEl.innerHTML = `
            <strong>${new Date(entry.timestamp).toLocaleTimeString()}</strong><br>
            ${entry.email.subject}<br>
            <small>Rules: ${entry.policy.rules.length} | Actions: ${entry.actions.length}</small>
        `;
        historyList.appendChild(entryEl);
    });
}

function manualTest() {
    browser.runtime.sendMessage({ action: "manualTest" })
        .then(response => {
            if (response.success) {
                addActivity('Manual test completed');
            }
        });
}

function simulatePolicy() {
    browser.runtime.sendMessage({ action: "simulatePolicy" })
        .then(response => {
            if (response.success) {
                addActivity('Policy simulation started');
            }
        });
}

function testAll() {
    browser.runtime.sendMessage({ action: "testAllScenarios" })
        .then(response => {
            if (response.success) {
                addActivity('All features tested');
            }
        });
}

function addActivity(message) {
    const activityLog = document.getElementById('activityLog');
    const activity = document.createElement('div');
    activity.className = 'activity';
    activity.textContent = '🕒 ' + new Date().toLocaleTimeString() + ' - ' + message;
    activityLog.insertBefore(activity, activityLog.firstChild);
    
    if (activityLog.children.length > 5) {
        activityLog.removeChild(activityLog.lastChild);
    }
}
