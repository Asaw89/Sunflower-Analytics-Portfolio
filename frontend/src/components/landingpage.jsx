import { useState } from 'react';
import './landingpage.css';
import solLogo from '../assets/sol-logo.png';

function LandingPage() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    
    // Add user message
    const userMessage = { type: 'user', text: question };
    setMessages(prev => [...prev, userMessage]);
    
    try {
      const response = await fetch('http://localhost:8000/api/ollama/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      
      const data = await response.json();
      
      // Add AI response
      setMessages(prev => [...prev, {
        type: 'assistant',
        text: data.answer,
        sql: data.sql,
        data: data.raw_data
      }]);
      
    } catch (error) {
      setMessages(prev => [...prev, {
        type: 'error',
        text: 'Sorry, I encountered an error. Please try again.'
      }]);
    }
    
    setQuestion('');
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="landing-page">
      <nav className="landing-nav">
        <div className="nav-logo">🌻</div>
        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#pricing">Pricing</a>
          <a href="#about">About</a>
          <a href="#contact">Contact</a>
        </div>
        <button className="sign-in-btn">Sign In</button>
      </nav>

      <div className="hero-section">
        <h1 className="hero-title">Sunflower Analytics</h1>
        <p className="hero-subtitle">
          Meet Sol.. Your friendly AI assistant for smarter analytics 🌻
        </p>

        <div className="sol-logo-container">
          <img src={solLogo} alt="Sol - Sunflower Analytics Mascot" className="sol-logo" />
        </div>

        {/* Messages Area - Shows when there are messages */}
        {messages.length > 0 && (
          <div className="messages-area">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.type}`}>
                {msg.type === 'user' && (
                  <div className="message-bubble user-bubble">
                    <strong>You:</strong> {msg.text}
                  </div>
                )}

                {msg.type === 'assistant' && (
                  <div className="message-bubble assistant-bubble">
                    <strong>Sol:</strong> {msg.text}
                    {msg.sql && (
                      <details className="sql-details">
                        <summary>View SQL</summary>
                        <pre><code>{msg.sql}</code></pre>
                      </details>
                    )}
                  </div>
                )}
                
                {msg.type === 'error' && (
                  <div className="message-bubble error-bubble">
                    {msg.text}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        <div className="chat-input-container">
          <input 
            type="text" 
            placeholder="Hi there! I'm Sol... how can I assist you today?"
            className="landing-chat-input"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
          />
          <button 
            className="send-btn-landing" 
            onClick={askQuestion}
            disabled={loading || !question.trim()}
          >
            {loading ? 'Thinking...' : 'Send'}
          </button>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">💡</div>
            <h3>Instant Insights</h3>
            <p>Ask questions in plain English and get fast answers.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Powerful Analytics</h3>
            <p>Built for streaming metrics: artists, genres, growth, retention.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>Secure & Private</h3>
            <p>Keep data protected with simple, safe backend patterns.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;