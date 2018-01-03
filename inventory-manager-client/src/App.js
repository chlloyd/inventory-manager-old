import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import LoginPage from "./pages/login";

const App = () => (
  <MuiThemeProvider>
    <LoginPage />
  </MuiThemeProvider>
);

export default App;