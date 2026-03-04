import os
import re
import pytest

FRONTEND_SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "app")

def test_app_component_exists():
    """Validates that the Angular app component TypeScript source exists."""
    ts_path = os.path.join(FRONTEND_SRC, "app.component.ts")
    assert os.path.exists(ts_path), f"Missing app.component.ts at {ts_path}"

    with open(ts_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "generateUUID" in content, "Missing generateUUID method"
    assert "'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace" in content, "Missing correct UUID format"

def test_angular_component_decorator():
    """Validates that the Angular @Component decorator is properly configured."""
    ts_path = os.path.join(FRONTEND_SRC, "app.component.ts")

    with open(ts_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "@Component" in content, "Missing @Component decorator"
    assert "standalone: true" in content, "Component should be standalone"
    assert "FormsModule" in content, "Missing FormsModule import for ngModel"
    assert "CommonModule" in content, "Missing CommonModule import for ngIf/ngFor"

def test_angular_template_directives():
    """Validates that the Angular template uses proper directives."""
    html_path = os.path.join(FRONTEND_SRC, "app.component.html")
    assert os.path.exists(html_path), f"Missing app.component.html at {html_path}"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "*ngIf" in content, "Missing *ngIf directives"
    assert "*ngFor" in content, "Missing *ngFor directives"
    assert "[(ngModel)]" in content, "Missing two-way binding with ngModel"

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(sys.argv))
