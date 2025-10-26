# Brick Builder Catalogue

A FastAPI application with a comprehensive web interface that helps users discover which Brick sets they can build with their existing piece collection. Features both a full-featured frontend and comprehensive REST API, including collaboration tools for group building projects.

## Features

- 🌐 **Complete Web Interface**: User-friendly interface with search, analysis, and collaboration features
- 🔍 **Build Analysis**: Analyze any user's Brick collection to find buildable sets
- 🤝 **Collaboration Tools**: Find other users to collaborate with for sets you can't build alone
- 🧱 **Detailed Piece Visualization**: View actual brick images and detailed requirements
- 📊 **Comprehensive Statistics**: Detailed inventory and build success metrics
- 🎯 **Smart Matching**: Intelligent piece-to-set matching algorithm
- 🚀 **REST API**: Clean, documented JSON API endpoints
- 📋 **Type Safety**: Fully typed with Pydantic models
- 📱 **Responsive Design**: Works on desktop and mobile devices

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

1. **Home Page**: Open http://localhost:8000 in your browser
2. **User Selection**: 
   - Enter a username manually (e.g., "arts-n-bricks")
   - Or select from the dropdown of available users
3. **Analysis Results**: View comprehensive build analysis including:
   - Collection statistics (total pieces, unique combinations)
   - Buildable sets with piece counts and set numbers
   - Sets you can't build (with missing piece information)
4. **Detailed Build View**: Click on any set to see:
   - Visual piece requirements with actual brick images
   - Color-coded availability (green = sufficient, red = insufficient)
   - Exact piece counts needed vs. available
5. **Collaboration**: For unbuildable sets, find collaboration partners:
   - Click "🤝 Find Collaboration Partners" 
   - View team combinations that can complete the build
   - See each collaborator's contribution details

## API Endpoints

### Frontend Routes
- `GET /` - Home page with user search
- `POST /analyze` - Analyze user collection (form submission)
- `GET /set/{set_id}/build/{username}` - Detailed build requirements
- `GET /set/{set_id}/collaborate/{username}` - Collaboration options

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
- `GET /api/set/{set_id}/collaborate/{username}` - Find collaboration partners for a set

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
  "unbuildable_count": 12,
  "buildable_sets": [
    {
      "id": "67b0f662-eb4a-4fce-8e0d-29a776c142f2",
      "name": "coffee-bar",
      "pieces": 395,
      "set_number": "430XX"
    }
  ],
  "unbuildable_sets": [
    {
      "id": "f5c8e2a1-9b3d-4c6e-8f1a-2d4b7e9c0a5f", 
      "name": "alien-spaceship",
      "pieces": 450,
      "set_number": "306XX"
    }
  ]
}
```

### Get Collaboration Partners
```bash
curl http://localhost:8000/api/set/f5c8e2a1-9b3d-4c6e-8f1a-2d4b7e9c0a5f/collaborate/arts-n-bricks
```

### Get All Users
```bash
curl http://localhost:8000/api/users
```

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Jinja2 templates with vanilla CSS/JavaScript
- **Type System**: Pydantic models with full validation
- **HTTP Client**: httpx (async)
- **External APIs**: 
  - Brick catalogue API (`https://d30r5p5favh3z8.cloudfront.net`)
  - BrickLink images (`https://img.bricklink.com`)

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
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Home page with user search
│   ├── results.html       # Analysis results page
│   ├── set-build.html     # Detailed build requirements
│   ├── collaborate.html   # Collaboration options
│   └── error.html         # Error page
├── static/
│   └── style.css          # Responsive CSS styling
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Architecture

The application follows a clean, layered architecture:

### **Data Access Layer** (`app/functions/functions.py`):
- Pure API wrapper functions
- Data transformation utilities
- Stateless helper functions
- External service integrations

### **Business Logic Layer** (`app/controllers/controller.py`):
- Complex workflow orchestration
- Domain-specific algorithms (collaboration matching)
- Data aggregation and analysis
- Business rule enforcement

### **Presentation Layer** (`app/router/router.py`):
- HTTP endpoint definitions
- Request/response handling
- Frontend route management
- API documentation

### **Frontend**:
- **Templates**: Server-side rendered Jinja2 with clean HTML structure
- **Styling**: Responsive CSS with mobile-first design
- **Interactivity**: Vanilla JavaScript for enhanced UX

## Key Features Explained

### **Build Analysis**
- Compares user inventory against set requirements
- Identifies buildable vs. unbuildable sets
- Provides detailed piece-by-piece analysis
- Color-coded visualization of availability

### **Collaboration System**
- Finds users whose combined inventories can complete sets
- Prevents overlapping team suggestions
- Prioritizes smaller teams over larger ones
- Shows individual contribution details

### **Visual Piece Display**
- Integrates with BrickLink image API
- Shows actual brick photos when available
- Graceful fallback with emoji for missing images
- Responsive image sizing and layout

## Example Users

Try these example usernames:
- `arts-n-bricks` - User from FIH with 2,140 pieces
- `brickmaster2023` - Another available user
- Use the dropdown on the home page to see all available users

## Development

### Running with Auto-reload
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Dependencies
- `fastapi` - Web framework and API server
- `uvicorn` - ASGI server for development
- `httpx` - Async HTTP client for external APIs
- `pydantic` - Data validation and serialization
- `jinja2` - Template engine for frontend
- `python-multipart` - Form data handling

### API Documentation

The API is fully documented with OpenAPI/Swagger. Visit `/docs` for interactive documentation or `/redoc` for alternative documentation format.

### Code Quality
- **Type Safety**: Full typing with Pydantic models
- **Error Handling**: Comprehensive exception handling
- **Clean Architecture**: Clear separation of concerns
- **Modular Design**: Reusable, testable components

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes following the existing architecture
4. Test thoroughly with the development server
5. Submit a pull request with clear description

## License

MIT License