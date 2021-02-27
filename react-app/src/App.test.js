import { render, screen } from "@testing-library/react";
import App from "./App";

// check if 'MTurk' exists and is visible on NavBar
test("MTurk on NavBar exists and is visible", () => {
  render(<App />);
  expect(screen.getByText("MTurk")).toBeInTheDocument();
});

// check if 'Home' exists and is visible on NavBar
test("Home on NavBar exists and is visible", () => {
  render(<App />);
  expect(screen.getByText("Home")).toBeInTheDocument();
});

// check if 'About' exists and is visible on NavBar
test("About on NavBar exists and is visible", () => {
  render(<App />);
  expect(screen.getByText("About")).toBeInTheDocument();
});

// check if 'Login' exists and is visible on NavBar
test("Login on NavBar exists and is visible", () => {
  render(<App />);
  expect(screen.getByText("Login")).toBeInTheDocument();
});
