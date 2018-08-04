import React from "react";
import {Grid, InputLabel} from "material-ui";

import {Button, CustomInput, ItemGrid, ProfileCard, RegularCard, LoginCard} from "../../components";

import Visibility from 'material-ui-icons/VisibilityOff';
import VisibilityOff from 'material-ui-icons/VisibilityOff';

function UserProfile({...props}) {
    return (
            <Grid container justify="center">
                <ItemGrid xs={12} sm={12} md={3}>{/* md should = 3 */}
                    <LoginCard
                        cardTitle="Login Page"
                        content={
                            <div>
                                    <ItemGrid xs={12} sm={12} md={12}>
                                        <CustomInput
                                            labelText="Username"
                                            id="username"
                                            formControlProps={{
                                                fullWidth: true
                                            }}
                                        />
                                        <CustomInput
                                            labelText="Password"
                                            id="password"
                                            formControlProps={{
                                                fullWidth: true
                                            }}
                                            // type={this.state.showPassword ? 'text' : 'password'}
                                            // value={this.state.password}
                                            // onChange={this.handleChange('password')}
                                            // endAdornment={
                                            // <InputAdornment position="end">
                                            //     <IconButton
                                            //         aria-label="Toggle password visibility"
                                            //         onClick={this.handleClickShowPassword}
                                            //         onMouseDown={this.handleMouseDownPassword}
                                            //     >
                                            //         {this.state.showPassword ? <VisibilityOff /> : <Visibility />}
                                            //     </IconButton>
                                            // </InputAdornment>
                                        />
                                    </ItemGrid>
                            </div>
                        }
                        footer={<Button color="primary">Login</Button>}
                    />
                </ItemGrid>
            </Grid>
    );
}

export default UserProfile;
