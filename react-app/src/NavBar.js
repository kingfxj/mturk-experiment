import React from "react";
import "./NavBar.css";
import { Navbar, Nav } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

export const NavBar = () => (
  <Navbar className="navbar-custom" variant="dark">
    <Navbar.Brand>MTurk</Navbar.Brand>
    <Nav className="mr-auto">
      {/* navbar paths to corresponding pages */}
      <Nav.Link href="/">Home</Nav.Link>
      <Nav.Link href="/hittypes">HITTypes</Nav.Link>
      <Nav.Link href="/hits">HITs</Nav.Link>
      <Nav.Link href="/assignments">Assignments</Nav.Link>
      <Nav.Link href="/lobby">Lobby</Nav.Link>
      <Nav.Link href="/login">Login</Nav.Link>
    </Nav>
  </Navbar>
);
