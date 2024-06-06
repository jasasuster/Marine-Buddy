import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import Predictions from './Predictions';

function Map() {
  const [locations, setLocations] = useState([]);
  const [seePredictions, setSeePredictions] = useState(false);

  useEffect(() => {
    fetch('data/locations.json')
      .then((res) => res.json())
      .then((data) => {
        setLocations(data);
      })
      .catch((err) => {
        console.error('Error fetching sea points', err);
      });
  }, []);

  return (
    <div className='w-2/3 mx-auto'>
      <h1>Map</h1>
      <MapContainer center={[45.1805, 13.4665]} zoom={14}>
        {/* className='w-full h-2/3' */}
        <TileLayer url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' />
        {locations.map((location) => {
          return (
            <Marker
              key={location.number}
              position={[location.coordinates.latitude, location.coordinates.longitude]}
            >
              <Popup>
                <p className='text-center'>{location.name}</p>
                <button
                  className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
                  onClick={() => setSeePredictions(!seePredictions)}
                >
                  {seePredictions ? 'Hide Predictions' : 'View Predictions'}
                </button>
                {seePredictions && <Predictions seaPointNumber={location.number} />}
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}

export default Map;
