import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from 'axios'
import { Alert } from "bootstrap";
function Signup() {
    const [name,setName]=useState()
    const [email,setEmail]=useState()
    const [password,setPassword]=useState()
  const navigate = useNavigate();
  const handleSubmit = (e) => {
  e.preventDefault();
  axios.post('http://localhost:3001/register', { name, email, password })
    .then((result) => {
        if(result.data==="Success"){
                  console.log("Registration success:", result.data);
                    navigate("/login"); // Only navigate on success
        }else{
             navigate("/login"); 
        }

    })
    .catch((err) => {
      console.error("Registration error:", err);
      alert("Registration failed. Please try again."); // Optional error UI
    });
};
  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div
        className="card p-4 shadow-lg"
        style={{ maxWidth: "400px", width: "100%" }}
      >
        <h2 className="text-center mb-4 text-primary">Create Account</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="name" className="form-label">
              Full Name
            </label>
            <input
              type="text"
              className="form-control"
              id="name"
              placeholder="Enter your full name"
              onChange={(e)=>setName(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Email address
            </label>
            <input
              type="email"
              className="form-control"
              id="email"
              placeholder="Enter your email"
              onChange={(e)=>setEmail(e.target.value)}

            />
            <div id="emailHelp" className="form-text">
              We'll never share your email with anyone else.
            </div>
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              className="form-control"
              id="password"
              placeholder="Create a password"
              onChange={(e)=>setPassword(e.target.value)}
            />
          </div>

          <p className="mt-3 text-center">
            Already have an account? <Link to="/login">Login</Link>
          </p>
        <button type="submit" className="btn btn-primary w-100">
          Sign Up
        </button>
        </form>

        <Link to='/login'type="submit" className="btn btn-secondary w-100 mt-3">
          Login
        </Link>
      </div>
    </div>
  );
}

export default Signup;
