// import "./App.css";
import React from "react";
import { render } from "react-dom";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { HomePage } from "./HomePage";
// import { AboutPage } from "./AboutPage";
// import { LoginPage } from "./LoginPage";
// import { NotFoundPage } from "./NotFoundPage.js";
// import { NavBar } from "./NavBar";

// displays everything - navbar, pages with corresponding path routes
function App() {
  return (
    <div className="App">
      <Router>
        {/* <NavBar /> */}
        <div className="App-header">
          <Switch>
            <Route path="/" exact>
              <HomePage />
            </Route>
            {/* <Route path="/about" exact>
              <AboutPage />
            </Route>
            <Route path="/login" exact>
              <LoginPage />
            </Route>
            <Route>
              <NotFoundPage />
            </Route> */}
          </Switch>
        </div>
      </Router>
    </div>
  );
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
