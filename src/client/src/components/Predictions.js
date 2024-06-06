import React, { useEffect, useState } from 'react';

function Predictions({ seaPointNumber }) {
  const [predictions, setPredictions] = useState([]);
  const [isLoadingPredictions, setIsLoadingPredictions] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (seaPointNumber) {
      const storedPredictions = getStoredPredictions(seaPointNumber);
      if (storedPredictions) {
        setPredictions(storedPredictions);
        setIsLoadingPredictions(false);
      } else {
        setIsLoadingPredictions(true);
        fetch(`https://${process.env.REACT_APP_SERVE_URL}/wave/${seaPointNumber}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then((res) => res.json())
          .then((data) => {
            storePredictions(seaPointNumber, data.predictions);
            setPredictions(data.predictions);
            setIsLoadingPredictions(false);
          })
          .catch((err) => {
            console.error('Error fetching predictions', err);
            setError(err.message);
            setIsLoadingPredictions(false);
          });
      }
    }
  }, [seaPointNumber]);

  function generateTimesArray(interval) {
    const result = [];
    const now = new Date();
    // Round up to the next full hour
    const start = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours() + 1, 0, 0);
    const end = new Date(start);
    end.setHours(start.getHours() + 7);

    for (let d = start; d <= end; d.setMinutes(d.getMinutes() + interval)) {
      result.push(format(d));
    }

    return result;
  }

  function format(inputDate) {
    let hours = inputDate.getHours();
    let minutes = inputDate.getMinutes();
    const formattedHours = hours === 0 ? 12 : hours < 10 ? '0' + hours : hours;
    const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;
    return formattedHours + ':' + formattedMinutes;
  }

  const times = generateTimesArray(60);

  function storePredictions(seaPointNumber, predictions) {
    const now = new Date();
    const stationData = {
      number: seaPointNumber,
      predictions: predictions,
      timestamp: now.getTime(),
    };

    const jsonString = JSON.stringify(stationData);

    localStorage.setItem(`location-${seaPointNumber}`, jsonString);
  }

  function getStoredPredictions(seaPointNumber) {
    const storedData = localStorage.getItem(`location-${seaPointNumber}`);
    if (storedData) {
      const stationData = JSON.parse(storedData);
      const now = new Date().getTime();
      // Check if the stored data is less than 1 hour old
      if (now - stationData.timestamp < 60 * 60 * 1000) {
        return stationData.predictions;
      }
    }
    return null;
  }

  return (
    <div>
      {isLoadingPredictions ? (
        <div>Loading predictions...</div>
      ) : (
        <div className='mt-4'>
          <h3 className='text-xl font-bold mb-2'>Predictions:</h3>
          {error ? (
            <div className='mt-4'>
              <p className='text-red-500'>Error: {error}</p>
            </div>
          ) : (
            <ul>
              {predictions.map((prediction, index) => (
                <li key={index} className='text-gray-600'>
                  {times[index]}: {prediction}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default Predictions;
