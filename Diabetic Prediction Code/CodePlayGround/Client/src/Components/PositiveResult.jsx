import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';


const PositiveResult = () => {
  console.log("Positive")
  return (
    <div className="d-flex flex-column justify-content-center align-items-center min-vh-100 bg-gradient">
      <h1 className="display-4 mb-3">Result</h1>
      <p className="h5 mb-4 text-success">You are diabetc go for a doctor</p>
      <img
        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu95FmbJ7kf7Kgy9XYYQ4314hDzJVh7trgaA&s"
        alt="Relax"
        className="img-fluid rounded shadow mb-5"
      />
      <footer className="bg-dark text-white w-100 text-center py-2 mt-auto">
        
      </footer>
    </div>
  );
};

export default PositiveResult;
