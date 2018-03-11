import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import EmptyPage from "./pages/empty";

const App = () => (
  <MuiThemeProvider>
    <EmptyPage />
  </MuiThemeProvider>
);

export default App;