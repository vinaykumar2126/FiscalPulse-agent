import React, { useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import AuditForm from './components/AuditForm';
import Alert from './components/Alert';
import AuditResults from './components/AuditResults';
import Features from './components/Features';

function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/audit', {
        query: query
      });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <Header />
      <main className="main">
        <div className="container">
          <div className="card">
            <div className="card-head">
              <h1>FiscalPulse Audit Desk</h1>
              <p>Ask anything about your past purchases and get instant, AI-powered tax checks.</p>
            </div>
            <AuditForm
              query={query}
              setQuery={setQuery}
              handleSubmit={handleSubmit}
              loading={loading}
            />
            {error && <Alert type="error" icon="⚠️" message={error} />}
            <AuditResults result={result} />
          </div>
          <Features />
        </div>
      </main>
    </div>
  );
}

export default Home;