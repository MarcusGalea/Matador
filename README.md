# Matador
A web-based Matador game built with Laravel, React/Inertia and a Python game engine.

# Installation
## Prerequisites

Before starting, install:

- Git
- Docker (Desktop)
- Composer
- WSL2 (if using Windows)
- Node.js + npm

Make sure to run either on Linux or WSL2 on Windows, and to have Docker running at all times

easy bash command to install php and composer on Linux / WSL2:
```
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

## Procedure
### 1. Clone the repository

```bash
git clone https://github.com/MarcusGalea/Matador.git
cd Matador
```

### 2. Setting up environment variables
```bash
cp .env.example .env
```

You can run the following command to generate an application key, which is required for Laravel to function properly:
```bash
php artisan key:generate
```

Install composer dependencies:
```bash
composer install
```

Now you can edit the .env file to set up your database connection and other environment variables. 
```bash
php artisan sail:install
```

Make sure to set the database connection to match the one defined in your Docker Compose file (e.g., DB_HOST=pgsql, DB_DATABASE=matador, DB_USERNAME=sail, DB_PASSWORD=password).

### 3. Install frontend dependencies and build assets
```bash
npm install && npm run build 
```

### 4. Start Docker containers
Make sure Docker is running, then run the command:
```bash
./vendor/bin/sail up -d
```

### 5. Run database migrations and seeders
```bash
./vendor/bin/sail artisan migrate --seed
```

### 6. Run the Laravel development server
```bash
./vendor/bin/sail composer run dev
```

### 7. Access the application
Open your web browser and navigate to http://localhost:80 (or whichever port was binded in compose.yml) to access the Matador application. You should see the homepage where you can register a new account or log in with existing credentials.