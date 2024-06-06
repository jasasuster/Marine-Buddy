import React from 'react';
import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <nav className='flex items-center justify-between flex-wrap bg-blue-800 bg-opacity-90 p-6'>
      <div className='flex items-center flex-shrink-0 text-white mr-6'>
        <img src='/octopus.png' alt='octopus' className='h-7 w-7 mr-1' />
        <span className='font-semibold text-xl tracking-tight'>Marine Buddy</span>
      </div>
      <div className='w-full block flex-grow lg:flex lg:items-center lg:w-auto px-5'>
        <div className='text-sm lg:flex-grow'></div>
        <div>
          <div className='text-sm lg:flex-grow'>
            <Link
              to='/'
              className='block mt-4 lg:inline-block lg:mt-0 text-white hover:underline hover:font-medium mr-4'
            >
              List
            </Link>
            {/* <Link
              to='/map'
              className='block mt-4 lg:inline-block lg:mt-0 text-white hover:underline hover:font-medium mr-4'
            >
              Map
            </Link> */}
            <Link
              to='/animals'
              className='block mt-4 lg:inline-block lg:mt-0 text-white hover:underline hover:font-medium mr-4'
            >
              Predict Animals
            </Link>
            <Link
              to='/admin'
              className='block mt-4 lg:inline-block lg:mt-0 text-white hover:underline hover:font-medium mr-4'
            >
              Admin Panel
            </Link>
            <ul className='pl-4 list-disc'>
              <li>
                <Link
                  to='/admin/data-quality'
                  className='block mt-4 lg:inline-block lg:mt-0 text-white hover:underline hover:font-medium mr-4'
                >
                  Data Quality
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  );
}
