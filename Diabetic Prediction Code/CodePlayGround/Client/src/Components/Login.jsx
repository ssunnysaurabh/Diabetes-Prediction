import React from "react";
import { Link } from "react-router-dom";
import { useState } from "react";
import axios from 'axios'
import { useNavigate } from "react-router-dom";
function Login() {
        const [email,setEmail]=useState()
        const [password,setPassword]=useState()
        const navigate = useNavigate();
        const handleSubmit=(e)=>{
            e.preventDefault();
            axios.post('http://localhost:3001/login',{email,password})
            .then(result=>{
                console.log(result);
                if(result.data==="Success"){
                    navigate('/home')
                }
            })
        }
  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card p-4 shadow-lg" style={{ maxWidth: "400px", width: "100%" }}>
        <h2 className="text-center mb-4 text-primary">Welcome Back</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="loginEmail" className="form-label">
              Email address
            </label>
            <input
              type="email"
              className="form-control"
              id="loginEmail"
              placeholder="Enter your email"
              onChange={(e)=>setEmail(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="loginPassword" className="form-label">
              Password
            </label>
            <input
              type="password"
              className="form-control"
              id="loginPassword"
              placeholder="Enter your password"
              onChange={(e)=>setPassword(e.target.value)}
            />
          </div>
  
          <button type="submit" className="btn btn-primary w-100">
            Login
          </button>
          <p className="mt-3 text-center">
            Don't have an account? <Link to="/Signup">Sign up</Link>
          </p>
        </form>
      </div>
    </div>
  );
}

export default Login;
