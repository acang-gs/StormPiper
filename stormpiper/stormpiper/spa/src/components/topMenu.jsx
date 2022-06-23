import AppBar from "@material-ui/core/AppBar";
import Drawer from '@material-ui/core/Drawer';
import Toolbar from "@material-ui/core/Toolbar";
import { List, ListItem } from "@material-ui/core";
import IconButton from "@material-ui/core/IconButton";
import HomeRoundedIcon from "@material-ui/icons/HomeRounded"
import InfoRoundedIcon from "@material-ui/icons/InfoRounded"
import GridOnRoundedIcon from "@material-ui/icons/GridOnRounded"
import ScatterPlotRoundedIcon from "@material-ui/icons/ScatterPlotRounded"
import Typography from "@material-ui/core/Typography";
import { useTheme,makeStyles,styled } from "@material-ui/core/styles";
import MenuIcon from "@material-ui/icons/Menu";
import SearchIcon from "@material-ui/icons/Search";
import MoreIcon from "@material-ui/icons/MoreVert";
import Grid from "@material-ui/core/Grid";
import WorkflowModal from "./workflowModal";
import EvaluateProjects from "./evaluateProject";
import EvaluateWatersheds from "./evaluateWatersheds";
import UserAdminMenu from "./userAdminMenu";
import Reports from "./reports";
import About from "./about";
import Help from "./help";
import logo from "../assets/img/TacomaLogoSM.jpeg";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft"
import ChevronRightIcon from "@material-ui/icons/ChevronRight"
import { useState } from "react";

const useStyles = makeStyles((theme) => ({
  root: {
    position: "fixed",
    zIndex: 10,
    top: 0,
    bottom: 0,
    left:0,
    overflowX: "hidden",
    overflowY: "hidden",
    height: "8%",
    width: "100%",
    // background: "rgb(36, 21, 170)",
  },

  gridRoot: {
    zIndex: 10,
    height: "100%",
  },

  menuButton: {
    marginRight: theme.spacing(2),
  },
  gridRow: {
    height: "100%",
  },
  toolbar: {
    zIndex: 10,
    alignItems: "flex-start",
    paddingTop: theme.spacing(1),
    paddingBottom: theme.spacing(2),
    height: "100%",
  },
  title: {
    flexGrow: 1,
    textAlign:"left",
    alignSelf: "flex-start",
  },
  menuItem: {
    flexGrow: 1,
    alignSelf: "flex-start",
  },
}));

const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.easeInOut,
    duration: 1000,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.easeInOut,
    duration: 1000,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-start',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

const CustomAppBar = styled(AppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  height:60,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const CustomDrawer = styled(Drawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  }),
);

export default function ProminentAppBar(props) {
  const classes = useStyles();
  const theme = useTheme()

  const [open,setOpen] = useState(false)

  const [buttonConfig,setButtonConfig] = useState({
    home:{
      label:"Home",
      icon:<HomeRoundedIcon/>
    },
    project:{
      label:"Evaluate Project",
      icon:<ScatterPlotRoundedIcon/>
    },
    watershed:{
      label:"Evaluate Watershed",
      icon:<GridOnRoundedIcon/>
    },
    about:{
      label:"About",
      icon:<InfoRoundedIcon/>
    }
  })

  const [selectedButton,setSelectedButton] = useState("Home")

  function handleDrawerClose(){
    setOpen(false)
  }
  function handleDrawerOpen(){
    setOpen(true)
  }

  return (
    <div className={classes.root}>
      <CustomAppBar open={open} position="fixed">
        {/* <Toolbar className={classes.toolbar}> */}
        <Grid
          container
          spacing={1}
          className={classes.gridRow}
          alignItems="flex-start"
        >
          <Toolbar>
            <IconButton
              id="top-menu-hamburger"
              color="inherit"
              aria-label="open drawer"
              onClick={handleDrawerOpen}
              edge="start"
              sx={{
                marginRight: 5,
                ...(open && { display: "none" }),
              }}
            >
              <MenuIcon />
            </IconButton>
            {/* <div>
              <img alt="" src={logo} height="60px" width="auto" padding="5px" />
          </div> */}
            <Typography variant="h6" noWrap component="div">
              Tacoma Watershed Insights
            </Typography>
          </Toolbar>
        </Grid>
      </CustomAppBar>
      <CustomDrawer variant="permanent" open={open}>
        <div>
          <IconButton id="top-menu-chevron" onClick={handleDrawerClose}>
            {theme.direction === "ltr" ? (
              <ChevronLeftIcon />
            ) : (
              <ChevronRightIcon />
            )}
          </IconButton>
        </div>
        <DrawerHeader sx={{ minHeight: 0 }}>
          <List>
            {open ? (
              <ListItem>
                <Typography variant="subtitle1">Hello User</Typography>
              </ListItem>
            ) : (
              <p></p>
            )}
            {open ? (
              <ListItem>
                <Typography variant="subtitle2">user@stormpiper.com</Typography>
              </ListItem>
            ) : (
              <p></p>
            )}
          </List>
        </DrawerHeader>
        <List alignItems="flex-start">
          {Object.keys(buttonConfig).map((b) => {
            const button = buttonConfig[b];
            return (
              <ListItem>
                <WorkflowModal
                  workflowTitle={button.label}
                  iconComponent={button.icon}
                  displayTitle={open}
                  clickHandler={() => {
                    setSelectedButton(button.label);
                  }}
                  selected={selectedButton}
                ></WorkflowModal>
              </ListItem>
            );
          })}
        </List>
      </CustomDrawer>
    </div>
  );
}
