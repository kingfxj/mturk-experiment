// import "./App.css";
import React from "react";
import { render } from "react-dom";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
// import { HomePage } from "./HomePage";
// import { LobbyPage } from "./LobbyPage";
// import { LoginPage } from "./LoginPage";
// import { NotFoundPage } from "./NotFoundPage";
// import { NavBar } from "./NavBar";
import { AssignmentsPage } from "./AssignmentsPage";
// import { QualsPage } from "./QualsPage";
// import { HITTypesPage } from "./HITTypesPage";

// displays everything - navbar + pages with corresponding path routes
function App() {
  return (
    <div className="App">
      <Router>
        {/* <NavBar /> */}
        <div className="App-header">
          <Switch>
            {/* <Route path="/" exact>
              <HomePage />
            </Route>
            <Route path="/hittypes" exact>
              <HITTypesPage />
            </Route>
            <Route path="/qualifications" exact>
              <QualsPage />
            </Route> */}
            <Route path="/" exact>
              <AssignmentsPage />
            </Route>
            {/* <Route path="/lobby" exact>
              <LobbyPage />
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
