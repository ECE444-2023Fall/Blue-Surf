import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/LoginPage.css";
const surfEmojiImage = require("../assets/surf-emoji.png");
const waveImage = require("../assets/wave.png");

interface LoginPageProps {
  setToken: (token: string | null) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ setToken }) => {
  const [loginForm, setloginForm] = useState({
    userIdentifier: "",
    password: "",
  });
  const navigate = useNavigate();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value, name } = event.target;
    setloginForm((prevForm) => ({
      ...prevForm,
      [name]: value,
    }));
  };

  const logMeIn = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const response = await fetch("/api/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_identifier: loginForm.userIdentifier,
          password: loginForm.password,
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error("Incorrect password.");
        } else if (response.status === 404) {
          throw new Error("User not found.");
        } else {
          throw new Error("Network response was not ok.");
        }
      }

      const data = await response.json();
      setToken(data.access_token);
      navigate("/");
    } catch (error: any) {
      console.error("Login Error:", error);
    }

    setloginForm({
      userIdentifier: "",
      password: "",
    });
  };

  return (
    <div className="login-page-wrapper">
      <div className="row">
        <div className="col-md-4">
          <div className="image-container">
            <img src={surfEmojiImage} alt="..." className="surf-image" />
            <img src={waveImage} alt="..." className="wave-image" />
          </div>
        </div>
        <div className="col-md-8">
          <div className="login-container">
            <h1>Sign in to BlueSurf</h1>
            <p className="login-subtext">
              Get back to discovering UofT activities and events.
            </p>
            <form method="post" action="/">
              <div className="form-group userinput">
                <input
                  type="text"
                  id="username"
                  name="userIdentifier"
                  className="form-control input-boxes"
                  placeholder="Username/Email"
                  value={loginForm.userIdentifier}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <input
                  type="password"
                  id="password"
                  name="password"
                  className="form-control input-boxes"
                  placeholder="Password"
                  value={loginForm.password}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group forgot-password-container">
                <a href="/register" className="forgot-password">
                  Forgot password?
                </a>
              </div>
              <div className="form-group">
                <button type="submit" className="login-btn" onClick={logMeIn}>
                  Login
                </button>
              </div>
            </form>
            <p className="login-subtext bottom-subtext">
              {" "}
              New to BlueSurf? <a href="/register">Join Now</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
