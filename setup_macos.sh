#!/bin/bash

echo "🐘 NOVYA LMS Local PostgreSQL Setup for macOS"
echo "=============================================="

echo ""
echo "📋 This script will help you set up PostgreSQL locally on macOS"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3 from https://python.org or using Homebrew"
    exit 1
fi

echo "✅ Python 3 is installed"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed"
    echo ""
    echo "📋 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Homebrew"
        exit 1
    fi
    echo "✅ Homebrew installed"
fi

echo "✅ Homebrew is installed"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed"
    echo ""
    echo "📦 Installing PostgreSQL..."
    brew install postgresql@15
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PostgreSQL"
        exit 1
    fi
    echo "✅ PostgreSQL installed"
fi

echo "✅ PostgreSQL is installed"

# Start PostgreSQL service
echo ""
echo "🔄 Starting PostgreSQL service..."
brew services start postgresql@15
if [ $? -ne 0 ]; then
    echo "❌ Failed to start PostgreSQL service"
    exit 1
fi
echo "✅ PostgreSQL service started"

# Create a database for the current user
echo ""
echo "🗄️ Creating database for current user..."
createdb $(whoami) 2>/dev/null || echo "Database already exists or created successfully"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.py
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"

# Run the Python setup script
echo ""
echo "🐍 Running Django setup..."
python3 setup_local_postgresql.py
if [ $? -ne 0 ]; then
    echo "❌ Django setup failed"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update DB_PASSWORD in .env file with your PostgreSQL password"
echo "2. Create superuser: python3 manage.py createsuperuser"
echo "3. Populate data: python3 manage.py populate_initial_data"
echo "4. Start server: python3 manage.py runserver"
echo ""
echo "🌐 Access points:"
echo "- Django Admin: http://localhost:8000/admin/"
echo "- API: http://localhost:8000/api/"
echo ""
