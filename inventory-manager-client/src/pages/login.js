import React, {Component} from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField'

const styles = {
    container: {
        textAlign: 'center',
        paddingTop: 200,
    },
};

class Login extends Component {
    render() {
        return (
            <div style={styles.container}>
                <h1>Login Page</h1>
                <TextField
                    hintText="Email"
                    floatingLabelText="Email"
                /><br />
                <TextField
                    hintText="Password"
                    floatingLabelText="Password"
                    type="password"
                /><br />
                <RaisedButton
                    label="Login"
                    secondary={true}
                    // onClick={this.handleTouchTap}
                />
            </div>
        );
    }
}

export default Login;