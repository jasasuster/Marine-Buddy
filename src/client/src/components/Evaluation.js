import React, { useEffect, useState } from 'react';

function Evaluation() {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    fetch(`https://${process.env.REACT_APP_SERVE_URL}/evaluation`)
      .then((res) => res.json())
      .then((data) => {
        setMetrics(data.metrics);
      })
      .catch((err) => {
        console.error('Error fetching metrics', err);
      });
  }, []);

  return (
    <div>
      <h2 className='text-2xl font-bold mb-4'>Evaluation</h2>
    </div>
  );
}

export default Evaluation;
