import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import PostCard from "../components/PostCard";

jest.mock("node-fetch");

const sampleProps = {
  title: "Test Post",
  start_time: new Date(),
  location: "Test Location",
  description: "Test Description",
  tags: ["tag1", "tag2"],
  id: 1,
  author_id: 123,
  is_published: true,
  end_time: new Date(),
  like_count: 0,
  token: "sampleToken",
  user: { userId: "123", username: "testuser" },
  setAuth: jest.fn(),
  showDeletePopUp: jest.fn(),
};

describe("PostCard Component", () => {
  it("renders with correct data", () => {
    render(<PostCard {...sampleProps} />);
    
    expect(screen.getByTestId("post-title")).toHaveTextContent(sampleProps.title);
    
    expect(screen.getByTestId("post-date-location")).toHaveTextContent(`${sampleProps.start_time} | ${sampleProps.location}`);
    
    expect(screen.getByTestId("post-description")).toHaveTextContent(sampleProps.description);
    
    sampleProps.tags.forEach((tag) => {
      expect(screen.getByTestId("post-tags")).toHaveTextContent(tag);
    });
  });

  it("handles like button click", async () => {
    render(<PostCard {...sampleProps} />);
    
    (global as any).fetch.mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValueOnce({ access_token: "newToken" }),
    });
    
    fireEvent.click(screen.getByTestId("like-button"));
    
    await waitFor(() => {
      expect(sampleProps.setAuth).toHaveBeenCalledWith("newToken", sampleProps.user);
    });

    await waitFor(() => {
      expect(screen.getByTestId("like-button")).toHaveClass("liked");
    })
  });

  it("handles delete button click", () => {
    render(<PostCard {...sampleProps} />);
    
    fireEvent.click(screen.getByText("Delete"));
    
    expect(sampleProps.showDeletePopUp).toHaveBeenCalledWith(sampleProps.id, sampleProps.title);
  });
});
