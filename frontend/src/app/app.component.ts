import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    isLoggedIn = false;
    email = "";
    subscriptions: any[] = [];
    saveMessage = "";

    constructor() {
        const token = localStorage.getItem("auth_token");
        if (token) {
            this.login();
        }
    }

    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    async fetchConfig() {
        const token = localStorage.getItem("auth_token");
        if (!token) return;
        try {
            const res = await fetch("/api/v1/config?user_id=mock-user-id", {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                this.email = data.email || "user@example.com";
                this.subscriptions = data.subscriptions || [];
                this.isLoggedIn = true;
            } else {
                this.isLoggedIn = false;
            }
        } catch (err) {
            console.error("Failed to fetch settings", err);
        }
    }

    login() {
        localStorage.setItem("auth_token", "mock_oauth_token");
        this.isLoggedIn = true;
        this.fetchConfig();
    }

    logout() {
        localStorage.removeItem("auth_token");
        this.isLoggedIn = false;
        this.subscriptions = [];
    }

    addSubscription() {
        this.subscriptions.push({
            id: this.generateUUID(),
            name: "New Interest",
            prompt: "",
            frequency: "DAILY"
        });
    }

    removeSubscription(index: number) {
        this.subscriptions.splice(index, 1);
    }

    async saveSettings() {
        const token = localStorage.getItem("auth_token");
        try {
            const res = await fetch("/api/v1/config?user_id=mock-user-id", {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ subscriptions: this.subscriptions })
            });
            if (res.ok) {
                this.saveMessage = "Settings Saved Successfully!";
                setTimeout(() => this.saveMessage = "", 3000);
            }
        } catch (err) {
            console.error("Failed to save", err);
            this.saveMessage = "Failed to save settings.";
        }
    }
}
