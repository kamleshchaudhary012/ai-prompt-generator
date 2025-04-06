#!/bin/bash
# exit on error
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Loading initial data..."
python manage.py load_initial_data || {
  echo "Warning: Initial data load failed, but continuing deployment"
}

echo "Setup completed successfully!" 