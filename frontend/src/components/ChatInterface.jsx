import { useState } from 'react';
import './ChatInterface.css';

function ChatInterface() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
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
        text: 'Sorry, I encountered an error processing your question. Please try again.'
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

  const exampleQuestions = [
    "Who is the top artist in New York?",
    "What are the top 5 genres in California?",
    "How many paid subscribers are there?",
    "Show me the most popular artist in Texas"
  ];

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>🎵 Ask About Music Data</h2>
        <p>Ask questions in natural language about artists, genres, and subscribers</p>
      </div>

      {messages.length === 0 && (
        <div className="example-questions">
          <p>Try asking:</p>
          {exampleQuestions.map((q, idx) => (
            <button 
              key={idx} 
              className="example-btn"
              onClick={() => setQuestion(q)}
            >
              {q}
            </button>
          ))}
        </div>
      )}

      <div className="messages-container">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            {msg.type === 'user' && (
              <div className="message-content">
                <strong>You:</strong>
                <p>{msg.text}</p>
              </div>
            )}
            
            {msg.type === 'assistant' && (
              <div className="message-content">
                <strong>AI Assistant:</strong>
                <p>{msg.text}</p>
                
                {msg.sql && (
                  <details className="sql-details">
                    <summary>View SQL Query</summary>
                    <pre><code>{msg.sql}</code></pre>
                  </details>
                )}
                
                {msg.data && msg.data.length > 0 && (
                  <details className="data-details">
                    <summary>View Raw Data ({msg.data.length} rows)</summary>
                    <pre><code>{JSON.stringify(msg.data, null, 2)}</code></pre>
                  </details>
                )}
              </div>
            )}
            
            {msg.type === 'error' && (
              <div className="message-content error">
                <strong>Error:</strong>
                <p>{msg.text}</p>
              </div>
            )}
          </div>
        ))}
        
        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <strong>AI Assistant:</strong>
              <p className="typing-indicator">Thinking...</p>
            </div>
          </div>
        )}
      </div>

      <div className="input-container">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question... (e.g., 'Who is the top artist in California?')"
          disabled={loading}
          rows={2}
        />
        <button 
          onClick={askQuestion} 
          disabled={loading || !question.trim()}
          className="send-btn"
        >
          {loading ? '⏳' : '📤'} {loading ? 'Processing...' : 'Ask'}
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;