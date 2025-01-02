import os
import sys

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
