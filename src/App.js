import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import FNavbar from "./components/FNavbar";
import LandingPage from "./components/LandingPage";
import useAuth from "./components/useAuth";
import LoginPage from "./components/LoginPage";
import SignupPage from "./components/SignupPage";
import Profile from "./components/Profile";
import PostDetailsPage from "./components/PostDetailsPage";
import PostCreatePage from "./components/PostCreatePage";
// import {
//   BrowserRouter as Router,
//   Routes,
//   Route,
//   Navigate,
// } from "react-router-dom";
import { HashRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import PersonalDashboard from "./components/PersonalDashboard"
import 'react-datepicker/dist/react-datepicker.css';

function App() {
  const { token, user, removeAuth, setAuth } = useAuth();
  
  const authenticatedRoutes = (
    <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/post/:postId" element={<PostDetailsPage />} />
        <Route path="/profile" element={<Profile token={token} user={user} setAuth={setAuth} />} />
        <Route path="/dashboard" element={<PersonalDashboard token={token} user={user} setAuth={setAuth}/>} />
        <Route path="/create" element={<PostCreatePage />} />
        <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );

  const nonAuthenticatedRoutes = (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/post/:postId" element={<PostDetailsPage />} />
      <Route path="/login" element={<LoginPage setAuth={setAuth} />} />
      <Route path="/register" element={<SignupPage />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );

  return (
    <Router>
      <FNavbar token={token} user={user} removeAuth={removeAuth} />
      {token && token !== "" && token !== undefined ? authenticatedRoutes : nonAuthenticatedRoutes}
    </Router>
  );
}

export default App;