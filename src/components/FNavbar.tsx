import React from "react";
import "../styles/FNavbar.css";
import { Navbar, Nav } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { useNavigate } from "react-router-dom";
import axios from "axios";

interface FNavbarProps {
  token: string | null;
  removeToken: () => void;
}

const FNavbar: React.FC<FNavbarProps> = ({ token, removeToken }) => {
  const navigate = useNavigate();

  const logOut = () => {
    axios({
      method: "POST",
      url: "/api/logout",
    })
      .then((response) => {
        removeToken();
        navigate("/login");
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
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
        <LinkContainer to="/profile">
          <p className="navbar-link-text my-2">
            {" "}
            <strong>Test</strong>{" "}
          </p>
        </LinkContainer>
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
