import React from 'react';
import '../styles/LoginPage.css'; // Import the corresponding CSS file
const surfEmojiImage = require("../assets/surf-emoji.png");
const waveImage = require("../assets/wave.png");

const LoginPage: React.FC = () => {
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
                <form method="post" action="/">
                    <div className="form-group userinput">
                        <input type="text" id="username" name="username" className="form-control input-boxes" placeholder="Username" />
                    </div>
                    <div className="form-group">
                        <input type="password" id="password" name="password" className="form-control input-boxes" placeholder="Password"/>
                    </div>
                    <div className="form-group forgot-password-container">
                        <a href="/forgot-password" className="forgot-password">Forgot password?</a>
                    </div>
                    <div className="form-group">
                        <button type="submit" className="login-btn">Login</button>
                    </div>
                </form>
                <p className="login-subtext bottom-subtext">New to BlueSurf? <a href="/register">Join Now</a></p>
            </div>
        </div>
    </div>
  );
};

export default LoginPage;
