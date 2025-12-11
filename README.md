# RPG Character Sheet Web Application

A comprehensive web-based character sheet manager for tabletop RPGs, built with Flask and designed for easy deployment with Docker on Linux systems.

## Overview

This application provides a complete digital character sheet solution for tabletop role-playing games. It allows you to create, manage, and track multiple characters with detailed stats, skills, equipment, and more. The application is containerized for easy deployment and includes database migration support.

## Features

### Character Management
- **Create Characters**: Generate new characters with default attributes and skills
- **Character Statistics**: Manage core attributes, basic skills, and special abilities
- **Equipment Tracking**: Track armor, weapons, ammunition, and general trappings
- **Spell Management**: Organize spells and prayers for magic-using characters
- **Experience Tracking**: Monitor character progression and experience points

### Party Management
- **Party Ledger**: Shared inventory and resource management
- **Group Coordination**: Track party-wide equipment and finances

### Data Persistence
- **SQLite Database**: Reliable local storage with automatic migrations
- **Backup Support**: Easy database backup through Docker volumes

## Prerequisites (Linux)

### Required Software
- **Docker**: Version 20.10 or later
- **Docker Compose**: Version 2.0 or later

Ensure Docker and Docker Compose are installed and properly configured on your Linux system before proceeding.

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd RPG_character_sheet

# Make the entrypoint script executable
chmod +x docker-entrypoint.sh

# Copy environment file template and configure if needed
cp .env.example .env
# Edit .env to customize settings (optional - defaults are sensible)
```

### 2. Environment Configuration

Configuration is managed through environment variables. See `.env.example` for all available options:

- `FLASK_ENV` - Set to `production` or `development` (default: `development`)
- `FLASK_SECRET_KEY` - Secret key for session/CSRF protection (auto-generated dev key if not set)
- `DATABASE_URL` - Database connection string (default: `sqlite:///CharSheet.db`)

For development, the defaults are fine. For production, you **must** set a strong `FLASK_SECRET_KEY`.

### 3. Production Deployment
```bash
# Start the application in production mode
docker compose up -d

# View logs
docker compose logs -f app

# Access the application at http://localhost:5000
```

### 4. Development Mode
```bash
# Start in development mode with live reload
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Access the application at http://localhost:5000
```

## Usage Guide

### Creating Your First Character

1. **Access the Application**: Open your web browser and navigate to `http://localhost:5000`
2. **Create Character**: Click on "Create New Character" or similar option
3. **Fill Basic Information**: Enter character name, description, and basic details
4. **Set Attributes**: Configure core attributes like Strength, Dexterity, Intelligence, etc.
5. **Assign Skills**: Allocate points to basic and special skills
6. **Add Equipment**: Configure starting armor, weapons, and trappings

### Managing Characters

#### Character Sheets
- **Battle Page**: Combat-focused view with weapons, armor, and health tracking
- **Skills & Talents**: Comprehensive skill management and talent selection
- **Fluff Page**: Character background, description, and roleplaying information

#### Equipment Management
- **Weapons**: Add/edit weapons with damage, range, and special properties
- **Armor**: Track armor points, encumbrance, and coverage
- **Ammunition**: Manage arrows, bullets, and other consumables
- **Trappings**: General equipment and inventory items

#### Character Progression
- **Experience Points**: Track and spend XP for character advancement
- **Skill Improvements**: Increase skill levels and unlock new abilities
- **Talent Acquisition**: Add new talents and special abilities

### Party Management

The application supports party-wide resource tracking:

1. **Party Ledger**: Shared inventory for group equipment
2. **Financial Tracking**: Manage party funds and expenses
3. **Resource Sharing**: Track communal supplies and equipment

## Docker Commands Reference

### Basic Operations
```bash
# Start the application
docker compose up -d

# Stop the application
docker compose down

# Restart the application
docker compose restart

# View logs
docker compose logs -f app

# Access container shell
docker compose exec app bash
```

### Database Management
```bash
# Run database migrations
docker compose exec app bash -c "./docker-entrypoint.sh migrate"

# Initialize a fresh database
docker compose exec app bash -c "./docker-entrypoint.sh init-db"

# Run custom alembic commands
docker compose exec app bash -c "./docker-entrypoint.sh alembic revision --autogenerate -m 'Your message'"

# Backup database
docker compose exec app bash -c "cp /app/instance/CharSheet_test.db /app/instance/backup_$(date +%Y%m%d_%H%M%S).db"
```

### Development Workflow
```bash
# Development mode with live reload
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Build new image after changes
docker compose build

# Reset and restart development environment
docker compose down
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode, `production` for deployment
- Database and logging paths are configured automatically

### Data Persistence
The application uses Docker volumes for data persistence:
- `charsheet_db`: Database files
- `charsheet_logs`: Application logs

### Port Configuration
Default port is 5000. To change:
```yaml
# In docker-compose.yml
ports:
  - "8080:5000"  # Changes external port to 8080
```

## Troubleshooting

### Common Issues

**Application won't start:**
```bash
# Check logs
docker compose logs app

# Verify Docker is running
sudo systemctl status docker

# Rebuild container
docker compose build --no-cache
```

**Database migration errors:**
```bash
# Reset database (WARNING: loses all data)
docker compose down
docker volume rm rpg_character_sheet_charsheet_db
docker compose up -d
```

**Permission issues:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x docker-entrypoint.sh
```

### Performance Optimization
- The application uses SQLite for simplicity, suitable for personal/small group use
- For larger deployments, consider switching to PostgreSQL (configuration included)
- Use production mode (`FLASK_ENV=production`) for better performance

## Development Notes

The application is built with:
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Alembic**: Database migrations
- **Waitress**: Production WSGI server
- **UV**: Python package management

For local development without Docker, ensure Python 3.12+ and UV are installed, then use the development commands in the docker-entrypoint.sh script.

## Support

For issues, questions, or contributions, please refer to the project repository or documentation. The application is designed to be self-contained and should work out of the box with the provided Docker configuration.
