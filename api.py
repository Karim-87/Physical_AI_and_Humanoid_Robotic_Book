# Vercel FastAPI entrypoint
# This file is required by Vercel to detect the FastAPI application
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.main import app

# The 'app' variable is what Vercel looks for in FastAPI projects
# This satisfies Vercel's requirement for an entrypoint