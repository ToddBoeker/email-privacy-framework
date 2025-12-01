// thunderbird/background.js
messenger.runtime.onMessage.addListener(async (message) => {
    if (message.type === "enforcePolicy") {
        // Call Python backend via native messaging
        const response = await messenger.runtime.sendNativeMessage(
            "email.privacy.framework",
            {action: "enforce", email: message.email, policy: message.policy}
        );
        return response;
    }
});