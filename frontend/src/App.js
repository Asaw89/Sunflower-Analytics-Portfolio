import React, { useState, useEffect, useMemo } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import Plot from 'react-plotly.js';
import ChatInterface from './components/ChatInterface';
import LandingPage from './components/landingpage';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Dashboard Component (your existing code)
function Dashboard() {
  const [genresData, setGenresData] = useState([]);
  const [subscribersData, setSubscribersData] = useState([]);
  const [topArtistsData, setTopArtistsData] = useState([]);
  const [risingArtistsData, setRisingArtistsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [genres, subscribers, topArtists, risingArtists] = await Promise.all([
        axios.get(`${API_URL}/api/genres/by-region`),
        axios.get(`${API_URL}/api/subscribers/by-region`),
        axios.get(`${API_URL}/api/artists/top?limit=10`),
        axios.get(`${API_URL}/api/artists/rising?limit=10`)
      ]);

      setGenresData(genres.data);
      setSubscribersData(subscribers.data);
      setTopArtistsData(topArtists.data);
      setRisingArtistsData(risingArtists.data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const genresChart = useMemo(() => {
    if (genresData.length === 0) return null;
    
    const regions = [...new Set(genresData.map(d => d.region))];
    const genres = [...new Set(genresData.map(d => d.genre))];

    const traces = genres.map(genre => ({
      x: regions,
      y: regions.map(region => {
        const item = genresData.find(d => d.region === region && d.genre === genre);
        return item ? item.stream_count : 0;
      }),
      name: genre,
      type: 'bar'
    }));

    return {
      data: traces,
      layout: {
        title: 'Genre Distribution by Region',
        barmode: 'stack',
        xaxis: { title: 'Region' },
        yaxis: { title: 'Stream Count' }
      }
    };
  }, [genresData]);

  const subscribersChart = useMemo(() => {
    if (subscribersData.length === 0) return null;
    
    const regions = [...new Set(subscribersData.map(d => d.region))];
    
    const paidData = regions.map(region => {
      const item = subscribersData.find(d => d.region === region && d.level === 'paid');
      return item ? item.user_count : 0;
    });

    const freeData = regions.map(region => {
      const item = subscribersData.find(d => d.region === region && d.level === 'free');
      return item ? item.user_count : 0;
    });

    return {
      data: [
        {
          x: regions,
          y: paidData,
          name: 'Paid',
          type: 'bar',
          marker: { color: '#4CAF50' }
        },
        {
          x: regions,
          y: freeData,
          name: 'Free',
          type: 'bar',
          marker: { color: '#2196F3' }
        }
      ],
      layout: {
        title: 'Subscribers by Region (Paid vs Free)',
        barmode: 'group',
        xaxis: { title: 'Region' },
        yaxis: { title: 'User Count' }
      }
    };
  }, [subscribersData]);

  const topArtistsChart = useMemo(() => {
    if (topArtistsData.length === 0) return null;
    
    return {
      data: [{
        x: topArtistsData.map(a => a.artist),
        y: topArtistsData.map(a => a.stream_count),
        type: 'bar',
        marker: { color: '#FF5722' }
      }],
      layout: {
        title: 'Top 10 Artists by Streams',
        xaxis: { title: 'Artist', tickangle: -45 },
        yaxis: { title: 'Stream Count' }
      }
    };
  }, [topArtistsData]);

  const risingArtistsChart = useMemo(() => {
    if (risingArtistsData.length === 0) return null;
    
    return {
      data: [{
        x: risingArtistsData.map(a => a.artist),
        y: risingArtistsData.map(a => a.growth_rate),
        type: 'bar',
        marker: { color: '#9C27B0' },
        text: risingArtistsData.map(a => `${a.growth_rate.toFixed(1)}%`),
        textposition: 'auto'
      }],
      layout: {
        title: 'Rising Artists by Growth Rate',
        xaxis: { title: 'Artist', tickangle: -45 },
        yaxis: { title: 'Growth Rate (%)' }
      }
    };
  }, [risingArtistsData]);

  if (loading) {
    return (
      <div className="App">
        <nav className="main-nav">
          <Link to="/" className="nav-link">🏠 Home</Link>
          <Link to="/dashboard" className="nav-link">📊 Dashboard</Link>
          <Link to="/chat" className="nav-link">💬 AI Chat</Link>
        </nav>
        <header className="App-header">
          <h1>Sunflower Analytics</h1>
        </header>
        <div className="loading">Loading data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <nav className="main-nav">
          <Link to="/" className="nav-link">🏠 Home</Link>
          <Link to="/dashboard" className="nav-link">📊 Dashboard</Link>
          <Link to="/chat" className="nav-link">💬 AI Chat</Link>
        </nav>
        <header className="App-header">
          <h1>Sunflower Analytics</h1>
        </header>
        <div className="error">
          <p>Error loading data: {error}</p>
          <button onClick={fetchData}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <nav className="main-nav">
        <Link to="/" className="nav-link">🏠 Home</Link>
        <Link to="/dashboard" className="nav-link">📊 Dashboard</Link>
        <Link to="/chat" className="nav-link">💬 AI Chat</Link>
      </nav>
      <header className="App-header">
        <h1>🎵 Sunflower Analytics</h1>
        <p>Music Streaming Analytics Dashboard</p>
      </header>
      
      <div className="dashboard">
        <div className="chart-container">
          {genresChart && (
            <Plot
              data={genresChart.data}
              layout={genresChart.layout}
              config={{ responsive: true }}
              style={{ width: '100%', height: '100%' }}
            />
          )}
        </div>

        <div className="chart-container">
          {subscribersChart && (
            <Plot
              data={subscribersChart.data}
              layout={subscribersChart.layout}
              config={{ responsive: true }}
              style={{ width: '100%', height: '100%' }}
            />
          )}
        </div>

        <div className="chart-container">
          {topArtistsChart && (
            <Plot
              data={topArtistsChart.data}
              layout={topArtistsChart.layout}
              config={{ responsive: true }}
              style={{ width: '100%', height: '100%' }}
            />
          )}
        </div>

        <div className="chart-container">
          {risingArtistsChart && (
            <Plot
              data={risingArtistsChart.data}
              layout={risingArtistsChart.layout}
              config={{ responsive: true }}
              style={{ width: '100%', height: '100%' }}
            />
          )}
        </div>
      </div>

      <footer className="App-footer">
        <p>Powered by FastAPI, PostgreSQL, React, Plotly, and Ollama</p>
        <button onClick={fetchData} className="refresh-btn">🔄 Refresh Data</button>
      </footer>
    </div>
  );
}

// Main App with Routing
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/chat" element={
          <div className="App">
            <nav className="main-nav">
              <Link to="/" className="nav-link">🏠 Home</Link>
              <Link to="/dashboard" className="nav-link">📊 Dashboard</Link>
              <Link to="/chat" className="nav-link">💬 AI Chat</Link>
            </nav>
            <ChatInterface />
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;