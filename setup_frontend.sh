#!/bin/bash
set -e

# Create frontend using Vite (React + JavaScript)
# Use --yes to skip interactive prompts
npm create vite@latest frontend -- --template react --yes

# Install dependencies
cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
