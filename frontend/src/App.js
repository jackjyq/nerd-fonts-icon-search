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

function Logo() {
  return (
    <Box display="flex" justifyContent="center">
      <img src={logo} alt="Logo" />
    </Box>
  );
}

function SearchBox() {
  return (
    <Paper
      component="form"
      sx={{
        p: "2px 4px",
        mt: 2,
        display: "flex",
        alignItems: "center",
        maxWidth: 600,
      }}
    >
      <InputBase sx={{ ml: 1, flex: 1 }} placeholder="Search for glyphs..." />
      <IconButton type="button" sx={{ p: "10px" }} aria-label="search">
        <SearchIcon />
      </IconButton>
    </Paper>
  );
}

function ResultFormatRadioButtons() {
  return (
    <FormControl>
      <RadioGroup
        row
        name="result-format-radio-buttons"
        defaultValue="font-name"
      >
        <FormControlLabel
          value="font-name"
          control={<Radio />}
          label="font name"
        />
        <FormControlLabel
          value="hex-code"
          control={<Radio />}
          label="hex code"
        />
      </RadioGroup>
    </FormControl>
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

function ResultArea() {
  return (
    <Stack
      direction="row"
      flexWrap="wrap"
      sx={{
        borderTop: 1,
        borderColor: "divider",
      }}
    >
      <ResultItem fontName={"nf-md-cat"} Text={"cat"}></ResultItem>
    </Stack>
  );
}

function App() {
  return (
    <React.Fragment>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Container maxWidth="xl">
          <Logo></Logo>
          <SearchBox />
          <ResultFormatRadioButtons />
          <ResultArea />
        </Container>
      </ThemeProvider>
    </React.Fragment>
  );
}

export default App;
