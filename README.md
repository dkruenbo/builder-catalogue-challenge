# Brick Builder Catalogue

A FastAPI application with a minimal frontend that helps users discover which Brick sets they can build with their existing piece collection. Features both a simple web interface and comprehensive REST API.

## Features

- 🌐 **Simple Web Interface**: Clean, minimal frontend for easy user interaction
- 🔍 **Build Analysis**: Analyze any user's Brick collection to find buildable sets
- 📊 **Comprehensive Statistics**: Detailed inventory and build success metrics
- 🧱 **Complete API Coverage**: Full access to users, sets, and colors data
- 🎯 **Smart Matching**: Intelligent piece-to-set matching algorithm
- 🚀 **REST API**: Clean, documented JSON API endpoints
- 📋 **Type Safety**: Fully typed with Pydantic models

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the development server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage

### Web Interface

1. Open http://localhost:8000 in your browser
2. Enter a username (e.g., "arts-n-bricks") or click "Try This User" for available users
3. Click "Analyze Collection"
4. View results showing:
   - Collection statistics (total pieces, unique combinations)
   - Success rate and buildable set count
   - List of sets you can build with piece counts

## API Endpoints

### Default Endpoints (Direct API Mirror)

#### Users
- `GET /api/users` - Get all available users
- `GET /api/user/by-username/{username}` - Get user summary by username
- `GET /api/user/by-id/{user_id}` - Get full user data by ID

#### Sets
- `GET /api/sets` - Get all available sets
- `GET /api/set/by-name/{name}` - Get set summary by name
- `GET /api/set/by-id/{set_id}` - Get full set data by ID

#### Colors
- `GET /api/colours` - Get all available colors

### Brick Builder Catalogue Endpoints (Custom Logic)

#### Build Analysis
- `GET /api/user/{username}/builds` - Analyze which sets a user can build

## Usage Examples

### Get User Build Analysis
```bash
curl http://localhost:8000/api/user/arts-n-bricks/builds
```

Response:
```json
{
  "username": "arts-n-bricks",
  "total_pieces": 2140,
  "unique_combinations": 232,
  "total_sets": 15,
  "buildable_count": 3,
  "buildable_sets": [
    {
      "name": "undersea-monster",
      "pieces": 395,
      "set_number": "430XX"
    },
    {
      "name": "castaway", 
      "pieces": 450,
      "set_number": "306XX"
    }
  ]
}
```

### Get All Users
```bash
curl http://localhost:8000/api/users
```

### Get Specific Set Information
```bash
curl http://localhost:8000/api/set/by-name/alien-spaceship
```

## Technology Stack

- **Backend**: FastAPI (Python)
- **Type System**: Pydantic models
- **HTTP Client**: httpx (async)
- **External API**: Brick catalogue API (`https://d30r5p5favh3z8.cloudfront.net`)

## Project Structure

```
builder-catalogue-challenge/
├── main.py                 # FastAPI application launcher
├── app/                    # Application package
│   ├── router/
│   │   └── router.py      # API endpoints & frontend routes
│   ├── controllers/
│   │   └── controller.py  # Business logic orchestration
│   ├── functions/
│   │   └── functions.py   # Utility functions and API calls
│   └── models/
│       └── models.py      # Pydantic data models
├── templates/              # Jinja2 HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── results.html       # Analysis results
│   └── error.html         # Error page
├── static/
│   └── style.css          # CSS styling
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Architecture

The application follows a clean, modular architecture with both frontend and API:

- **`main.py`**: FastAPI app setup with static file mounting
- **`app/router/router.py`**: Frontend routes and API endpoint definitions
- **`app/controllers/controller.py`**: Business logic orchestration
- **`app/functions/functions.py`**: Pure utility functions for API calls
- **`app/models/models.py`**: Pydantic models for type safety
- **`templates/`**: Minimal Jinja2 templates for the web interface
- **`static/`**: CSS styling for the frontend

## Example Users

Try these example usernames:
- `arts-n-bricks` - User from FIH with 2,140 pieces
- `brickmaster2023` - Another available user

## Development

### Running with Auto-reload
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `httpx` - Async HTTP client
- `pydantic` - Data validation

### API Documentation

The API is fully documented with OpenAPI/Swagger. Visit `/docs` for interactive documentation or `/redoc` for alternative documentation format.

## License

MIT License