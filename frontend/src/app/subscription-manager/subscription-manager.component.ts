import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SubscriptionCardComponent, Subscription } from '../subscription-card/subscription-card.component';

@Component({
    selector: 'app-subscription-manager',
    standalone: true,
    imports: [CommonModule, FormsModule, SubscriptionCardComponent],
    templateUrl: './subscription-manager.component.html',
    styleUrls: ['./subscription-manager.component.css']
})
export class SubscriptionManagerComponent implements OnInit {
    @Input() idToken: string = '';

    subscriptions: Subscription[] = [];
    saveMessage = '';

    async ngOnInit() {
        await this.fetchConfig();
    }

    generateUUID(): string {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    async fetchConfig() {
        if (!this.idToken) return;
        try {
            const res = await fetch('/api/v1/config', {
                headers: { 'Authorization': `Bearer ${this.idToken}` }
            });
            if (res.ok) {
                const data = await res.json();
                this.subscriptions = data.subscriptions || [];
            }
        } catch (err) {
            console.error('Failed to fetch settings', err);
        }
    }

    addSubscription() {
        this.subscriptions.push({
            id: this.generateUUID(),
            name: 'New Interest',
            prompt: '',
            frequency: 'DAILY'
        });
    }

    removeSubscription(index: number) {
        this.subscriptions.splice(index, 1);
    }

    async saveSettings() {
        try {
            const res = await fetch('/api/v1/config', {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${this.idToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ subscriptions: this.subscriptions })
            });
            if (res.ok) {
                this.saveMessage = 'Settings Saved Successfully!';
                setTimeout(() => this.saveMessage = '', 3000);
            }
        } catch (err) {
            console.error('Failed to save', err);
            this.saveMessage = 'Failed to save settings.';
        }
    }
}
