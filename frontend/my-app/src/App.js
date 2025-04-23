import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import MyAccount from "./pages/MyAccount";
import Login from "./pages/Login";
import Register from "./pages/Registration";
import UserAccount from "./pages/UserAccount"
import ForgotPassword from "./pages/ForgotPassword";


import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';


import "./styles/index.css"


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />}/>
        <Route path="/" element={<Home/>}/>
        <Route path="/register" element={<Register />}/>
        <Route path="/me" element={<MyAccount />}/>
        <Route path="/user-account/:user_id" element={<UserAccount />}/>
        <Route path="/forgot-password" element={<ForgotPassword />}/>
      </Routes>
    </Router>
  );
}


export default App;