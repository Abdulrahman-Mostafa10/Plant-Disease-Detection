import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './HomePage';
import TestTraditionalML from './TestTraditionalML';
import TestDNN from './TestDNN';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/test-traditional-ml" element={<TestTraditionalML />} />
        <Route path="/test-dnn" element={<TestDNN />} />
      </Routes>
    </Router>
  );
}

export default App;
