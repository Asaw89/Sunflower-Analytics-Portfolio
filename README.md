# Sunflower Analytics 🌻

An AI-powered music streaming analytics platform that enables natural language querying of music data using local LLMs. Ask questions like "Who is the top artist in California?" and get instant SQL-powered answers through Sol, your friendly AI assistant.

![Sunflower Analytics](screenshot.png)

## 🎯 Overview

Sunflower Analytics transforms complex music streaming data into actionable insights through conversational AI. Built on a foundation of robust data engineering and enhanced with Ollama/LLM integration, this platform demonstrates modern full-stack development with AI capabilities.

## ✨ Key Features

- **🤖 Natural Language Queries**: Ask questions in plain English, get SQL-powered answers
- **📊 Interactive Analytics Dashboard**: Real-time visualizations of music trends
- **🎵 Genre & Artist Analytics**: Track popularity across US regions
- **👥 Subscriber Metrics**: Compare paid vs free subscribers by region  
- **🌟 Rising Artists**: Identify trending artists based on growth rate
- **💬 AI Chat Interface**: Powered by Ollama with Llama 3.1 8B
- **🔒 Local-First**: Runs entirely on your machine, no external API keys needed

## 🏗️ Architecture
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   React     │────▶│   FastAPI    │────▶│ PostgreSQL  │
│  Frontend   │     │   Backend    │     │  Database   │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Ollama    │
                    │  (Llama 3.1) │
                    └──────────────┘
```

**Query Flow:**
1. User asks question in natural language
2. Ollama/Llama converts to SQL query
3. FastAPI executes query on PostgreSQL
4. Results formatted by Ollama into natural language
5. Answer displayed with optional SQL preview

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL 15**: Robust relational database
- **SQLAlchemy**: SQL toolkit and ORM
- **Ollama**: Local LLM runtime
- **psycopg2**: PostgreSQL adapter
- **Pandas**: Data manipulation and analysis
- **Python 3.11**

### Frontend
- **React**: JavaScript library for building user interfaces
- **React Router**: Client-side routing
- **Plotly.js**: Interactive visualization library
- **Axios**: HTTP client for API requests
- **Custom CSS**: Beautiful gradient design

### AI/ML
- **Llama 3.1 8B** (primary model for natural language processing)
- **CodeLlama 13B** (code generation and complex queries)
- **Phi3 Mini** (fast inference for simple queries)

### Infrastructure
- **Docker & Docker Compose**: Containerization and orchestration
- **Uvicorn**: ASGI server for FastAPI
- **Local development environment**

## 📊 Data Models

### Summary Tables
- **summary_artist_popularity_by_geo**: Artist popularity metrics by state
  - `artist`, `region_name`, `play_count`, `unique_listeners`, `last_updated`
  
- **summary_genre_by_region**: Genre distribution across regions
  - `genre`, `region_name`, `listen_count`, `last_updated`
  
- **summary_subscribers_by_region**: Subscriber metrics by region
  - `region_name`, `level` (paid/free), `subscriber_count`, `last_updated`

### Raw Event Tables
- **listen_events**: Music listening activity (297 MB)
- **auth_events**: User authentication events
- **page_view_events**: User page view tracking (355 MB)
- **status_change_events**: Subscription status changes

*Note: Raw event CSVs are kept local due to GitHub's 100MB file size limit*

## 🚀 Getting Started

### Prerequisites

- Docker Desktop
- Ollama ([install here](https://ollama.ai))
- 10GB+ free disk space
- Git

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/Asaw89/Sunflower-Analytics-Portfolio.git
   cd Sunflower-Analytics-Portfolio
```

2. **Download AI models**
```bash
   ollama pull llama3.1:8b
   ollama pull codellama:13b
   ollama pull phi3:mini
```

3. **Start Ollama server** (in separate terminal)
```bash
   ollama serve
```

4. **Start the application**
```bash
   docker-compose up --build
```

5. **Access the application**
   - Landing Page: http://localhost:3000
   - Dashboard: http://localhost:3000/dashboard
   - AI Chat: http://localhost:3000/chat
   - API Docs: http://localhost:8000/docs

### Data Setup

The database includes pre-populated summary tables with real music streaming analytics:
- **270,318 rows** in artist-region records
- **4,487 rows** in genre-region combinations  
- **9 regions** with subscriber metrics

Raw event data (600+ MB) is kept local for performance.

## 💬 Sample AI Queries

Try asking Sol:
- "Who is the top artist in New York?"
- "What are the top 5 genres in California?"
- "How many paid subscribers are there total?"
- "Show me the most popular artist in Texas"
- "Compare genres between CA and FL"

## 📡 API Endpoints

### Natural Language Query
**POST** `/api/ollama/ask`

Request:
```json
{
  "question": "Who is the top artist in California?"
}
```

Response:
```json
{
  "question": "Who is the top artist in California?",
  "sql": "SELECT artist FROM summary_artist_popularity_by_geo WHERE region_name = 'CA' ORDER BY play_count DESC LIMIT 1;",
  "answer": "The top artist in California is Drake with 45,231 plays.",
  "raw_data": [{"artist": "Drake"}]
}
```

