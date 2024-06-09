import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {   Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

function ProductionEvaluation() {
  const [metrics, setMetrics] = useState([]);
  const [gettingPredictions, setGettingPredictions] = useState(false);

  useEffect(() => {
    setGettingPredictions(true);
    fetch(`${process.env.REACT_APP_SERVE_URL}/production-evaluation`)
      .then((res) => res.json())
      .then((data) => {
        setGettingPredictions(false);
        console.log('data', data);
        setMetrics(data.metrics);
      })
      .catch((err) => {
        setGettingPredictions(false);
        console.error('Error fetching metrics', err);
      });
  }, []);

  // Extracting data for each metric
  const mseData = metrics.map((metric) => ({
    x: metric.end_time,
    y: metric.mse
  }));
  const evsData = metrics.map((metric) => ({
    x: metric.end_time,
    y: metric.evs
  }));
  const maeData = metrics.map((metric) => ({
    x: metric.end_time,
    y: metric.mae
  }));

  const reversedTimestamps = metrics
    .map((metric) => metric.end_time)
    .reverse();

  return (
    <div>
      <h2 className='text-2xl font-bold mb-4'>Production Evaluation</h2>
      {gettingPredictions && <p>Loading metrics...</p>}
      <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
        {/* MSE */}
        <div className='mb-8'>
          <h3 className='text-lg font-bold mb-2'>Mean Squared Error (MSE)</h3>
          <Line
            data={{
              labels: reversedTimestamps,
              datasets: [
                {
                  label: 'MSE',
                  data: mseData,
                  borderColor: 'rgb(0, 0, 255)',
                  fill: false,
                }
              ],
            }}
          />
        </div>

        {/* EVS */}
        <div className='mb-8'>
          <h3 className='text-lg font-bold mb-2'>Explained Variance Score (EVS)</h3>
          <Line
            data={{
              labels: reversedTimestamps,
              datasets: [
                {
                  label: 'EVS',
                  data: evsData,
                  borderColor: 'rgb(0, 0, 255)',
                  fill: false,
                }
              ],
            }}
          />
        </div>

        {/* MAE */}
        <div className='mb-8'>
          <h3 className='text-lg font-bold mb-2'>Mean Absolute Error (MAE)</h3>
          <Line
            data={{
              labels: reversedTimestamps,
              datasets: [
                {
                  label: 'MAE',
                  data: maeData,
                  borderColor: 'rgb(0, 0, 255)',
                  fill: false,
                }
              ],
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default ProductionEvaluation;
