#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files for the frontend
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate