import React from "react";
import "../styles/FNavbar.css";
import { Navbar, Nav } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import API_URL from '../config';

console.log(API_URL);

interface User {
  userId: string;
  username: string;
}

interface FNavbarProps {
  token: string | null;
  user: User | null;
  removeAuth: () => void;
}

const FNavbar: React.FC<FNavbarProps> = ({ token, user, removeAuth }) => {
  const logOut = async () => {
    try {
      const response = await fetch(`${API_URL}/api/logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();
      if (!response.ok) {
        if (response.status === 500) {
          throw new Error(data["error message"]);
        }
        throw new Error("Network response was not ok.");
      }

      if (data && data.msg === "logout successful") {
        removeAuth();
      } else {
        throw new Error("Unexpected response message after logout");
      }
    } catch (error) {
      console.error("Logout Error:", error);
    }
  };

  let renderNav: JSX.Element;

  if (token && token !== "" && token !== undefined) {
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
          <strong>{user?.username}</strong>{" "}
        </p>
      </Nav>
    );
  } else {
    renderNav = (
      <div className="right-align ml-auto">
        <LinkContainer to="/login">
          <Nav.Link className="navbar-link-text bold">Login / Sign Up</Nav.Link>
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
};

export default FNavbar;
