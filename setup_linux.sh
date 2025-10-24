#!/bin/bash

echo "🐘 NOVYA LMS Local PostgreSQL Setup for Linux"
echo "=============================================="

echo ""
echo "📋 This script will help you set up PostgreSQL locally on Linux"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run this script as root"
    echo "Run it as a regular user with sudo privileges"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3 using your package manager"
    exit 1
fi

echo "✅ Python 3 is installed"

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo "❌ Cannot detect Linux distribution"
    exit 1
fi

echo "🖥️ Detected OS: $OS"

# Install PostgreSQL based on distribution
if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
    echo ""
    echo "📦 Installing PostgreSQL for Ubuntu/Debian..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib python3-pip
elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]] || [[ "$OS" == *"Fedora"* ]]; then
    echo ""
    echo "📦 Installing PostgreSQL for CentOS/RHEL/Fedora..."
    if command -v dnf &> /dev/null; then
        sudo dnf install -y postgresql-server postgresql-contrib python3-pip
    else
        sudo yum install -y postgresql-server postgresql-contrib python3-pip
    fi
    sudo postgresql-setup initdb
else
    echo "❌ Unsupported Linux distribution: $OS"
    echo "Please install PostgreSQL manually"
    exit 1
fi

if [ $? -ne 0 ]; then
    echo "❌ Failed to install PostgreSQL"
    exit 1
fi

echo "✅ PostgreSQL installed"

# Start PostgreSQL service
echo ""
echo "🔄 Starting PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql
if [ $? -ne 0 ]; then
    echo "❌ Failed to start PostgreSQL service"
    exit 1
fi
echo "✅ PostgreSQL service started"

# Create a database for the current user
echo ""
echo "🗄️ Creating database for current user..."
sudo -u postgres createdb $(whoami) 2>/dev/null || echo "Database already exists or created successfully"

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
