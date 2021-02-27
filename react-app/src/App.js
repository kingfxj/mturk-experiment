import "./App.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { HomePage } from "./HomePage";
import { LobbyPage } from "./LobbyPage";
import { LoginPage } from "./LoginPage";
import { NotFoundPage } from "./NotFoundPage.js";
import { NavBar } from "./NavBar";

// displays everything - navbar, pages with corresponding path routes
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
