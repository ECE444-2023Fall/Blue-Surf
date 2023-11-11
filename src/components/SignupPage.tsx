import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import "../styles/SignupPage.css";
import API_URL from '../config';
const surfEmojiImage = require("../assets/surf-emoji.png");
const waveImage = require("../assets/wave.png");

const SignupPage: React.FC = () => {
  const [registerForm, setRegisterForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [errorMessages, setErrorMessages] = useState({
    username: "",
    email: "",
    password: "",
    confirmpassword:"",
    loginError: "",
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
    setErrorMessages({ username: "", email: "" , password: "", confirmpassword: "", loginError: "" });
    const validateErrors = validate();
    if(validateErrors.username || validateErrors.password || validateErrors.confirmpassword || validateErrors.email){
      setErrorMessages({ username: validateErrors.username, email: validateErrors.email , password: validateErrors.password, confirmpassword: validateErrors.confirmpassword, loginError: "" });
    }

    // TODO: Should add a proper way to notify the user that their passwords do not match
    if (registerForm.password !== registerForm.confirmPassword) {
      console.error("Passwords do not match");
      return;
    }

    if (!registerForm.password) {
      return;
    }

    if (!registerForm.username) {
      return;
    }

    if (!registerForm.email) {
      return;
    }

    if (!registerForm.confirmPassword) {
      return;
    }

    if(!/^\S+@\S+\.\S+$/.test(registerForm.email)){
      return; 
    }

    if(!registerForm.email.includes("utoronto.ca")){
      return; 
    }

    if(registerForm.password.length < 8){
      return;
    }
    


    try {
      const response = await fetch(`${API_URL}/api/register`, {
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
          setErrorMessages({username:"", password:"", email:"", confirmpassword:"", loginError:"Email or Username already exists"})
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

  const validate = () => {
    const error = {
      username: "",
      email: "",
      password: "",
      confirmpassword:"",
      loginError: "",
    };

    if (!registerForm.username) {
      error.username = "Username is required";
    } else {
      error.username = "";
    }

    if (!registerForm.email) {
      error.email = "Email is required";
    } 
    else if(!/^\S+@\S+\.\S+$/.test(registerForm.email)){
      error.email="Invalid email format"
    }
    else if(!registerForm.email.includes("utoronto.ca")){
      error.email="Please enter University of Toronto email"
    }
    else {
      error.email = "";
    }

    if (!registerForm.password) {
      error.password = "Password is required";
    } 
    else if(registerForm.password.length < 8){
      error.password = "Password must be at least 8 characters"
    }
    else {
      error.password = "";
    }

    if (!registerForm.confirmPassword){
      error.confirmpassword = "Please re-enter password"
    }
    else if(registerForm.confirmPassword !== registerForm.password){
      error.confirmpassword = "Passwords don't match"
    }
    else{
      error.confirmpassword=""
    }

    return error;
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
            {errorMessages.loginError && (
                  <div className="error">{errorMessages.loginError}</div>
                )}
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
                {errorMessages.username && (
                  <div className="error">{errorMessages.username}</div>
                )}
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
                {errorMessages.email && (
                  <div className="error">{errorMessages.email}</div>
                )}
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
                {errorMessages.password && (
                  <div className="error">{errorMessages.password}</div>
                )}
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
                {errorMessages.confirmpassword && (
                  <div className="error error-confirmpassword">{errorMessages.confirmpassword}</div>
                )}
              </div>
              <div className="form-group">
                <button type="submit" className="signup-btn" onClick={signMeUp}>
                  Create Account
                </button>
              </div>
            </form>
            <p className="signup-subtext bottom-subtext">
              Already have an account? <Link to ="/login">Login</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
