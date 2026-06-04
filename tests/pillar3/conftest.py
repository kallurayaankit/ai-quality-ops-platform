import sys
import os
import pytest

# Add sandbox to Python path
SANDBOX_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "existing_projects", "ai-agent-quality-sandbox"
)
sys.path.insert(0, SANDBOX_PATH)

# Import the adversary class – change "Adversary" to the actual class name
try:
    from adversary import Adversary   # or from main import Adversary, etc.
except ImportError:
    # If the sandbox has a different structure, adjust accordingly
    raise ImportError("Could not import Adversary from sandbox. Check the module path.")

@pytest.fixture(scope="session")
def adversary():
    """Return an instance of the sandbox adversarial agent."""
    return Adversary()