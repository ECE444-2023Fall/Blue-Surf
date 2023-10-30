import React from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/SignUp.css";


const SignUp: React.FC = () => {
  return (
    <div>
    {/* Head Content */}
    <head>
        <title>Post Creation</title>
        <link rel="stylesheet" type="text/css" href="../static/postcreation-styles.css" />
        <link href="https://fonts.googleapis.com/css?family=Karla:400,700" rel="stylesheet" />
        <script src="../animations/postcreation.js"></script>
      </head> 

      {/* Content */} 
      <div className="login-container">
        <h1>Create a Blue Surf account!</h1>
        <p className="login-subtext">Create an account to discover UofT activities and accounts.</p>
        <form method="post" action="/">
            <div className="form-group">
                <label htmlFor="username" className="sr-only">Username</label>
                <input type="text" id="username" name="username" className="form-control input-boxes" placeholder="Username"/>
            </div>
            <div className="form-group">
                <label htmlFor="password" className="sr-only">Password</label>
                <input type="password" id="password" name="password" className="form-control input-boxes" placeholder="Password"/>
            </div>
            <div className="form-group">
                <label htmlFor="password" className="sr-only">Password</label>
                <input type="password" id="password" name="password" className="form-control input-boxes" placeholder="Re-enter Password"/>
            </div>
            <div className="form-group">
                <button type="submit" className="btn btn-primary login-btn">Create Account</button>
            </div>
        </form>
        <p className="login-subtext">Already have an account? <a href="/login">Login</a></p>
    </div>   
    </div>
    );
};

export default SignUp;