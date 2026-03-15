import { Component, AfterViewInit, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SubscriptionManagerComponent } from './subscription-manager/subscription-manager.component';

declare const google: any;

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, SubscriptionManagerComponent],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit {
    isLoggedIn = false;
    email = '';
    name = '';
    picture = '';
    userId = '';
    idToken = '';
    clientId = '';

    constructor(private ngZone: NgZone) {
        const storedToken = localStorage.getItem('id_token');
        const storedUser = localStorage.getItem('user_info');
        if (storedToken && storedUser) {
            this.idToken = storedToken;
            const user = JSON.parse(storedUser);
            this.email = user.email;
            this.name = user.name;
            this.picture = user.picture;
            this.userId = user.user_id;
            this.isLoggedIn = true;
        }
    }

    async ngAfterViewInit() {
        try {
            const res = await fetch('/api/v1/auth/client-id');
            const data = await res.json();
            this.clientId = data.client_id;

            if (this.clientId && !this.isLoggedIn) {
                this.renderGoogleButton();
            }
        } catch (err) {
            console.error('Failed to fetch client ID', err);
        }
    }

    renderGoogleButton() {
        const tryRender = () => {
            if (typeof google !== 'undefined' && google.accounts) {
                google.accounts.id.initialize({
                    client_id: this.clientId,
                    callback: (response: any) => {
                        this.ngZone.run(() => this.handleCredentialResponse(response));
                    },
                });
                const btnContainer = document.getElementById('google-signin-btn');
                if (btnContainer) {
                    google.accounts.id.renderButton(btnContainer, {
                        theme: 'filled_blue',
                        size: 'large',
                        shape: 'pill',
                        text: 'signin_with',
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
            const res = await fetch('/api/v1/auth/google', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
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

                localStorage.setItem('id_token', idToken);
                localStorage.setItem('user_info', JSON.stringify(user));
            } else {
                const err = await res.json();
                console.error('Auth failed:', err);
            }
        } catch (err) {
            console.error('Failed to authenticate', err);
        }
    }

    logout() {
        localStorage.removeItem('id_token');
        localStorage.removeItem('user_info');
        this.isLoggedIn = false;
        this.idToken = '';
        this.email = '';
        this.name = '';
        this.userId = '';

        if (typeof google !== 'undefined' && google.accounts) {
            google.accounts.id.disableAutoSelect();
        }

        setTimeout(() => this.renderGoogleButton(), 100);
    }
}
