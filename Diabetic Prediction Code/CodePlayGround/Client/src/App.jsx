import { useState } from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Signup from './Components/Signup';
import Login from './Components/Login';
import Home from './Components/Home';
import PositiveResult from './Components/PositiveResult';
import NegativeResult from './Components/NegativeResultv';
function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/signup" element={<Signup/>} />
        <Route path="/diabetic" element={<PositiveResult/>} />
        <Route path="/nondiabetic" element={<NegativeResult/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
