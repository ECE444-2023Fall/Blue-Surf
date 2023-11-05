import React, { useState } from 'react';
import '../styles/LoginPage.css'; // Import the corresponding CSS file
const surfEmojiImage = require("../assets/surf-emoji.png");
const waveImage = require("../assets/wave.png");
import axios from 'axios';

const LoginPage: React.FC = () => {
    const [loginForm, setloginForm] = useState({
        username: "",
        password: ""
      });
    
      const [token, setToken] = useState<string | null>(null);
    
      const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { value, name } = event.target;
        setloginForm((prevForm) => ({
          ...prevForm,
          [name]: value,
        }));
      };
    
      const logMeIn = (event: React.FormEvent) => {
        event.preventDefault();
    
        axios({
          method: "POST",
          url: "/token",
          data: {
            username: loginForm.username,
            password: loginForm.password,
          },
        })
          .then((response) => {
            setToken(response.data.access_token);
          })
          .catch((error) => {
            if (error.response) {
              console.log(error.response);
              console.log(error.response.status);
              console.log(error.response.headers);
            }
          });
    
        setloginForm({
          username: "",
          password: "",
        });
      };

    
  return (
    <div className="row">
        <div className="col-md-4">
            <div className="image-container">
                <img src={surfEmojiImage} alt="..." className="surf-image"/>
                <img src={waveImage} alt="..." className="wave-image" />
            </div>
        </div>
        <div className="col-md-8">
            <div className="login-container">
                <h1>Sign in to BlueSurf</h1>
                <p className="login-subtext">Get back to discovering UofT activities and events.</p>
                <form method="post" action="/" >
                    <div className="form-group userinput">
                        <input type="text" 
                        id="username" 
                        name="username" 
                        className="form-control input-boxes" 
                        placeholder="Username" 
                        value = {loginForm.username}
                        onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <input type="password" 
                        id="password" 
                        name="password" 
                        className="form-control input-boxes" 
                        placeholder="Password"
                        value={loginForm.password}
                        onChange={handleChange}/>
                    </div>
                    <div className="form-group forgot-password-container">
                        <a href="/forgot-password" className="forgot-password">Forgot password?</a>
                    </div>
                    <div className="form-group">
                        <button type="submit" className="login-btn" onClick={logMeIn}>
                            Login
                        </button>
                    </div>
                </form>
                {token ? (
                    <p className="login-subtext bottom-subtext">
                    Logged in as: {token}
                    </p>
                ) : (
                    <p className="login-subtext bottom-subtext">
                    New to BlueSurf? <a href="/register">Join Now</a>
                    </p>
          )}
            </div>
        </div>
    </div>
  );
};

export default LoginPage;
