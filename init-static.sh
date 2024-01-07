#!/bin/bash
# init-static.sh

# Remove existing static files
rm -rf staticfiles/*
rm -rf static/*

# Collect static files
python manage.py collectstatic --noinput

# Copy static files to the desired location
cp -r staticfiles/* static/
