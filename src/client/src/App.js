import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import SeaPointInfo from './components/SeaPointInfo';
import Map from './components/Map';
import Animals from './components/Animals';
import Header from './components/Header';
import AdminPanel from './components/AdminPanel';
import DataQuality from './components/DataQuality';
import Evaluation from './components/Evaluation';
import ProductionEvaluation from './components/ProductionEvaluation';

const routes = [
  { path: '/', element: <Home />, private: true },
  { path: '/location/:seaPointId', element: <SeaPointInfo /> },
  { path: '/map', element: <Map /> },
  { path: '/animals', element: <Animals /> },
  { path: '/admin', element: <AdminPanel />, private: true },
  { path: '/admin/data-quality', element: <DataQuality />, private: true },
  { path: '/admin/evaluation', element: <Evaluation />, private: true },
  { path: '/admin/production-evaluation', element: <ProductionEvaluation />, private: true },
];

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        {routes.map((route, index) => (
          <Route key={index} path={route.path} element={route.element} />
        ))}
      </Routes>
    </Router>
  );
}

export default App;
