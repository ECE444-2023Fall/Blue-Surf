import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/SignupPage.css";
const surfEmojiImage = require("../assets/surf-emoji.png");
const waveImage = require("../assets/wave.png");

const SignupPage: React.FC = () => {
  const [registerForm, setRegisterForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const navigate = useNavigate();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value, name } = event.target;
    setRegisterForm((prevForm) => ({
      ...prevForm,
      [name]: value,
    }));
  };

  const signMeUp = async (event: React.FormEvent) => {
    event.preventDefault();

    // TODO: Should add a proper way to notify the user that their passwords do not match
    if (registerForm.password !== registerForm.confirmPassword) {
      console.error("Passwords do not match");
      return;
    }

    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: registerForm.username,
          email: registerForm.email,
          password: registerForm.password,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        if (response.status === 400) {
          throw new Error(data["error message"]);
        } else if (response.status === 500) {
          throw new Error(data["error message"]);
        } else {
          throw new Error("Network response was not ok.");
        }
      }
      navigate("/login");
    } catch (error) {
      console.error("Signup Error:", error);
    }

    setRegisterForm({
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    });
  };
  return (
    <div className="signup-page-wrapper">
      <div className="row">
        <div className="col-md-4">
          <div className="image-container">
            <img src={surfEmojiImage} alt="..." className="surf-image-signup" />
            <img src={waveImage} alt="..." className="wave-image-signup" />
          </div>
        </div>
        <div className="col-md-8">
          <div className="signup-container">
            <h1>Create a BlueSurf account!</h1>
            <p className="signup-subtext">
              Create an account to discover UofT activities and events.
            </p>
            <form method="post" action="/">
              <div className="form-group userinput">
                <input
                  type="text"
                  id="username"
                  name="username"
                  className="form-control input-boxes"
                  placeholder="Username"
                  value={registerForm.username}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group userinput">
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="form-control input-boxes"
                  placeholder="Email"
                  value={registerForm.email}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group userinput">
                <input
                  type="password"
                  id="password"
                  name="password"
                  className="form-control input-boxes"
                  placeholder="Password"
                  value={registerForm.password}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  className="form-control input-boxes"
                  placeholder="Confirm Password"
                  value={registerForm.confirmPassword}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <button type="submit" className="signup-btn" onClick={signMeUp}>
                  Create Account
                </button>
              </div>
            </form>
            <p className="signup-subtext bottom-subtext">
              Already have an account? <a href="/login">Login</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
