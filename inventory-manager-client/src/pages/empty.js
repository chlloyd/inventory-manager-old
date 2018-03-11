import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';

class Empty extends Component {
    render() {
        return (
            <AppBar
                title="Inventory Manager"
                iconClassNameRight="muidocs-icon-navigation-expand-more"
            />
        );
    }
}


export default Empty;


// <IconMenu
//     {...props}
//     iconButtonElement={
//       <IconButton><MoreVertIcon /></IconButton>
//     }
//     targetOrigin={{horizontal: 'right', vertical: 'top'}}
//     anchorOrigin={{horizontal: 'right', vertical: 'top'}}
//   >
//     <MenuItem primaryText="Refresh" />
//     <MenuItem primaryText="Help" />
//     <MenuItem primaryText="Sign out" />
//   </IconMenu>