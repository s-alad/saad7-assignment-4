import React, { useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart, BarElement, CategoryScale, LinearScale } from 'chart.js';

Chart.register(BarElement, CategoryScale, LinearScale);

interface Result {
  rank: number;
  document: string;
  score: number;
}

const App: React.FC = () => {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<Result[]>([]);
  const [error, setError] = useState<string>('');

  const handleSearch = async () => {
    if (!query) {
      setError('Please enter a query');
      return;
    }
    setError('');
    try {
      const response = await axios.post('/search', { query });
      setResults(response.data.results);
    } catch (err) {
      console.error(err);
      setError('An error occurred during search');
    }
  };

  const data = {
    labels: results.map((result) => `Doc ${result.rank}`),
    datasets: [
      {
        label: 'Cosine Similarity',
        data: results.map((result) => result.score),
        backgroundColor: 'rgba(75,192,192,0.6)',
      },
    ],
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>LSA Search Engine</h1>
      <input
        type="text"
        value={query}
        placeholder="Enter your query"
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: '300px', marginRight: '10px' }}
      />
      <button onClick={handleSearch}>Search</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {results.length > 0 && (
        <div>
          <h2>Top 5 Documents</h2>
          {results.map((result) => (
            <div key={result.rank} style={{ marginBottom: '20px' }}>
              <h3>Document {result.rank}</h3>
              <p>Similarity Score: {result.score.toFixed(4)}</p>
              <p>{result.document.substring(0, 300)}...</p>
            </div>
          ))}
          <h2>Similarity Bar Chart</h2>
          <Bar data={data} />
        </div>
      )}
    </div>
  );
};

export default App;
