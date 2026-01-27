# Quick Start Guide

Get Zip Listen Analytics up and running in under 5 minutes!

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) (includes Docker Compose)
- Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/CircusCircus-Sunflower/Zip-Listen-Analytics.git
cd Zip-Listen-Analytics
```

## Step 2: Start the Application

```bash
docker compose up -d
```

This command will:
1. Pull the PostgreSQL image
2. Build the FastAPI backend container
3. Build the React frontend container
4. Start all services
5. Initialize the database with sample data

**First-time startup takes 2-3 minutes** to build images and install dependencies.

## Step 3: Wait for Services to be Ready

Check the status of services:

```bash
docker compose ps
```

Wait until all services show "Up" or "healthy" status:

```
NAME                      STATUS              PORTS
ziplisten-backend         Up                  0.0.0.0:8000->8000/tcp
ziplisten-db             Up (healthy)        0.0.0.0:5432->5432/tcp
ziplisten-frontend       Up                  0.0.0.0:3000->3000/tcp
```

## Step 4: Access the Application

Open your web browser and navigate to:

### Frontend Dashboard
```
http://localhost:3000
```

You should see the Zip Listen Analytics dashboard with four interactive charts:
- Genre Distribution by Region
- Subscribers by Region (Paid vs Free)
- Top 10 Artists by Streams
- Rising Artists by Growth Rate

### Backend API Documentation
```
http://localhost:8000/docs
```

Interactive Swagger UI where you can test all API endpoints.

## Step 5: Test the API

Try these quick API tests in your terminal:

```bash
# Health check
curl http://localhost:8000/health

# Get all genres by region
curl http://localhost:8000/api/genres/by-region

# Get top 5 artists
curl http://localhost:8000/api/artists/top?limit=5

# Get rising artists
curl http://localhost:8000/api/artists/rising
```

## Common Commands

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

### Stop the Application

```bash
docker compose stop
```

### Start the Application (if already built)

```bash
docker compose start
```

### Restart Services

```bash
docker compose restart
```

### Rebuild and Restart (after code changes)

```bash
docker compose up -d --build
```

### Stop and Remove Everything

```bash
docker compose down

# Also remove volumes (database data)
docker compose down -v
```

## Troubleshooting

### Problem: Port Already in Use

If you see an error like "port is already allocated":

```bash
# Find what's using the port (example for port 8000)
lsof -i :8000

# Stop the conflicting service or change ports in docker-compose.yml
```

### Problem: Frontend Cannot Connect to Backend

1. Check if backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check backend logs:
   ```bash
   docker compose logs backend
   ```

3. Ensure CORS is properly configured in `backend/app/main.py`

### Problem: Database Connection Error

1. Check database status:
   ```bash
   docker compose ps db
   ```

2. Wait for database to be healthy:
   ```bash
   docker compose logs db | grep "ready to accept connections"
   ```

3. Restart the backend after database is ready:
   ```bash
   docker compose restart backend
   ```

### Problem: Frontend Shows White Screen

1. Check frontend logs:
   ```bash
   docker compose logs frontend
   ```

2. Verify frontend is running:
   ```bash
   curl http://localhost:3000
   ```

3. Clear browser cache and reload

## Next Steps

### Explore the Data

The database comes pre-loaded with sample data. View the data:

```bash
# Connect to PostgreSQL
docker compose exec db psql -U zipuser -d ziplistendb

# Run queries
\dt                          # List tables
SELECT COUNT(*) FROM listen_events;
SELECT * FROM listen_events LIMIT 5;
\q                           # Quit
```

### Add More Data

Edit `init_db.sql` to add more sample data, then recreate the database:

```bash
docker compose down -v
docker compose up -d
```

### Customize the Frontend

1. Edit files in `frontend/src/`
2. Changes will auto-reload (hot module replacement)
3. View changes at http://localhost:3000

### Modify API Endpoints

1. Edit files in `backend/app/api/`
2. Restart the backend:
   ```bash
   docker compose restart backend
   ```

### Connect Tableau

See [TABLEAU_GUIDE.md](TABLEAU_GUIDE.md) for detailed instructions on connecting Tableau to the PostgreSQL database.

## Development Mode (Without Docker)

If you prefer to run services locally without Docker:

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL separately or update DATABASE_URL
<<<<<<< HEAD
export DATABASE_URL="postgresql://zipuser:zippassword@localhost:5432/ziplistendb"
=======
export DATABASE_URL=""postgresql://sunflower_user:zipmusic@xo.zipcode.rocks:9088/sunflower""
>>>>>>> ce926f01fdf6ba5d4102e83dd8128365cbdc23ed

# Run the server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
export REACT_APP_API_URL="http://localhost:8000"
npm start
```

## Production Deployment

For production deployment, consider:

1. **Security**: 
   - Use environment variables for secrets
   - Enable HTTPS
   - Configure proper CORS origins
   - Implement authentication

2. **Performance**:
   - Add caching (Redis)
   - Use production WSGI server
   - Optimize database queries
   - Add indexes

3. **Monitoring**:
   - Add logging
   - Set up health checks
   - Monitor database performance

4. **Scaling**:
   - Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
   - Deploy backend to container platform (ECS, Kubernetes)
   - Host frontend on CDN (Cloudfront, Netlify)

## Support

For issues or questions:
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Review [README.md](README.md)
- Open an issue on GitHub

## Success! 🎉

You now have a fully functional music streaming analytics platform running locally!

Explore the interactive dashboard at http://localhost:3000 and the API at http://localhost:8000/docs.
