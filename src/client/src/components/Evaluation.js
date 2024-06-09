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

function Evaluation() {
  const [metrics, setMetrics] = useState([]);
  const [gettingPredictions, setGettingPredictions] = useState(false);

  useEffect(() => {
    setGettingPredictions(true);
    fetch(`${process.env.REACT_APP_SERVE_URL}/evaluation`)
      .then((res) => res.json())
      .then((data) => {
        setGettingPredictions(false);
        setMetrics(data.metrics);
      })
      .catch((err) => {
        setGettingPredictions(false);
        console.error('Error fetching metrics', err);
      });
  }, []);

  // Extracting data for each metric
  const mseProductionData = metrics.map((metric) => ({
    x: metric.end_time,
    y: metric.MSE_production
  }));
  const mseStagingData = metrics.map((metric) => ({
    x: metric.end_time,
    y: metric.MSE_staging
  }));

  const evsProductionData = metrics.map((metric) => ({
    x: metric.end_time,
    y: metric.EVS_production
  }));
  const evsStagingData = metrics.map((metric) => ({
    x: metric.end_time,
    y: metric.EVS_staging
  }));

  const maeProductionData = metrics.map((metric) => ({
    x: metric.end_time,
    y: metric.MAE_production
  }));
  const maeStagingData = metrics.map((metric) => ({
    x: metric.end_time,
    y: metric.MAE_staging
  }));

  const reversedTimestamps = metrics
    .map((metric) => metric.end_time)
    .reverse();

  return (
    <div>
      <h2 className='text-2xl font-bold mb-4'>Evaluation</h2>
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
                  label: 'Production',
                  data: mseProductionData,
                  borderColor: 'rgb(0, 0, 255)',
                  fill: false,
                },
                {
                  label: 'Staging',
                  data: mseStagingData,
                  borderColor: 'rgb(0, 255, 0)',
                  fill: false,
                },
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
                  label: 'Production',
                  data: evsProductionData,
                  borderColor: 'rgb(0, 0, 255)',
                  fill: false,
                },
                {
                  label: 'Staging',
                  data: evsStagingData,
                  borderColor: 'rgb(0, 255, 0)',
                  fill: false,
                },
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
                  label: 'Production',
                  data: maeProductionData,
                  borderColor: 'rgb(0, 0, 255)',
                  fill: false,
                },
                {
                  label: 'Staging',
                  data: maeStagingData,
                  borderColor: 'rgb(0, 255, 0)',
                  fill: false,
                },
              ],
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default Evaluation;
