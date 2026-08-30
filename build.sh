#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "========================================="
echo " 1. Building React + Vite Frontend"
echo "========================================="
cd frontend
npm install
npm run build
cd ..

echo "========================================="
echo " 2. Installing Python Backend Dependencies"
echo "========================================="
python -m pip install --upgrade pip
pip install -r backend/requirements.txt

echo "========================================="
echo " [+] Build Completed Successfully!"
echo "========================================="
