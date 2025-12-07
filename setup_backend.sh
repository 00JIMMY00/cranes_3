#!/bin/bash
set -e

# Create backend directory
mkdir -p backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install django djangorestframework psycopg2-binary python-dotenv django-cors-headers

# Freeze requirements
pip freeze > requirements.txt

# Initialize Django Project (if not exists)
if [ ! -f "backend/manage.py" ]; then
    django-admin startproject core backend
fi
