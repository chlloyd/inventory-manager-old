import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';
import IconMenu from 'material-ui/IconMenu'

const styles = {
    title: {
        cursor: 'pointer'
    },
};

function titleclick() {
//    Go to home page
}

class leftappbarbutton {
    render() {

        inner = (
            <IconButton>
                <MoreVertIcon />
            </IconButton>);


        return (
            <IconMenu
                iconButtonElement={inner}
                targetOrigin={{horizontal: 'right', vertical: 'top'}}
                anchorOrigin={{horizontal: 'right', vertical: 'top'}}>
                <MenuItem primaryText="Refresh" />
                <MenuItem primaryText="Help" />
                <MenuItem primaryText="Sign out" />
            </IconMenu>
                )

                {/*render() {*/}
                {/*return (*/}
                {/*<AppBar title={<span style={styles.title}>Inventory Manager</span>}*/}
                {/*onTitleClick={titleclick}*/}
                {/*onLeftIconButtonClick={leftappbarbutton}/>*/}
                {/*);*/}
                }
                }

                {/*export default Empty;*/}


                {/*    <IconMenu*/}
                {/*     {...props}*/}
                {/*     iconButtonElement={*/}
                {/*       <IconButton><MoreVertIcon /></IconButton>*/}
                {/*     }*/}
                {/*     targetOrigin={{horizontal: 'right', vertical: 'top'}}*/}
                {/*     anchorOrigin={{horizontal: 'right', vertical: 'top'}}*/}
                {/*   >*/}
                {/*     <MenuItem primaryText="Refresh" />*/}
                {/*     <MenuItem primaryText="Help" />*/}
                {/*     <MenuItem primaryText="Sign out" />*/}
                {/*   </IconMenu>*/}