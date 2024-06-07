import React, { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Header() {
  const [isAdminDropdownOpen, setIsAdminDropdownOpen] = useState(false);

  const toggleAdminDropdown = () => {
    setIsAdminDropdownOpen(!isAdminDropdownOpen);
  };

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
              onClick={() => setIsAdminDropdownOpen(false)}
            >
              List
            </Link>
            <Link
              to='/animals'
              className='block mt-4 lg:inline-block lg:mt-0 text-white hover:underline hover:font-medium mr-4'
              onClick={() => setIsAdminDropdownOpen(false)}
            >
              Predict Animals
            </Link>
            <div className='relative inline-block text-left'>
              <button
                onClick={toggleAdminDropdown}
                className='block mt-4 lg:inline-block lg:mt-0 text-white hover:underline hover:font-medium mr-4'
              >
                Admin Panel
              </button>
              {isAdminDropdownOpen && (
                <ul className='absolute right-0 mt-2 w-48 bg-blue-700 rounded-md shadow-lg py-2 left-0'>
                  <li className='px-4 py-2'>
                    <Link
                      to='/admin/data-quality'
                      className='block text-sm text-white hover:underline'
                      onClick={() => setIsAdminDropdownOpen(false)}
                    >
                      Data Quality
                    </Link>
                  </li>
                  <li className='px-4 py-2'>
                    <Link
                      to='/admin/evaluation'
                      className='block text-sm text-white hover:underline'
                      onClick={() => setIsAdminDropdownOpen(false)}
                    >
                      Evaluation
                    </Link>
                  </li>
                  <li className='px-4 py-2'>
                    <Link
                      to='/admin/production-evaluation'
                      className='block text-sm text-white hover:underline'
                      onClick={() => setIsAdminDropdownOpen(false)}
                    >
                      Production Evaluation
                    </Link>
                  </li>
                </ul>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
