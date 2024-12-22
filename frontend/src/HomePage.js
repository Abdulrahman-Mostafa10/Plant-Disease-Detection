import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  return (
    <div
      className="home-page"
      style={{
        backgroundImage: `url('/bg.jpg')`, // Directly reference the image in the public folder
      }}
    >
      <h1>Welcome to the Testing Page</h1>
      <div className="button-container">
        <Link to="/test-traditional-ml">
          <button className="nav-button">Test with Traditional ML</button>
        </Link>
        <Link to="/test-dnn">
          <button className="nav-button">Test with DNN</button>
        </Link>
      </div>
    </div>
  );
}

export default HomePage;
