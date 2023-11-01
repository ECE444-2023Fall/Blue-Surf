import React from 'react';
import '../styles/SignupPage.css'; // Import the corresponding CSS file
const surfEmojiImage = require("../assets/surf-emoji.png");
const waveImage = require("../assets/wave.png");

const SignupPage: React.FC = () => {
  return (
    <div className="row">
        <div className="col-md-4">
            <div className="image-container">
                <img src={surfEmojiImage} alt="..." className="surf-image"/>
                <img src={waveImage} alt="..." className="wave-image" />
            </div>
        </div>
        <div className="col-md-8">
            <div className="signup-container">
                <h1>Create a BlueSurf account!</h1>
                <p className="signup-subtext">Create an account to discover UofT activities and accounts.</p>
                <form method="post" action="/">
                    <div className="form-group userinput">
                        <input type="text" id="username" name="username" className="form-control input-boxes" placeholder="Username" />
                    </div>
                    <div className="form-group userinput">
                        <input type="password" id="password" name="password" className="form-control input-boxes" placeholder="Password"/>
                    </div>
                    <div className="form-group">
                        <input type="password" id="confirmPassword" name="confirmPassword" className="form-control input-boxes" placeholder="Confirm Password"/>
                    </div>
                    <div className="form-group">
                        <button type="submit" className="signup-btn">Create Account</button>
                    </div>
                </form>
                <p className="signup-subtext bottom-subtext">Already have an account? <a href="/login">Login</a></p>
            </div>
        </div>
    </div>
  );
};

export default SignupPage;
