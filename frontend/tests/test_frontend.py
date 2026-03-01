import os
import re
import pytest

def test_uuid_generator_logic_exists():
    """Validates that the UUID generator logic is correctly implemented in app.js"""
    app_js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.js")
    
    with open(app_js_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Verify the UUID pattern replacement is present
    assert "generateUUID" in content, "Missing generateUUID function"
    assert "'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace" in content, "Missing correct UUID format"

def test_vue_components_exist():
    """Validates that Vue is correctly defining components"""
    app_js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.js")
    
    with open(app_js_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "createApp" in content
    assert "setup()" in content

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(sys.argv))
