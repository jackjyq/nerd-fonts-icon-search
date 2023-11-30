import SearchIcon from "@mui/icons-material/Search";
import { Box, Icon, Typography } from "@mui/material";
import Chip from "@mui/material/Chip";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import IconButton from "@mui/material/IconButton";
import InputBase from "@mui/material/InputBase";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import * as React from "react";
import "./App.css";
import logo from "./logo.svg";
import "./webfont.css";
import ListItemIcon from "@mui/material/ListItemIcon";
import ContentCopy from "@mui/icons-material/ContentCopy";

const theme = createTheme({
  palette: {
    mode: "dark",
  },
});

function LogoSection() {
  return (
    <Box sx={{ width: { xs: 80, sm: 160 } }}>
      <img src={logo} alt="Logo" />
    </Box>
  );
}

function SearchBoxSection() {
  return (
    <Paper component="form" sx={{ display: "flex", width: 600 }}>
      <InputBase
        sx={{ ml: 1, flexGrow: 1 }}
        placeholder="Search for nerd fonts icons..."
      />
      <IconButton type="button" sx={{ p: "10px" }} aria-label="search">
        <SearchIcon />
      </IconButton>
    </Paper>
  );
}

function FontIcon({ fontName }) {
  return <Icon className={`nf ${fontName}`} />;
}

function ResultItem({ fontName, label, menuTexts }) {
  /* result item

    props:
      - fontName: the font name to display the icon
      - label: the text to display after the icon
      - menuTexts: an array of strings to copy to clipboard
  */
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box>
      <Chip
        icon={FontIcon((fontName = { fontName }))}
        label={label}
        size="medium"
        clickable
        id="chip"
        aria-controls={open ? "menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open ? "true" : undefined}
        onClick={handleClick}
      />

      <Menu
        id="menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          "aria-labelledby": "chip",
        }}
      >
        {menuTexts.map((text) => (
          <MenuItem onClick={handleClose}>
            <ListItemIcon>
              <ContentCopy fontSize="small" />
            </ListItemIcon>
            {text}
          </MenuItem>
        ))}
      </Menu>
    </Box>
  );
}

function ResultListSection() {
  return (
    <Stack
      direction="row"
      flexWrap="wrap"
      spacing={2}
      useFlexGap
      sx={{
        width: 900,
      }}
    >
      <ResultItem
        fontName={"nf-md-cat"}
        label={"cat"}
        menuTexts={["a", "b", "c"]}
      ></ResultItem>
    </Stack>
  );
}

function FooterSection() {
  return <Typography variant="body2">copyright Jack Jiang</Typography>;
}

function App() {
  /* the main app, most of the layout is done here
  
  Refs:
    https://mui.com/material-ui/customization/breakpoints/
    https://mui.com/system/getting-started/the-sx-prop/#sizing
  */
  return (
    <React.Fragment>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {/************************* the logo section *************************/}
        <Container
          sx={{
            display: "flex",
            justifyContent: "center",
            pt: { xs: 1, sm: 8 },
          }}
        >
          <LogoSection />
        </Container>

        {/************************* the search section ***********************/}
        <Container
          sx={{
            display: "flex",
            justifyContent: "center",
            py: { xs: 1, sm: 2 },
          }}
        >
          <SearchBoxSection />
        </Container>

        {/********************** the result list section *********************/}
        <Container
          sx={{
            display: "flex",
            justifyContent: "center",
            py: { xs: 1, sm: 2 },
          }}
        >
          <ResultListSection />
        </Container>

        {/************************ the footer section ************************/}
        <Container
          sx={{
            display: "flex",
            justifyContent: "center",
            py: 4,
          }}
        >
          <FooterSection />
        </Container>
      </ThemeProvider>
    </React.Fragment>
  );
}

export default App;
