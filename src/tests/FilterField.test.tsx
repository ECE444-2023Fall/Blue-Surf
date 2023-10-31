// Made by: Karishma Shah
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import FilterField from "../components/FilterField";

test("FilterField component renders with provided props and handles user interaction", () => {
  const title = "Filter Title";
  const values = ["Option 1", "Option 2"];

  render(<FilterField title={title} values={values} />);

  // Check if the title and options are initially rendered
  expect(screen.getByText(title)).toBeInTheDocument();

  // Simulate selecting an option and check if it changes
  const selectElement = screen.getByRole("combobox");
  fireEvent.change(selectElement, { target: { value: "Option 2" } });

  // Check if the selected option is reflected in the component
  expect(selectElement).toHaveValue("Option 2");
});
