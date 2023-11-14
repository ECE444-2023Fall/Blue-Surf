import React from "react";
import { render, fireEvent, waitFor, screen } from "@testing-library/react";
import LandingPage from "../components/LandingPage";
import API_URL from "../config";

(global as any).fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve([]),
  })
);

describe("LandingPage Component", () => {
  test("renders without crashing", () => {
    render(<LandingPage token="" user={{ userId: "", username: "" }} setAuth={() => {}} />);
  });

  test("fetches events on mount", async () => {
    render(<LandingPage token="" user={{ userId: "", username: "" }} setAuth={() => {}} />);
    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/api/`));
  });

});
