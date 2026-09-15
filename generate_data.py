import sys
import os

# Add backend directory to sys.path and run generate_data
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from backend.generate_data import generate_synthetic_data

if __name__ == '__main__':
    generate_synthetic_data()
