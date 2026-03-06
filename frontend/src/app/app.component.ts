import { Component, AfterViewInit, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

declare const google: any;

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit {
    isLoggedIn = false;
    email = "";
    name = "";
    picture = "";
    userId = "";
    idToken = "";
    subscriptions: any[] = [];
    saveMessage = "";
    clientId = "";

    constructor(private ngZone: NgZone) {
        // Check for existing session
        const storedToken = localStorage.getItem("id_token");
        const storedUser = localStorage.getItem("user_info");
        if (storedToken && storedUser) {
            this.idToken = storedToken;
            const user = JSON.parse(storedUser);
            this.email = user.email;
            this.name = user.name;
            this.picture = user.picture;
            this.userId = user.user_id;
            this.isLoggedIn = true;
            this.fetchConfig();
        }
    }

    async ngAfterViewInit() {
        // Fetch client ID from backend, then render the Google button
        try {
            const res = await fetch("/api/v1/auth/client-id");
            const data = await res.json();
            this.clientId = data.client_id;

            if (this.clientId && !this.isLoggedIn) {
                this.renderGoogleButton();
            }
        } catch (err) {
            console.error("Failed to fetch client ID", err);
        }
    }

    renderGoogleButton() {
        // Wait for GSI script to load
        const tryRender = () => {
            if (typeof google !== 'undefined' && google.accounts) {
                google.accounts.id.initialize({
                    client_id: this.clientId,
                    callback: (response: any) => {
                        this.ngZone.run(() => this.handleCredentialResponse(response));
                    },
                });
                const btnContainer = document.getElementById("google-signin-btn");
                if (btnContainer) {
                    google.accounts.id.renderButton(btnContainer, {
                        theme: "filled_blue",
                        size: "large",
                        shape: "pill",
                        text: "signin_with",
                    });
                }
            } else {
                setTimeout(tryRender, 200);
            }
        };
        tryRender();
    }

    async handleCredentialResponse(response: any) {
        const idToken = response.credential;
        try {
            const res = await fetch("/api/v1/auth/google", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ token: idToken }),
            });
            if (res.ok) {
                const user = await res.json();
                this.idToken = idToken;
                this.email = user.email;
                this.name = user.name;
                this.picture = user.picture;
                this.userId = user.user_id;
                this.isLoggedIn = true;

                localStorage.setItem("id_token", idToken);
                localStorage.setItem("user_info", JSON.stringify(user));

                this.fetchConfig();
            } else {
                const err = await res.json();
                console.error("Auth failed:", err);
            }
        } catch (err) {
            console.error("Failed to authenticate", err);
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
        if (!this.idToken) return;
        try {
            const res = await fetch("/api/v1/config", {
                headers: { "Authorization": `Bearer ${this.idToken}` }
            });
            if (res.ok) {
                const data = await res.json();
                this.email = data.email || this.email;
                this.subscriptions = data.subscriptions || [];
            }
        } catch (err) {
            console.error("Failed to fetch settings", err);
        }
    }

    logout() {
        localStorage.removeItem("id_token");
        localStorage.removeItem("user_info");
        this.isLoggedIn = false;
        this.subscriptions = [];
        this.idToken = "";
        this.email = "";
        this.name = "";
        this.userId = "";

        // Also sign out from Google
        if (typeof google !== 'undefined' && google.accounts) {
            google.accounts.id.disableAutoSelect();
        }

        // Re-render the sign-in button
        setTimeout(() => this.renderGoogleButton(), 100);
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
        try {
            const res = await fetch("/api/v1/config", {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${this.idToken}`,
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
