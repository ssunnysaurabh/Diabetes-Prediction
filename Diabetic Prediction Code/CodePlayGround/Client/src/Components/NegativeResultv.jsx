import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const NegativeResult = () => {
    console.log("nagative")
  return (
    <div className="d-flex flex-column justify-content-center align-items-center min-vh-100 bg-gradient" style={{ background: 'linear-gradient(to right, #a0eac9, #90cdf4)' }}>
      <h1 className="display-4 mb-3">Result</h1>
      <p className="h5 mb-4 text-danger">U don't have diabetic </p>
      <img
        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIl0zbAw2_X3_fGaNzpMULpWkLyig_GeLthw&s" 
         
        alt="Doctor"
        className="img-fluid rounded shadow mb-5"
      />
      <footer className="bg-dark text-white w-100 text-center py-2 mt-auto">
       
      </footer>
    </div>
  );
};

export default NegativeResult;
