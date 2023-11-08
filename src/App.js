import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import FNavbar from "./components/FNavbar";
import LandingPage from "./components/LandingPage";
import PostDetailsPage from "./components/PostDetailsPage";
import PostCreatePage from "./components/PostCreatePage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <FNavbar />
      <div className="content-container">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/post/:postId" element={<PostDetailsPage />} />
          <Route path="/create" element={<PostCreatePage />} />
          {/* Define other routes here*/}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
