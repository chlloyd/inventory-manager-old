import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import LoginPage from "./pages/login";
import BlankPage from "./pages/empty";

const App = () => (
  <MuiThemeProvider>
    {/*<LoginPage />*/}
    <BlankPage />
  </MuiThemeProvider>
);

export default App;