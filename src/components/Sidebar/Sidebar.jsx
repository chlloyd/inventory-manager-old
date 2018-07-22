import React from "react";
import PropTypes from "prop-types";
import { NavLink } from "react-router-dom";
import cx from "classnames";
import { Collapse, Drawer, Hidden, List, ListItem, ListItemIcon, ListItemText, withStyles } from "material-ui";
import {ExpandLess, ExpandMore } from 'material-ui-icons';

import {HeaderLinks} from "../../components";

import sidebarStyle from "../../variables/styles/sidebarStyle.jsx";

// verifies if routeName is the one active (in browser input)
function activeRoute(props, routeName) {
    console.log(props.location.pathname, routeName, props.location.pathname === routeName);
    // return props.location.pathname.indexOf(routeName) > -1 ? true : false;

    return props.location.pathname === routeName;
}

class Sidebar extends React.Component {
    state = {
    }

    handleClick = (e) => {
        console.log("Click! ", e);
        this.setState(
            { [e]: !this.state[e] }
        );
        console.log("State: ", this.state);
    };

    buildSubMenu() {
        const {classes, color, routes} = this.props;

        console.log("buildSubMenu", this.props);

        return (
            <List className={classes.list}>
                {routes.map((prop, key) => {
                    if (prop.redirect) return null;
                    const listItemClasses = cx({
                        [" " + classes[color]]: activeRoute(this.props, prop.path)
                    });
                    const whiteFontClasses = cx({
                        [" " + classes.whiteFont]: activeRoute(this.props, prop.path)
                    });

                    // debugger;

                    if (prop.children) {
                        const children = prop.children;

                        console.log("Children: " + children);

                        return (
                            <div>
                                <ListItem button onClick={this.handleClick} className={classes.itemLink + listItemClasses}>
                                    <ListItemIcon className={classes.itemIcon + whiteFontClasses}>
                                        { this.state[prop]
                                        ? <ExpandLess className={classes.itemIcon + whiteFontClasses} />
                                        : <ExpandMore className={classes.itemIcon + whiteFontClasses} /> }
                                    </ListItemIcon>
                                    <ListItemText inset primary={prop.sidebarName}
                                                  className={classes.itemText + whiteFontClasses}
                                                  disableTypography={true} />

                                </ListItem>
                                <Collapse in={this.state[prop]} timeout="auto" unmountOnExit>
                                    <List component="div" disablePadding>
                                        {children.map(
                                            (prop, key) => {
                                                const listItemClasses = cx({
                                                    [" " + classes[color]]: activeRoute(this.props, prop.path)
                                                });
                                                const whiteFontClasses = cx({
                                                    [" " + classes.whiteFont]: activeRoute(this.props, prop.path)
                                                });

                                                return (<NavLink
                                                    to={prop.path}
                                                    className={classes.item}
                                                    activeClassName="active"
                                                    key={key}
                                                >
                                                    <ListItem button className={classes.nestedItemLink + listItemClasses}>
                                                        <ListItemIcon className={classes.nestedItemIcon + whiteFontClasses}>
                                                            <prop.icon/>
                                                        </ListItemIcon>
                                                        <ListItemText
                                                            primary={prop.sidebarName}
                                                            className={classes.nestedItemText + whiteFontClasses}
                                                            disableTypography={true}
                                                        />
                                                    </ListItem>
                                                </NavLink>)
                                            }
                                        )}
                                    </List>
                                </Collapse>
                            </div>
                        )
                    }

                    return (
                        <NavLink
                            to={prop.path}
                            className={classes.item}
                            activeClassName="active"
                            key={key}
                        >
                            <ListItem button className={classes.itemLink + listItemClasses}>
                                <ListItemIcon className={classes.itemIcon + whiteFontClasses}>
                                    <prop.icon/>
                                </ListItemIcon>
                                <ListItemText
                                    primary={prop.sidebarName}
                                    className={classes.itemText + whiteFontClasses}
                                    disableTypography={true}
                                />
                            </ListItem>
                        </NavLink>
                    );
                })}
            </List>
        )
    }

    render() {
        const {classes, logo, logoText} = this.props;

        var links = this.buildSubMenu(this.props);

        var brand = (
            <div className={classes.logo}>
                <a href="/" className={classes.logoLink}>
                    {logo && <div className={classes.logoImage}>
                        <img src={logo} alt="logo" className={classes.img}/>
                    </div>}
                    {logoText}
                </a>
            </div>
        );
        return (
            <div>
                <Hidden mdUp>
                    <Drawer
                        variant="temporary"
                        anchor="right"
                        open={this.props.open}
                        classes={{
                            paper: classes.drawerPaper
                        }}
                        onClose={this.props.handleDrawerToggle}
                        ModalProps={{
                            keepMounted: true // Better open performance on mobile.
                        }}
                    >
                        {brand}
                        <div className={classes.sidebarWrapper}>
                            <HeaderLinks/>
                            {links}
                        </div>
                        <div className={classes.background}/>
                    </Drawer>
                </Hidden>
                <Hidden smDown>
                    <Drawer
                        anchor="left"
                        variant="permanent"
                        open
                        classes={{
                            paper: classes.drawerPaper
                        }}
                    >
                        {brand}
                        <div className={classes.sidebarWrapper}>{links}</div>
                        <div className={classes.background}/>
                    </Drawer>
                </Hidden>
            </div>
        );
    };
}

Sidebar.propTypes = {
    classes: PropTypes.object.isRequired
};

export default withStyles(sidebarStyle)(Sidebar);
