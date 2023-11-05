import React, { useState } from "react";
import "../styles/FNavbar.css";
import { Navbar, Nav } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import axios from "axios";

interface User {
  displayName: string;
}

function FNavbar() {

  const [loginForm, setloginForm] = useState({
    username: "",
    password: ""
  });
  // Test user placeholder until Auth is set up
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

 /* const logIn = () => {
    // TODO: Implement sign-in logic, e.g., using an authentication service.
    setUser({
      displayName: "Test User",
    });
  };*/

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
  }

 const logOut = () => {
    // TODO: Implement sign-out logic.
    setUser(null);
  };

  {/*const logOut = () => {
    axios({
      method: "POST",
      url: "/logout",
    })
      .then((response) => {
        props.token();
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  };*/}

  let renderNav: JSX.Element;

  if (user) {
    renderNav = (
      <Nav className="right-align">
        <LinkContainer to="/dashboard">
          <Nav.Link className="navbar-link-text">Dashboard</Nav.Link>
        </LinkContainer>
        <LinkContainer to="/">
          <Nav.Link className="navbar-link-text" onClick={logOut}>
            Sign Out
          </Nav.Link>
        </LinkContainer>
        <p className="navbar-link-text my-2">
          {" "}
          <strong>{user.displayName}</strong>{" "}
        </p>
      </Nav>
    );
  } else {
    renderNav = (
      <div className="right-align ml-auto">
        <LinkContainer to="/login">
          <Nav.Link className="navbar-link-text bold" onClick={logMeIn}>
            Login / Sign Up
          </Nav.Link>
        </LinkContainer>
      </div>
    );
  }

  return (
    <Navbar
      collapseOnSelect
      expand="lg"
      bg="none"
      variant="light"
      fixed="top"
      className="mynavbar py-md-3 px-md-5 px-3 py-2"
    >
      <LinkContainer to="/" className="navbar-brand-container">
        <Navbar.Brand className="navbar-brand">
          BLUESURF <span style={{ fontSize: "1.5em" }}>🏄‍♂️</span>
        </Navbar.Brand>
      </LinkContainer>
      <Navbar.Toggle
        aria-controls="responsive-navbar-nav"
        className="mynavbar-toggle"
      />
      <Navbar.Collapse
        id="responsive-navbar-nav"
        className="collapsed-navbar-align"
      >
        {renderNav}
      </Navbar.Collapse>
    </Navbar>
  );
}

export default FNavbar;
