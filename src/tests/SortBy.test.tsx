// Made by: Karishma Shah
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import SortBy from "../components/SortBy";

test("SortBy component renders with provided options", () => {
  const options = ["Option 1", "Option 2"];
  const onSortChange = jest.fn();

  render(<SortBy options={options} onSortChange={onSortChange} />);

  expect(screen.getByText("Sort by")).toBeInTheDocument();

  const selectElement = screen.getByRole("combobox");

  fireEvent.change(selectElement, { target: { value: "Option 2" } });

  // Check if the selected option is reflected in the component
  expect(selectElement).toHaveValue("Option 2");
});
