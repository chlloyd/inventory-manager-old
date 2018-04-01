import React from 'react';
import {BrowserRouter as Router, Route, Link, Switch} from 'react-router-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { INDEX_ROUTE, BLANK_ROUTE } from './routes';
import IndexPage from './pages/login';
import EmptyPage from "./pages/empty";
import {createBrowserHistory} from "history";

const history = createBrowserHistory();

const App = () => (
    <MuiThemeProvider>
        <Router history={history}>
            <Switch>
                <Route
                    path={INDEX_ROUTE}
                    component={IndexPage} />
                <Route
                    path={BLANK_ROUTE}
                    component={EmptyPage} />
            </Switch>
        </Router>

        <EmptyPage />
    </MuiThemeProvider>
);

export default App;