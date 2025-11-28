import pytest
import os
import sys

# Add the project root to the python path
sys.path.insert(0, os.getcwd())

# Run pytest
sys.exit(pytest.main(["-v"]))
