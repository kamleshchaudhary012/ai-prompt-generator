#!/bin/bash
# exit on error
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Showing migrations..."
python manage.py showmigrations

echo "Running migrations..."
python manage.py migrate --no-input
python manage.py migrate generator --no-input

echo "Loading initial data..."
python manage.py load_initial_data || {
  echo "Warning: Initial data load failed, but continuing deployment"
}

echo "Setup completed successfully!" 