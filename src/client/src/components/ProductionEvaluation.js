import React, { useEffect, useState } from 'react';

function ProductionEvaluation() {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    fetch(`https://${process.env.REACT_APP_SERVE_URL}/production-evaluation`)
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
      <h2 className='text-2xl font-bold mb-4'>Production Evaluation</h2>
    </div>
  );
}

export default ProductionEvaluation;
