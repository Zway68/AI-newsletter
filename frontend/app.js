const { createApp, ref, onMounted } = Vue;

const generateUUID = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
};

createApp({
    setup() {
        const isLoggedIn = ref(false);
        const email = ref("");
        const subscriptions = ref([]);
        const saveMessage = ref("");

        // Simple auth mock for now. Will be replaced by Google Auth logic later.
        const token = localStorage.getItem("auth_token") || "";

        const fetchConfig = async () => {
            if (!token) return;
            try {
                // Hardcode mock user_id since backend setup currently requires it
                const res = await fetch("/api/v1/config?user_id=mock-user-id", {
                    headers: { "Authorization": `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    email.value = data.email || "user@example.com";
                    subscriptions.value = data.subscriptions || [];
                    isLoggedIn.value = true;
                } else {
                    isLoggedIn.value = false;
                }
            } catch (err) {
                console.error("Failed to fetch settings", err);
            }
        };

        const login = () => {
            localStorage.setItem("auth_token", "mock_oauth_token");
            isLoggedIn.value = true;
            fetchConfig();
        };

        const logout = () => {
            localStorage.removeItem("auth_token");
            isLoggedIn.value = false;
            subscriptions.value = [];
        };

        const addSubscription = () => {
            subscriptions.value.push({
                id: generateUUID(),
                name: "New Interest",
                prompt: "",
                frequency: "DAILY"
            });
        };

        const removeSubscription = (index) => {
            subscriptions.value.splice(index, 1);
        };

        const saveSettings = async () => {
            try {
                const res = await fetch("/api/v1/config?user_id=mock-user-id", {
                    method: "PUT",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ subscriptions: subscriptions.value })
                });
                if (res.ok) {
                    saveMessage.value = "Settings Saved Successfully!";
                    setTimeout(() => saveMessage.value = "", 3000);
                }
            } catch (err) {
                console.error("Failed to save", err);
                saveMessage.value = "Failed to save settings.";
            }
        };

        onMounted(() => {
            if (token) login();
        });

        return {
            isLoggedIn, email, subscriptions, saveMessage,
            login, logout, addSubscription, removeSubscription, saveSettings
        };
    }
}).mount('#app');
