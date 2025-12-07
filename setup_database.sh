#!/bin/bash
set -e

# Activate venv and create database
source venv/bin/activate
cd backend

# Create the database
python create_db.py

# Run migrations
python manage.py migrate

# Create superuser (non-interactive)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else print('Superuser exists')" | python manage.py shell
