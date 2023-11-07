import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import FNavbar from "./components/FNavbar";
import LandingPage from "./components/LandingPage";
import PostDetailsPage from "./components/PostDetailsPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PersonalDashboard from "./components/PersonalDashboard"


function App() {
  return (
    <Router>
      <FNavbar />
      <div className="content-container">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/post/:postId" element={<PostDetailsPage />} />
          <Route path="/dashboard" element={<PersonalDashboard />} />
          {/* Define other routes here*/}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
