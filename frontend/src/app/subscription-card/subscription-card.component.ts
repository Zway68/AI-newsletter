import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface Subscription {
    id: string;
    name: string;
    prompt: string;
    frequency: string;
}

@Component({
    selector: 'app-subscription-card',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './subscription-card.component.html',
    styleUrls: ['./subscription-card.component.css']
})
export class SubscriptionCardComponent {
    @Input() subscription!: Subscription;
    @Input() animationDelay: string = '0s';
    @Output() remove = new EventEmitter<void>();

    onRemove() {
        this.remove.emit();
    }
}
