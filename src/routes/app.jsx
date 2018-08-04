import DashboardPage from "../views/Dashboard/Dashboard.jsx";
import UserProfile from "../views/UserProfile/UserProfile.jsx";
import TableList from "../views/TableList/TableList.jsx";
import Typography from "../views/Typography/Typography.jsx";
import Icons from "../views/Icons/Icons.jsx";
import Maps from "../views/Maps/Maps.jsx";
import NotificationsPage from "../views/Notifications/Notifications.jsx";
import Items from "../views/Items/Items.jsx";
import Login from "../views/Login/Login.jsx";

import {BubbleChart, ContentPaste, Dashboard, LibraryBooks, LocationOn, Notifications, Person} from "material-ui-icons";

const appRoutes = [
    {
        path: "/dashboard",
        sidebarName: "Dashboard",
        navbarName: "Material Dashboard",
        icon: Dashboard,
        component: DashboardPage
    },
    {
        path: "/user",
        sidebarName: "User Profile",
        navbarName: "Profile",
        icon: Person,
        component: UserProfile
    },
    {
        path: "/table",
        sidebarName: "Table List",
        navbarName: "Table List",
        icon: ContentPaste,
        component: TableList
    },
    {
        path: "/login",
        sidebarName: "login",
        navbarName: "Login",
        icon: ContentPaste,
        component: Login
    },
    {
        path: "/typography",
        sidebarName: "Typography",
        navbarName: "Typography",
        icon: LibraryBooks,
        component: Typography
    },
    {
        path: "/icons",
        sidebarName: "Icons",
        navbarName: "Icons",
        icon: BubbleChart,
        component: Icons
    },
    {
        path: "/maps",
        sidebarName: "Maps",
        navbarName: "Map",
        icon: LocationOn,
        component: Maps
    },
    {
        path: "/notifications",
        sidebarName: "Notifications",
        navbarName: "Notifications",
        icon: Notifications,
        component: NotificationsPage
    },
    {
        path: "/items",
        sidebarName: "Items",
        navbarName: "Items",
        icon: Notifications,
        component: Items
    },
    {
        sidebarName: "Items",
        navbarName: "Items",
        icon: ContentPaste,
        // component: TableList,
        children: [
            {
                path: "/table2/test",
                sidebarName: "All",
                navbarName: "All",
                icon: Notifications,
                component: TableList,
            },
            {
                path: "/table2/test",
                sidebarName: "Active",
                navbarName: "Active",
                icon: Notifications,
                component: TableList,
            },
                        {
                path: "/table2/test",
                sidebarName: "Not Active",
                navbarName: "Not Active",
                icon: Notifications,
                component: TableList,
            },
                        {
                path: "/table2/test",
                sidebarName: "Drafts",
                navbarName: "Drafts",
                icon: Notifications,
                component: TableList,
            },
        ]
    },
    {
        sidebarName: "Sales",
        navbarName: "Sales",
        icon: ContentPaste,
        // component: TableList,
        children: [
            {
                path: "/table2/test",
                sidebarName: "Sold",
                navbarName: "Sold",
                icon: Notifications,
                component: TableList,
            },
            {
                path: "/table2/test",
                sidebarName: "Awaiting Postage",
                navbarName: "Awaiting Postage",
                icon: Notifications,
                component: TableList,
            },
                        {
                path: "/table2/test",
                sidebarName: "Awaiting Payment",
                navbarName: "Awaiting Payment",
                icon: Notifications,
                component: TableList,
            },
                        {
                path: "/table2/test",
                sidebarName: "Paid and Dispatched",
                navbarName: "Sold",
                icon: Notifications,
                component: TableList,
            },
                        {
                path: "/table2/test",
                sidebarName: "Returns",
                navbarName: "Returns",
                icon: Notifications,
                component: TableList,
            },
        ]
    },

    {redirect: true, path: "/", to: "/dashboard", navbarName: "Redirect"}
];

export default appRoutes;