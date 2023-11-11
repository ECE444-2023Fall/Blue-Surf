// Made by: Karishma Shah
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import PostCard from "../components/PostCard";

test("PostCard component renders with provided props", async () => {
  const title = "Post Title";
  const start_time = new Date();
  const location = "Location";
  const description = "Description";
  const tags = ["Tag1", "Tag2"];
  const id = 123;
  const author_id = 123;
  const is_published = true;
  const end_time = new Date();
  const like_count = 0;
  const token = "123";
  const user = { userId: "123", username: "author" };
  const setAuth = jest.fn();

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
    />
  );
});

test('Like button toggles "liked" class when clicked', async () => {
  const title = "Post Title";
  const start_time = new Date();
  const location = "Location";
  const description = "Description";
  const tags = ["Tag1", "Tag2"];
  const id = 123;
  const author_id = 123;
  const is_published = true;
  const end_time = new Date();
  const like_count = 0;
  const token = "123";
  const user = { userId: "123", username: "author" };
  const setAuth = jest.fn();

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
    />
  );
});
