import React from 'react';
import ReactDOM from 'react-dom';
import {createBrowserHistory} from 'history';
import {Router, Route, Switch} from 'react-router-dom';
import WebFontLoader from 'webfontloader';

import App from './App';
import registerServiceWorker from './registerServiceWorker';

const hist = createBrowserHistory();

WebFontLoader.load({
    google: {
        families: ['Roboto:300,400,500,700', 'Material Icons']
    }
});

ReactDOM.render(
    <Router history={hist}>
        <Switch>
            {[{path: '/', component: App}].map(
                (prop, key) =>
                    <Route path={prop.path} component={prop.component} key={key} />
            )}
        </Switch>
    </Router>

    // <App />
    , document.getElementById('root'));

registerServiceWorker();
