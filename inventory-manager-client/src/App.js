import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import RaisedButton from 'material-ui/RaisedButton'

import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
        <MuiThemeProvider>
            <RaisedButton label="Login" />
        </MuiThemeProvider>
    );
  }
}

export default App;
