import React from 'react';
import { Link } from 'react-router-dom';

function AdminPanel() {
  return (
    <div className='flex h-full w-2/3 mx-auto pt-8 gap-2'>
      <div className='w-1/3 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mt-4 rounded content-center'>
        <Link to='/admin/data-quality'>Data Quality</Link>
      </div>
      <div className='w-1/3 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mt-4 rounded content-center'>
        <Link to='/admin/evaluation'>Evaluation</Link>
      </div>
      <div className='w-1/3 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mt-4 rounded content-center'>
        <Link to='/admin/production-evaluation'>Production Evaluation</Link>
      </div>
    </div>
  );
}

export default AdminPanel;
