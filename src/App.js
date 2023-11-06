import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import FNavbar from "./components/FNavbar";
import LandingPage from "./components/LandingPage";
import useToken from "./components/useToken";
import LoginPage from './components/LoginPage'
import SignupPage from './components/SignupPage'
import Profile from './components/Profile'
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

function App() {
  return (
    <Router>
      <FNavbar token={token} removeToken={removeToken}/>
      <div className="content-container">
        <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage setToken={setToken} />} />
            <Route path="/register" element={<SignupPage />} />

            {token && token!=="" &&token!== undefined ? (
              <Route path="/profile" element={<Profile token={token} setToken={setToken} />} />
            ) : (
              <Route path="/profile" element={<Navigate to="/login" />} />
            )}

            {/* Define other routes here */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
      </div>
    </Router>
  );
}

export default App;
