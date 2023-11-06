import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/LoginPage.css';
import axios from 'axios';
const surfEmojiImage = require("../assets/surf-emoji.png");
const waveImage = require("../assets/wave.png");

interface LoginPageProps {
    setToken: (token: string | null) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({setToken}) => {
    const [loginForm, setloginForm] = useState({
        username: "",
        password: ""
      });
      const navigate = useNavigate();
    
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
            url: "/api/token",
            data: {
            username: loginForm.username,
            password: loginForm.password,
            },
        })

        .then((response) => {
            setToken(response.data.access_token);
            navigate('/');
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
                        <a href="/register" className="forgot-password">Forgot password?</a>
                    </div>
                    <div className="form-group">
                        <button type="submit" className="login-btn" onClick={logMeIn}>
                            Login
                        </button>
                    </div>
                </form>
                <p className="login-subtext bottom-subtext"> New to BlueSurf? <a href="/register">Join Now</a></p>
            </div>
        </div>
    </div>
  );
};

export default LoginPage;
