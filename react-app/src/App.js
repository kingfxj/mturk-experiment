import "./App.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { HomePage } from "./HomePage";
import { LobbyPage } from "./LobbyPage";
import { LoginPage } from "./LoginPage";
import { NotFoundPage } from "./NotFoundPage";
import { NavBar } from "./NavBar";
import { AssignmentsPage } from "./AssignmentsPage";
import { HITsPage } from "./HITsPage";
import { HITTypesPage } from "./HITTypesPage";

// displays everything - navbar + pages with corresponding path routes
function App() {
  return (
    <div className="App">
      <Router>
        <NavBar />
        <div className="App-header">
          <Switch>
            <Route path="/" exact>
              <HomePage />
            </Route>
            <Route path="/hittypes" exact>
              <HITTypesPage />
            </Route>
            <Route path="/hits" exact>
              <HITsPage />
            </Route>
            <Route path="/assignments" exact>
              <AssignmentsPage />
            </Route>
            <Route path="/lobby" exact>
              <LobbyPage />
            </Route>
            <Route path="/login" exact>
              <LoginPage />
            </Route>
            <Route>
              <NotFoundPage />
            </Route>
          </Switch>
        </div>
      </Router>
    </div>
  );
}

export default App;
