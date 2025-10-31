#!/bin/bash

# ============================================
# Bot Analysis - Setup & Run Script
# ============================================

set -e

echo "🚀 Bot User Behavior Analysis - Setup Wizard"
echo "==========================================="
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "✅ Found existing .env file"
    echo "   Do you want to use it? (y/n)"
    read -r use_existing

    if [ "$use_existing" != "y" ]; then
        echo "   Creating new configuration..."
        rm .env
    fi
fi

# Create .env if doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Setting up database configuration..."
    echo ""

    # Database Host
    echo "Enter database host (e.g., localhost or db.example.com):"
    read -r db_host

    # Database Port
    echo "Enter database port (default: 3306):"
    read -r db_port
    db_port=${db_port:-3306}

    # Database User
    echo "Enter database username:"
    read -r db_user

    # Database Password
    echo "Enter database password:"
    read -rs db_pass  # -s for silent (no echo)
    echo ""

    # Database Name
    echo "Enter database name (default: tg2app):"
    read -r db_name
    db_name=${db_name:-tg2app}

    # Write to .env
    cat > .env << EOF
# Database Configuration (Auto-generated)
DB_HOST=${db_host}
DB_PORT=${db_port}
DB_USER=${db_user}
DB_PASS=${db_pass}
DB_NAME=${db_name}

# API Configuration
API_BASE_URL=https://api.myshell.ai
API_SERVICE_NAME=organics-api
EOF

    echo ""
    echo "✅ Configuration saved to .env"
fi

# Load environment variables
echo ""
echo "📂 Loading configuration..."
export $(cat .env | grep -v '^#' | xargs)

# Test database connection
echo ""
echo "🔌 Testing database connection..."

# Try to connect to database
if command -v mysql &> /dev/null; then
    if mysql -h"${DB_HOST}" -P"${DB_PORT}" -u"${DB_USER}" -p"${DB_PASS}" -e "USE ${DB_NAME}; SELECT 1;" &> /dev/null; then
        echo "✅ Database connection successful!"
    else
        echo "❌ Database connection failed!"
        echo "   Please check your credentials in .env file"
        exit 1
    fi
else
    echo "⚠️  MySQL client not found. Skipping connection test."
    echo "   Will attempt to run queries anyway..."
fi

# Run analysis
echo ""
echo "🔍 Starting analysis execution..."
echo ""

# Execute the main analysis script
./execute_analysis.sh

echo ""
echo "✨ Analysis complete!"
echo "   Results saved to: analysis_results_*/"
