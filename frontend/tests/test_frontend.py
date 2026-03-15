import os
import pytest

FRONTEND_SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "app")

def test_app_component_exists():
    """Validates that the Angular app component exists and is auth-only."""
    ts_path = os.path.join(FRONTEND_SRC, "app.component.ts")
    assert os.path.exists(ts_path), f"Missing app.component.ts at {ts_path}"

    with open(ts_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "@Component" in content, "Missing @Component decorator"
    assert "standalone: true" in content, "Component should be standalone"
    assert "SubscriptionManagerComponent" in content, "Should import SubscriptionManagerComponent"
    # Auth-only: should NOT have subscription logic
    assert "addSubscription" not in content, "Subscription logic should be in subscription-manager"
    assert "saveSettings" not in content, "Save logic should be in subscription-manager"

def test_app_template_uses_child_components():
    """Validates that the parent template delegates to child components."""
    html_path = os.path.join(FRONTEND_SRC, "app.component.html")
    assert os.path.exists(html_path)

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "app-subscription-manager" in content, "Should use subscription-manager component"
    assert "*ngIf" in content, "Should use ngIf for conditional rendering"

def test_subscription_manager_component():
    """Validates the subscription-manager component owns all subscription logic."""
    mgr_dir = os.path.join(FRONTEND_SRC, "subscription-manager")
    assert os.path.isdir(mgr_dir), f"Missing subscription-manager directory"

    ts_path = os.path.join(mgr_dir, "subscription-manager.component.ts")
    with open(ts_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "@Component" in content, "Missing @Component decorator"
    assert "standalone: true" in content, "Should be standalone"
    assert "@Input() idToken" in content, "Should receive idToken from parent"
    assert "addSubscription" in content, "Should have addSubscription method"
    assert "removeSubscription" in content, "Should have removeSubscription method"
    assert "saveSettings" in content, "Should have saveSettings method"
    assert "fetchConfig" in content, "Should have fetchConfig method"
    assert "generateUUID" in content, "Should have generateUUID method"
    assert "SubscriptionCardComponent" in content, "Should import SubscriptionCardComponent"

    html_path = os.path.join(mgr_dir, "subscription-manager.component.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    assert "app-subscription-card" in html_content, "Should use subscription-card component"
    assert "*ngFor" in html_content, "Should iterate over subscriptions"

def test_subscription_card_component():
    """Validates the subscription-card child component."""
    card_dir = os.path.join(FRONTEND_SRC, "subscription-card")
    assert os.path.isdir(card_dir), f"Missing subscription-card directory"

    ts_path = os.path.join(card_dir, "subscription-card.component.ts")
    with open(ts_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "@Component" in content, "Missing @Component decorator"
    assert "standalone: true" in content, "Should be standalone"
    assert "@Input()" in content, "Should have @Input for subscription data"
    assert "@Output()" in content, "Should have @Output for remove event"
    assert "interface Subscription" in content, "Should export Subscription interface"

    html_path = os.path.join(card_dir, "subscription-card.component.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    assert "[(ngModel)]" in html_content, "Should have two-way binding"
    assert "glass-card" in html_content, "Should have glass-card class"

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(sys.argv))
