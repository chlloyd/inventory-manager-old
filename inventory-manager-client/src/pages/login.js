import React, {Component} from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField'
import AppBar from 'material-ui/AppBar'
import axios from 'axios'

const styles = {
    container: {
        textAlign: 'center',
        paddingTop: 200,
    },
    heading: {
        fontFamily: 'Roboto'
    }
};

class Login extends Component {
    constructor(props){
        super(props);
        this.state={
            username:'',
            password:''
        }
    }

    handleLoginButton(event){
        var apiBaseUrl = "http://localhost:5000/api/";
        var payload= {
            "email": this.state.email,
            "password": this.state.password
        }

        axios.post(apiBaseUrl+'login', payload).then(
            response => {
                console.log(response);
                if (response.data.code.startsWith("2")) {
                    console.log("Login Successful")
                }
                else{
                        console.log("Error 401: Username & password do not match");
                    }
            })
        .catch(error => console.log(error));
    }
    render() {
        return (
            <div>
                <AppBar title="Login Page"/>
                    <TextField
                    hintText="Email"
                    floatingLabelText="Email"
                    onChange = {(event,newValue) => this.setState({email:newValue})}
                /><br/>
                <TextField
                    hintText="Password"
                    floatingLabelText="Password"
                    type="password"
                    onChange = {(event,newValue) => this.setState({password:newValue})}
                /><br/>
                <RaisedButton
                    label="Login"
                    secondary={true}
                    onClick={(event) => this.handleLoginButton(event)}
                />
            </div>
        );
    }
}

export default Login;
