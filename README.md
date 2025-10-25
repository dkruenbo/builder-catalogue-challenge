# Brick Builder Catalogue API

A FastAPI backend application that helps users discover which Brick sets they can build with their existing piece collection. This API provides both direct access to the external brick catalogue and custom business logic for build analysis.

## Features

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
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

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
│   │   └── router.py      # API endpoint definitions
│   ├── controllers/
│   │   └── controller.py  # Business logic orchestration
│   ├── functions/
│   │   └── functions.py   # Utility functions and API calls
│   └── models/
│       └── models.py      # Pydantic data models
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Architecture

The application follows a clean, modular architecture organized in an `app` package:

- **`main.py`**: Minimal FastAPI app setup and startup
- **`app/router/router.py`**: HTTP endpoint definitions with proper tags and documentation
- **`app/controllers/controller.py`**: Business logic that orchestrates functions for complex operations
- **`app/functions/functions.py`**: Pure utility functions for API calls and data processing
- **`app/models/models.py`**: Pydantic models for type safety and validation

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