#!/bin/bash

# Base directories
mkdir -p app/{models,admin,routes,templates/{auth,inventory,finance,admin}}
mkdir -p migrations/versions
mkdir -p static/{css,js,img,assets}
mkdir -p tests

# Files in the app directory
touch app/{__init__.py,config.py,extensions.py,errors.py}
touch app/models/{__init__.py,user.py,business.py,inventory.py,finance.py}
touch app/admin/{__init__.py,inventory_admin.py,finance_admin.py,user_admin.py}
touch app/routes/{__init__.py,auth.py,inventory.py,finance.py,admin.py,main.py}

# Template files
touch app/templates/{base.html}
touch app/templates/auth/.keep
touch app/templates/inventory/.keep
touch app/templates/finance/.keep
touch app/templates/admin/.keep

# Migration folder
touch migrations/README

# Tests
touch tests/{__init__.py,test_auth.py,test_inventory.py,test_finance.py,test_admin.py}

# Static files
touch static/css/.keep
touch static/js/.keep
touch static/img/.keep
touch static/assets/.keep

# Root-level files
touch Dockerfile docker-compose.yml LICENSE README.md requirements.txt run.py .env

# Pre-filled content in README.md
echo "# Project Overview" > README.md
echo "This is a placeholder for the project's README file." >> README.md

echo "Directory structure and files created successfully!"