### Analytics Endpoints

**GET** `/api/genres/by-region` - Genre distribution by region
**GET** `/api/subscribers/by-region` - Subscriber metrics  
**GET** `/api/artists/top?limit=10` - Top artists by streams
**GET** `/api/artists/rising?limit=10` - Rising artists by growth rate

Full API documentation at `/docs` when running.

## 🗺️ US Region Mapping

- **Northeast**: CT, ME, MA, NH, RI, VT, NJ, NY, PA
- **Southeast**: DE, FL, GA, MD, NC, SC, VA, WV, AL, KY, MS, TN, AR, LA, TX
- **Midwest**: IL, IN, MI, OH, WI, IA, KS, MN, MO, NE, ND, SD
- **West**: AZ, CO, ID, MT, NV, NM, UT, WY, AK, CA, HI, OR, WA

## 📈 Data Visualizations

The React frontend provides interactive visualizations:
- **Stacked Bar Chart**: Genre distribution by region
- **Grouped Bar Chart**: Paid vs free subscribers by region
- **Bar Chart**: Top 10 artists by stream count
- **Bar Chart**: Rising artists with growth rates

## 🎓 Project Background

This project was built as part of my Data Engineering Fellowship at **Zip Code Wilmington** (January 2026). It demonstrates full-stack development, database design, data engineering pipelines, and AI integration skills for real-world analytics applications.

### Original Team Project
**Sunflower Analytics** (originally "Zip Listen Analytics") was developed as a team capstone project to create a comprehensive music streaming analytics platform for data-driven decision making.

**Team Members & Contributions:**
- **Ieshia Miles**: Database architect and data engineer
  - Designed and created all summary tables from raw event data
  - Built data aggregation pipelines for artist popularity, genre trends, and subscriber metrics
  - Processed 3+ million streaming records into optimized summary tables
  
- **Jude Nelson**: Creative director and brand designer  
  - Created Sol, the sunflower mascot character and logo
  - Designed original brand identity and visual assets
  - Contributed to UI/UX concept development

- **Alan Saw**: Infrastructure lead and full-stack developer
  - Project infrastructure and Docker containerization
  - Database setup and PostgreSQL configuration
  - Data ingestion and ETL pipeline development
  - Team coordination and project management

### Portfolio Enhancements
This portfolio version extends the original team project with significant AI capabilities:

**New Features Added:**
- ✨ **Ollama/LLM Integration**: Natural language query system using Llama 3.1 8B
- 🎨 **Enhanced Landing Page**: Modern UI showcasing Sol mascot with gradient design
- 🔌 **REST API Expansion**: `/api/ollama/ask` endpoint for AI-powered queries
- 🐳 **Local Database Setup**: Fully containerized development environment
- 📊 **270K+ Record Import**: Imported all summary tables for local analytics
- 🧠 **Multi-Model AI**: Integration of 3 specialized LLMs for different query types

**Technical Skills Demonstrated:**
- Full-stack development (React, FastAPI, PostgreSQL)
- AI/LLM integration and prompt engineering
- Database design and optimization
- Docker containerization and orchestration
- API development and documentation
- Data engineering and ETL pipelines
- Problem-solving under time constraints

## 🔮 Future Enhancements

- [ ] Add user authentication and authorization
- [ ] Implement query result caching for performance
- [ ] Add data visualizations within AI chat responses
- [ ] Support for time-series analysis and trending queries
- [ ] Voice input integration for hands-free queries
- [ ] Real-time streaming data ingestion
- [ ] Deploy to cloud (AWS/Azure) with CI/CD pipeline

## 🧪 Testing

Test the API endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Natural language query
curl -X POST http://localhost:8000/api/ollama/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Who is the top artist in NY?"}'

# Get genres by region
curl http://localhost:8000/api/genres/by-region

# Get top artists
curl http://localhost:8000/api/artists/top?limit=5
```

## 📧 Contact

**Alan Saw**  
Data Engineering Fellow | Full-Stack Developer

- GitHub: [@Asaw89](https://github.com/Asaw89)
- LinkedIn: [linkedin.com/in/alansaw](https://linkedin.com/in/alansaw)
- Email: alansaw89@gmail.com
- Portfolio: [github.com/Asaw89/Sunflower-Analytics-Portfolio](https://github.com/Asaw89/Sunflower-Analytics-Portfolio)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Zip Code Wilmington** for the intensive Data Engineering Fellowship program
- **Ieshia Miles** for exceptional database design and data engineering work
- **Jude Nelson** for creative vision and Sol mascot design
- **Anthropic** for Claude AI assistance during development
- **Ollama team** for making local LLMs accessible and developer-friendly
- **FastAPI, React, and PostgreSQL** communities for excellent documentation

---

Built with dockers and 🌻 by Alan Saw | Data Engineering Portfolio 2026