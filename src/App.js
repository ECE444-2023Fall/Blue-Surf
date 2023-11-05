import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import FNavbar from "./components/FNavbar";
import LandingPage from "./components/LandingPage";
import useToken from "./components/useToken";
import LoginPage from "./components/LoginPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  const { token, removeToken, setToken } = useToken();

  return (
    <Router>
      <FNavbar />
      <div className="content-container">
      <Header token={removeToken}/>
        {!token && token!=="" &&token!== undefined?  
        <LoginPage setToken={setToken} />
        :(          
        <>
          <Routes>
            <Route exact path="/profile" element={<Profile token={token} setToken={setToken}/>}></Route>
          </Routes>
        </>
      )}
        <Routes>
          <Route path="/" element={<LandingPage />} />
          {/* Define other routes here*/}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
