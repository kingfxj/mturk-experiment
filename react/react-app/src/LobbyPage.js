import React from "react";
import {
  Jumbotron,
  Button,
  DropdownButton,
  Dropdown,
  Table,
} from "react-bootstrap";

const lobbyName = "Lobby 1";
// Lobby page
export const LobbyPage = () => {
  return (
    <div>
      {/* Lobby info */}
      <Jumbotron style={{ color: "#282c34" }}>
        {/* Create lobby button */}
        <div style={{ fontSize: 15, display: "flex" }}>
          <Button variant="info" style={{ marginLeft: "auto" }}>
            Create Lobby
          </Button>
        </div>
        {/* Current lobby dropdown button */}
        <div style={{ display: "flex" }}>
          <h1 style={{ marginRight: "auto" }}>Lobby</h1>
          <DropdownButton
            style={{ marginLeft: "auto" }}
            id="dropdown-basic-button"
            title="Current Lobbies"
            variant="success"
          >
            <Dropdown.Item href="#/action-1">{lobbyName}</Dropdown.Item>
          </DropdownButton>
        </div>
        {/* Additional info text */}
        <p style={{ display: "flex" }}>
          Viewing lobby users in batch {lobbyName}
        </p>
        <div style={{ fontSize: 15, display: "flex" }}>
          <p>
            0 total users in current lobby
            <br></br>0 ready users in current lobby
          </p>
        </div>
        {/* Trigger lobby event button */}
        <div style={{ fontSize: 15, display: "flex" }}>
          <Button variant="warning">Trigger Lobby Event</Button>
        </div>
      </Jumbotron>
      {/* Lobby table  */}
      <Table striped bordered hover style={{ color: "black", fontSize: 15 }}>
        <thead>
          <tr style={{ fontSize: 20 }}>
            <th>#</th>
            <th>User</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>Jon</td>
            <td>Ong</td>
          </tr>
          <tr>
            <td>2</td>
            <td>Kalvin</td>
            <td>willgiveusgoodmarks</td>
          </tr>
          <tr>
            <td>3</td>
            <td>Ildar</td>
            <td>willalsogivegoodmarks</td>
          </tr>
        </tbody>
      </Table>
    </div>
  );
};
