import ContentCopy from "@mui/icons-material/ContentCopy";
import SearchIcon from "@mui/icons-material/Search";
import { Box, Icon, Typography } from "@mui/material";
import Chip from "@mui/material/Chip";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import IconButton from "@mui/material/IconButton";
import InputBase from "@mui/material/InputBase";
import ListItemIcon from "@mui/material/ListItemIcon";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import * as React from "react";
import { useState } from "react";
import "./App.css";
import logo from "./logo.svg";
import unicodeLiteral from "./utils";
import "./webfont.css";
import Link from "@mui/material/Link";

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

function SearchBoxSection({ handleSearch, query, setQuery }) {
  return (
    <Paper
      component="form"
      sx={{ display: "flex", width: 600 }}
      onSubmit={(e) => {
        e.preventDefault();
        handleSearch();
      }}
    >
      <InputBase
        sx={{ ml: 1, flexGrow: 1 }}
        placeholder="Search for nerd fonts icons..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <IconButton
        type="submit"
        sx={{ p: "10px" }}
        aria-label="search"
        onClick={handleSearch}
      >
        <SearchIcon />
      </IconButton>
    </Paper>
  );
}

function ResultItemMenuItem({ handleClose, menuText }) {
  /* menuText will be copied to clipboard when clicked by handleClose
   */
  return (
    <MenuItem
      onClick={(e) => handleClose(menuText)}
      sx={{ fontFamily: "NerdFontsSymbols Nerd Font" }}
    >
      <ListItemIcon>
        <ContentCopy fontSize="small" />
      </ListItemIcon>
      {menuText}
    </MenuItem>
  );
}

function ResultItem({ result }) {
  /* result item, including chip and menu

  result object:

    ```
    {
        "font_name": "nf-md-cat",
        "series": "nf",
        "group": "md",
        "unicode": "f011b",
        "description": "cat"
    }
    ```
  */
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleOpenMenu = (event) => {
    // show result menu
    setAnchorEl(event.currentTarget);
  };
  const handleCloseMenu = (menuText) => {
    // close result menu and copy menuText to clipboard
    navigator.clipboard.writeText(menuText);
    setAnchorEl(null);
  };

  const font = String.fromCodePoint(`0x${result.unicode}`);

  return (
    <Box>
      {/* result item chip */}
      <Chip
        icon={<Icon className={`nf ${result.font_name}`} />}
        label={result.font_name}
        size="medium"
        clickable
        id="chip"
        aria-controls={open ? "menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open ? "true" : undefined}
        onClick={handleOpenMenu}
      />

      {/* result item menu */}
      <Menu
        id="menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleCloseMenu}
        MenuListProps={{
          "aria-labelledby": "chip",
        }}
      >
        <ResultItemMenuItem handleClose={handleCloseMenu} menuText={font} />
        <ResultItemMenuItem
          handleClose={handleCloseMenu}
          menuText={result.unicode}
        />
        <ResultItemMenuItem
          handleClose={handleCloseMenu}
          menuText={result.font_name}
        />
        <ResultItemMenuItem
          handleClose={handleCloseMenu}
          menuText={unicodeLiteral(font)}
        />
      </Menu>
    </Box>
  );
}

function ResultListSection({ searchResults }) {
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
      {searchResults.map((result, index) => (
        <ResultItem result={result} key={index}></ResultItem>
      ))}
    </Stack>
  );
}

function FooterSection() {
  return (
    <Container>
      <Box sx={{ textAlign: "center" }}>
        <Typography variant="body2">
          To display font icons in terminal/editor/apps, one of the{" "}
          <Link href="https://www.nerdfonts.com/" underline="none">
            Nerd Fonts
          </Link>{" "}
          needs to be used
        </Typography>
      </Box>

      <Box sx={{ textAlign: "center" }}>
        <Typography variant="body2">
          Copyright &copy; 2023&nbsp;
          <Link href="https://jackjyq.com/" underline="none">
            jackjyq.com
          </Link>
          . Open sourced on{" "}
          <Link href="https://github.com/jackjyq/nerd-fonts-icon-search">
            GitHub
          </Link>{" "}
          under{" "}
          <Link href="https://github.com/jackjyq/nerd-fonts-icon-search/blob/master/LICENSE">
            MIT License
          </Link>
          .
        </Typography>
      </Box>
    </Container>
  );
}

function App() {
  /* the main app, most of the layout is done here
  
  Refs:
    https://mui.com/material-ui/customization/breakpoints/
    https://mui.com/system/getting-started/the-sx-prop/#sizing
  */
  const [searchResults, setSearchResults] = useState([]);
  const [query, setQuery] = React.useState("");

  function handleSearch() {
    fetch(
      new URL(
        `/api/search?q=${encodeURIComponent(query)}`,
        process.env.REACT_APP_BACKEND_SERVER
      )
    )
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setSearchResults(data.results);
      })
      .catch((error) => {
        console.log(error);
      });
  }

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
          <SearchBoxSection
            handleSearch={handleSearch}
            query={query}
            setQuery={setQuery}
          />
        </Container>

        {/********************** the result list section *********************/}
        <Container
          sx={{
            display: "flex",
            justifyContent: "center",
            py: { xs: 1, sm: 2 },
          }}
        >
          <ResultListSection searchResults={searchResults} />
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
