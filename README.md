# Zip Listen Analytics

Data Pipeline and Visualizations to present to Zip Listen executives.

A comprehensive music streaming analytics platform built with FastAPI, PostgreSQL, React, Docker, Pandas, and Plotly.

## 🎵 Features

- **Genre Analytics by Region**: View genre distribution across US regions (Northeast, Southeast, Midwest, West)
- **Subscriber Analytics**: Compare paid vs free subscribers by region
- **Top Artists**: Track most-streamed artists
- **Rising Artists**: Identify trending artists based on growth rate

## 🏗️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: SQL toolkit and ORM
- **Pandas**: Data manipulation and analysis
- **Python 3.11**

### Frontend
- **React**: JavaScript library for building user interfaces
- **Plotly.js**: Interactive visualization library
- **Axios**: HTTP client for API requests

### Infrastructure
- **Docker & Docker Compose**: Containerization and orchestration
- **Uvicorn**: ASGI server for FastAPI

## 📊 Data Models

### Listen Events
- `artist`: Artist name
- `song`: Song title
- `duration`: Song duration in seconds
- `userId`: User identifier
- `state`: US state code
- `level`: Subscription level (paid/free)
- `genre`: Music genre
- `timestamp`: Event timestamp

### Auth Events
- `success`: Authentication success status
- `userId`: User identifier
- `state`: US state code
- `timestamp`: Event timestamp

### Status Change Events
- `level`: Subscription level (paid/free)
- `userId`: User identifier
- `state`: US state code
- `timestamp`: Event timestamp

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/CircusCircus-Sunflower/Zip-Listen-Analytics.git
   cd Zip-Listen-Analytics
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend Dashboard: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup (without Docker)

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
<<<<<<< HEAD
   export DATABASE_URL="postgresql://zipuser:zippassword@localhost:5432/ziplistendb"
=======
   export DATABASE_URL=""postgresql://sunflower_user:zipmusic@xo.zipcode.rocks:9088/sunflower""
>>>>>>> ce926f01fdf6ba5d4102e83dd8128365cbdc23ed
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   export REACT_APP_API_URL="http://localhost:8000"
   ```

4. **Run the application**
   ```bash
   npm start
   ```

## 📡 API Endpoints

### GET /api/genres/by-region
Get genre distribution by US region.

**Query Parameters:**
- `region` (optional): Filter by specific region (Northeast, Southeast, Midwest, West)

**Response:**
```json
[
  {
    "region": "Northeast",
    "genre": "Pop",
    "stream_count": 150
  }
]
```

### GET /api/subscribers/by-region
Get subscriber distribution (paid vs free) by US region.

**Query Parameters:**
- `region` (optional): Filter by specific region

**Response:**
```json
[
  {
    "region": "Northeast",
    "level": "paid",
    "user_count": 50
  }
]
```

### GET /api/artists/top
Get top artists by total stream count.

**Query Parameters:**
- `limit` (optional, default: 10): Number of top artists to return (1-100)

**Response:**
```json
[
  {
    "artist": "Taylor Swift",
    "stream_count": 500,
    "rank": 1
  }
]
```

### GET /api/artists/rising
Get rising artists based on growth rate.

**Query Parameters:**
- `limit` (optional, default: 10): Number of rising artists to return (1-100)

**Response:**
```json
[
  {
    "artist": "NewArtist1",
    "growth_rate": 150.5,
    "current_streams": 100,
    "previous_streams": 40
  }
]
```

## 🗺️ US Region Mapping

- **Northeast**: CT, ME, MA, NH, RI, VT, NJ, NY, PA
- **Southeast**: DE, FL, GA, MD, NC, SC, VA, WV, AL, KY, MS, TN, AR, LA, TX
- **Midwest**: IL, IN, MI, OH, WI, IA, KS, MN, MO, NE, ND, SD
- **West**: AZ, CO, ID, MT, NV, NM, UT, WY, AK, CA, HI, OR, WA

## 🧪 Testing

The application includes sample data that is automatically loaded when the database is initialized.

To test the API endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Get genres by region
curl http://localhost:8000/api/genres/by-region

# Get top artists
curl http://localhost:8000/api/artists/top?limit=5
```

## 📈 Data Visualization

The React frontend provides interactive visualizations using Plotly:
- **Stacked Bar Chart**: Genre distribution by region
- **Grouped Bar Chart**: Paid vs free subscribers by region
- **Bar Chart**: Top 10 artists by stream count
- **Bar Chart**: Rising artists with growth rates

## 🔧 Configuration

### Environment Variables

**Backend (`backend/.env`):**
```
DATABASE_URL=postgresql://zipuser:zippassword@db:5432/ziplistendb
```

**Frontend (`frontend/.env`):**
```
REACT_APP_API_URL=http://localhost:8000
```

## 📝 Database Schema

The database is automatically initialized with the following tables:
- `listen_events`: Music listening activity
- `auth_events`: User authentication events
- `status_change_events`: Subscription status changes

Sample data is included for immediate testing and demonstration.

## 🐳 Docker Services

- **db**: PostgreSQL 15 database
- **backend**: FastAPI application
- **frontend**: React application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Plotly for powerful visualization capabilities
- React team for the robust frontend library
