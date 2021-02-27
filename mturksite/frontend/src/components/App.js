import React, { Component } from "react";
import { render } from "react-dom";
/*import "./App.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { HomePage } from "./HomePage";
import { AboutPage } from "./AboutPage";
import { LoginPage } from "./LoginPage";
import { NotFoundPage } from "./NotFoundPage.js";
import { NavBar } from "./NavBar";*/

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading",
    };
  }

  componentDidMount() {
    fetch("test/")
      .then((response) => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then((data) => {
        this.setState(() => {
          return {
            data,
            loaded: true,
          };
        });
      });
  }

  render() {
    return (
      <ul>
        {this.state.data.map((assignments) => {
          return (
            <li key={assignments.id}>
              {assignments.name} - {assignments.surname}
            </li>
          );
        })}
      </ul>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
