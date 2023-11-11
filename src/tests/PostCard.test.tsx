import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import PostCard from "../components/PostCard";

describe("PostCard Component", () => {
  interface User {
    userId: string;
    username: string;
  }

  let title: string, start_time: Date, location: string, description: string, tags: [string, string], id: number, author_id: number, is_published: boolean, end_time: Date, like_count: number, token: string, user: User, setAuth: () => void, showDeletePopUp: () => void

  beforeEach(() => {
    title = "Post Title";
    start_time = new Date();
    location = "Location";
    description = "Description";
    tags = ["Tag1", "Tag2"];
    id = 123;
    author_id = 123;
    is_published = true;
    end_time = new Date();
    like_count = 0;
    token = "123";
    user = { userId: '123', username: 'author' };
    setAuth = jest.fn();
    showDeletePopUp = jest.fn();
  });

  beforeEach(() => {
    title = "Post Title";
    start_time = new Date();
    location = "Location";
    description = "Description";
    tags = ["Tag1", "Tag2"];
    id = 123;
    author_id = 123;
    is_published = true;
    end_time = new Date();
    like_count = 0;
    token = "123";
    user = { userId: '123', username: 'author' };
    setAuth = jest.fn();
    showDeletePopUp = jest.fn();
  });

test("PostCard component renders with provided props", async () => {

  render(
    <PostCard
      id={id}
      title={title}
      start_time={start_time}
      location={location}
      description={description}
      tags={tags}
      author_id={author_id}
      is_published={is_published}
      end_time={end_time}
      like_count={like_count}
      token={token}
      user={user}
      setAuth={setAuth}
      showDeletePopUp={showDeletePopUp}
    />
  );

  // Check if the title, date, location, description, and tags are rendered
  expect(screen.getByTestId("post-title")).toBeInTheDocument();
  expect(screen.getByTestId("post-date-location")).toBeInTheDocument();
  expect(screen.getByTestId("post-description")).toBeInTheDocument();
  tags.forEach((tag) => {
    expect(screen.getByText(tag)).toBeInTheDocument();
  });

  // Check if the post image is rendered
  expect(screen.getByAltText("...")).toBeInTheDocument();
});

test('Like button toggles "liked" class when clicked', async () => {

  render(
    <PostCard
      id={id}
      title={title}
      start_time={start_time}
      location={location}
      description={description}
      tags={tags}
      author_id={author_id}
      is_published={is_published}
      end_time={end_time}
      like_count={like_count}
      token={token}
      user={user}
      setAuth={setAuth}
      showDeletePopUp={showDeletePopUp}
    />
  );

  const likeButton = screen.getByTestId("like-button");

    expect(likeButton).not.toHaveClass("liked");
    fireEvent.click(likeButton);

    expect(likeButton).toHaveClass("liked");
    fireEvent.click(likeButton);

    expect(likeButton).not.toHaveClass("liked");
    // Additional test logic to simulate functionality on like button click
    // For example, checking if like count increases or an API call is made
  });
});
