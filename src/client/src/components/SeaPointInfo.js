import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function SeaPointInfo() {
  const { seaPointId } = useParams();
  const parsedSeaPointId = parseInt(seaPointId);
  const [seaPoint, setSeaPoint] = useState(null);

  const [predictions, setPredictions] = useState([]);
  const [isLoadingPredictions, setIsLoadingPredictions] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('../data/locations.json')
      .then((res) => res.json())
      .then((data) => {
        const foundSeaPoint = data.find((s) => s.number === parsedSeaPointId);
        setSeaPoint(foundSeaPoint);
      })
      .catch((err) => {
        console.error('Error fetching sea point', err);
      });
  }, [parsedSeaPointId]);

  useEffect(() => {
    if (seaPoint) {
      const storedPredictions = getPredictions(seaPoint.number);
      if (storedPredictions) {
        setPredictions(storedPredictions);
        setIsLoadingPredictions(false);
      } else {
        setIsLoadingPredictions(true);
        fetch(`${process.env.REACT_APP_SERVE_URL}/wave/${seaPoint.number.toString()}`, {
          method: 'POST',
        })
          .then((res) => res.json())
          .then((data) => {
            storePredictions(seaPoint.number, data.predictions);
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
  }, [seaPoint]);

  function generateTimesArray(interval) {
    const result = [];
    const now = new Date();
    const start = new Date(
      now.getFullYear(),
      now.getMonth(),
      now.getDate(),
      now.getHours() + 1,
      0,
      0
    );
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

  function storePredictions(stationNumber, predictions) {
    const now = new Date();
    const stationData = {
      number: stationNumber,
      predictions: predictions,
      timestamp: now.getTime(),
    };

    const jsonString = JSON.stringify(stationData);
    localStorage.setItem(`location-${stationNumber}`, jsonString);
  }

  function getPredictions(stationNumber) {
    const storedData = localStorage.getItem(`location-${stationNumber}`);
    if (storedData) {
      const stationData = JSON.parse(storedData);
      const now = new Date().getTime();
      if (now - stationData.timestamp < 60 * 60 * 1000) {
        return stationData.predictions;
      }
    }
    return null;
  }

  if (!seaPoint) return <div>Loading...</div>;

  return (
    <div className='bg-white max-w-xl mx-auto p-4 rounded-lg shadow-md'>
      <h2 className='text-2xl font-bold mb-2'>{seaPoint.name}</h2>
      {isLoadingPredictions ? (
        <div>Loading predictions...</div>
      ) : (
        <div className='mt-4'>
          <h3 className='text-xl font-bold mb-2'>Wave Height Predictions:</h3>
          {error ? (
            <div className='mt-4'>
              <p className='text-red-500'>Error: {error}</p>
            </div>
          ) : (
            <ul>
              {predictions.map((prediction, index) => (
                <li key={index} className='text-gray-600'>
                  {times[index]}:{' '}
                  {prediction < 0
                    ? 0
                    : prediction > seaPoint.bike_stands
                    ? seaPoint.bike_stands
                    : prediction}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default SeaPointInfo;
