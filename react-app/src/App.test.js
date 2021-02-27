import { render, screen } from "@testing-library/react";
import App from "./App";

// check if 'MTurk' label exists and is visible on NavBar
test("MTurk exists/visible", () => {
  render(<App />);
  expect(screen.getByText("MTurk")).toBeInTheDocument();
});

// check if 'Home' exists and is visible on NavBar
test("Home exists/visible", () => {
  render(<App />);
  expect(screen.getByText("Home")).toBeInTheDocument();
});

// check if 'About' exists and is visible on NavBar
test("About exists/visible", () => {
  render(<App />);
  expect(screen.getByText("About")).toBeInTheDocument();
});

// check if 'Login' exists and is visible on NavBar
test("Login exists/visible", () => {
  render(<App />);
  expect(screen.getByText("Login")).toBeInTheDocument();
});
