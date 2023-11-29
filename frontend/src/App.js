import "./App.css";
import "./webfont.css";
import * as React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Container from "@mui/material/Container";
import InputBase from "@mui/material/InputBase";
import SearchIcon from "@mui/icons-material/Search";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { Box, Typography } from "@mui/material";
import logo from "./logo.svg";

const theme = createTheme({
  palette: {
    mode: "dark",
  },
});

function LogoSection() {
  return <img src={logo} width={64} alt="Logo" />;
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

function ResultItem({ fontName, Text }) {
  /*
    fontName: the name of the font
    Text: the text to display copy
  */
  return (
    <Button
      variant="text"
      sx={{
        padding: 2,
        width: "15rem",
        justifyContent: "start",
      }}
    >
      <IconButton className={`nf ${fontName}`}></IconButton>
      <Typography variant="subtitle1">{Text}</Typography>
    </Button>
  );
}

function ResultListSection() {
  return (
    <Stack
      direction="row"
      flexWrap="wrap"
      sx={{
        width: 800,
        background: "orange",
      }}
    >
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
    </Stack>
  );
}

function FooterSection() {
  return <Typography variant="body2">copyright Jack Jiang</Typography>;
}

function App() {
  return (
    <React.Fragment>
      <ThemeProvider theme={theme}>
        <CssBaseline />

        {/* the logo section */}
        <Container sx={{ display: "flex", justifyContent: "center", py: 1 }}>
          <LogoSection />
        </Container>

        {/* the search section */}
        <Container sx={{ display: "flex", justifyContent: "center", py: 0 }}>
          <SearchBoxSection />
        </Container>

        {/* the result list section */}
        <Container
          sx={{
            display: "flex",
            justifyContent: "center",
            py: 1,
          }}
        >
          <ResultListSection />
        </Container>

        {/* the footer section */}
        <Container
          sx={{
            display: "flex",
            justifyContent: "center",
            py: 2,
          }}
        >
          <FooterSection />
        </Container>
      </ThemeProvider>
    </React.Fragment>
  );
}

export default App;
