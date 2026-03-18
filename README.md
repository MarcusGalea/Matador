# Matador
A web-based Matador game built with Laravel, React/Inertia and a Python game engine.

# Installation
## Prerequisites

Before starting, install:

- Git
- Docker (Desktop)
- Composer
- WSL2 (if using Windows)
- PHP (optional, only if not using Sail)
- Node.js + npm

## Procedure
### 1. Clone the repository

```bash
git clone https://github.com/MarcusGalea/Matador.git
cd Matador
```

### 2. Copy environment variable
cp .env.example .env

### 3. Install dependencies
composer install
npm install

### 4. Build assets and install dependencies
npm install && npm run build
composer install

### 5. Start Docker containers
Make sure Docker is running, then run the command:
./vendor/bin/sail up -d

### 6. Run database migrations and seeders
./vendor/bin/sail artisan migrate --seed

### 7. Run the Laravel development server
./vendor/bin/sail composer run dev

### 8. Access the application
Open your web browser and navigate to http://localhost:80 (or whichever port was binded in compose.yml) to access the Matador game.