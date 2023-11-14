import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import FNavbar from "./components/FNavbar";
import LandingPage from "./components/LandingPage";
import useAuth from "./components/useAuth";
import LoginPage from "./components/LoginPage";
import SignupPage from "./components/SignupPage";
import PostDetailsPage from "./components/PostDetailsPage";
import PostCreatePage from "./components/PostCreatePage";
import { HashRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import PersonalDashboard from "./components/PersonalDashboard"
import 'react-datepicker/dist/react-datepicker.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const { token, user, removeAuth, setAuth } = useAuth();
  
  const authenticatedRoutes = (
    <Routes>
      <Route path="/" element={<LandingPage token={token} user={user} setAuth={setAuth} />} />
      <Route path="/post/:postId" element={<PostDetailsPage token={token} user={user} setAuth={setAuth} />} />
      <Route path="/dashboard" element={<PersonalDashboard token={token} user={user} setAuth={setAuth}/>} />
      <Route path="/create" element={<PostCreatePage token={token} user={user} setAuth={setAuth} />} />
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
      <ToastContainer autoClose={2500}/>
      {token && token !== "" && token !== undefined ? authenticatedRoutes : nonAuthenticatedRoutes}
    </Router>
  );
}

export default App;