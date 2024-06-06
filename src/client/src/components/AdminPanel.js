import React from 'react';
import { Link } from 'react-router-dom';

function AdminPanel() {
  return (
    <div className='flex h-full'>
      <nav className='w-1/5 bg-gray-800 text-white p-5'>
        <ul className='space-y-4'>
          <li>
            <Link to='data-quality' className='block p-2 hover:bg-gray-700 rounded'>
              Data Quality
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}

export default AdminPanel;
