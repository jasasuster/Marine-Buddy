import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import SeaPointInfoCard from './SeaPointInfoCard';

function Home() {
  const [locations, setLocations] = useState([]);
  const [filter, setFilter] = useState('');

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

  const filteredLocations = locations.filter((station) => station.name.toLowerCase().includes(filter.toLowerCase()));

  const noMatchedLocationsInFilter = filter !== '' && filteredLocations.length === 0;

  return (
    <div className='flex items-center justify-center'>
      <div className='bg-white p-8 rounded shadow-md w-[50vh]'>
        <h2 className='text-2xl font-bold mb-4'>Locations</h2>
        <input
          type='text'
          placeholder='Filter...'
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className='border p-2 mb-4 rounded w-full'
        ></input>
        {noMatchedLocationsInFilter && <div className='text-red-500 mb-4 font-semibold text-center'>No gyms match your filter.</div>}
        <div className='h-[75vh] overflow-auto'>
          {filteredLocations.map((location) => {
            return (
              <Link to={`/location/${location.number}`} key={location.number}>
                <SeaPointInfoCard id={location.number} name={location.name} />
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default Home;
