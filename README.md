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

### 4. Start Docker containers
Make sure Docker is running, then run the command:
./vendor/bin/sail up -d

