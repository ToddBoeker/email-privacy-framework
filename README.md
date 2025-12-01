# Email Privacy Framework

## Project - Web DB Management 4806

### Overview
A comprehensive email privacy framework that enables senders to embed machine-readable privacy policies directly within emails, with client-side enforcement through Thunderbird extensions.

### Key Features
- **XML based Privacy Policies**: Standardized format for specifying email privacy rules
- **Thunderbird Extension**: Real time policy detection and enforcement
- **Python Framework**: Policy creation and email sending with embedded policies
- **Real Time Enforcement**: Content filtering, tracking protection, and security controls
- **Configurable Settings**: User customizable privacy preferences
- **Audit Logging**: Comprehensive policy history and action tracking

### Architecture Email Privacy Framework
├── Python Backend (Policy Creation & Email Sending)
├── Thunderbird Extension (Policy Detection & Enforcement)
└── XML Policy Specification (Standardized Format)

### Structure email-privacy-framework/
├── .vscode
├── build
├── dist
├── examples/ # Demo and test scripts
├── plugins
├── schemas
├── src
├── tests/ # Test suites
├── thunderbird-extension/ # Browser extension
├── venv
├── REAMDE # Documentation
├── requirements
└── send_real_test.spec

### Quick Start
1. **Send Test Email**: `python tests/send_real_test.py`
2. **Load Extension**: Install Thunderbird extension from `thunderbird-extension/`
3. **Monitor Detection**: Watch Browser Console for policy detection

### Demo Results
- Policy detection in real emails
- Tracking pixel removal
- User notification system
- Configurable privacy settings
- Comprehensive audit logging

### Practical Value
This project demonstrates:
- Database like policy specification and enforcement
- Real world privacy problem solving
- Client-server architecture
- Standards based interoperability

**Course**: Web DB Management 4806 - Fall 2025
**Students**: Todd Boeker and Yu Di


#### ===== Installation Guide ==== ####

# Installing the Thunderbird Extension


#### Method 1: Temporary Installation (Recommended for Development)

Follow these steps to load the extension in Thunderbird's developer mode:

1. **Prepare Your Extension Files**
   - Navigate to the `thunderbird-extension/` folder in the project directory
   - Ensure all required files are present (especially `manifest.json`)

2. **Open Thunderbird Settings**
   - Launch Thunderbird
   - Click the menu button (≡) in the top-right corner
   - Select **Settings** or **Preferences**

3. **Navigate to Extension Management**
   - In the Settings window, select **Extensions & Themes** from the left sidebar
   

4. **Enable Developer Mode**
   - In the Extensions panel, look for a gear icon (⚙️) or settings menu
   - Click it and select **Debug Add-ons** or **Developer Mode**
   - A new "Debugging" page will open

5. **Load Temporary Add-on**
   - On the Debugging page, click the **Load Temporary Add-on** button
   - Navigate to: `email-privacy-framework/thunderbird-extension/`
   - Select the `manifest.json` file
   - Click **Open**

6. **Verify Installation**
   - The extension should appear in your installed extensions list
   - You'll see: "Temporarily installed extension"
   - The extension remains installed until Thunderbird restarts



#### Method 2: Using 16-Digit Verification Code (For Gmail/Signed Testing)

For testing with real email accounts or distribution:

1. **Package Your Extension**
   ```bash
   cd thunderbird-extension/
   zip -r ../email-privacy-framework.xpi *

2. **Upload to Developer Hub**

    Visit addons.thunderbird.net/developers/
    Sign in with your Firefox/Thunderbird account
    Click Submit a New Add-on
    Upload your .xpi file
    Select On your own for distribution

3. **Get the 16-Digit Code**
    Gmail App Passwords (16 characters):
    Used for third-party app access
    Generated in Google Account → Security → App passwords
    Required to sync your Gmail account email to Mozilla Thunderbird
    Your Gmail requires 2-factor authentication backup as a prequiste to releasing the 16-code

4. **Install in Thunderbird**

    Go to Add-ons page in Thunderbird
    Click gear icon → Install Add-on From File
    When prompted, enter the 16-digit verification code




## Quick Start

1.  **Send a Test Email:** Run the provided executable.
    - Navigate to the `dist` folder in your terminal:

      bash
      cd path/to/email-privacy-framework/dist
      
    - Execute the program:
      
      # On Windows:
      .\send_real_test.exe

      # On macOS/Linux 
      ./send_real_test
      
    - This will send a test email with an embedded privacy policy.

2.  **Load the Extension:** Install the Thunderbird extension from the `thunderbird-extension/` folder.

3.  **Monitor Detection:** Watch the Thunderbird Browser Console for policy detection logs when you receive the test email.

## Installation Guide



##### Setting Up Python Environment ##$$

1. Install Dependencies
    pip install -r requirements.txt

2. Configure Email Setting
    cp config.example.py config.py
    # Edit config.py with your email credentials #


#### Building the Executable (Optional)
To rebuild the `send_real_test.exe` yourself from the source code:

1.  Ensure you have `pyinstaller` installed:
    bash
    - pip install pyinstaller
   
2.  Navigate to the project root and run:
    bash
    python -m PyInstaller --onefile .\tests\send_real_test.py
   
3.  The executable will be created in the `dist/` folder.