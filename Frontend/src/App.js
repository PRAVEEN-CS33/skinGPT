import React from 'react';
// import './App.css';

import { BrowserRouter as Router,Route, Routes } from 'react-router-dom';
import PNavbar from './components/PNavbar';
import BHome from './components/bothome';




function App() {
  return (
    <div>
      <Router>
      <PNavbar/>
        <Routes>
          <Route path="/" element={<BHome />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;