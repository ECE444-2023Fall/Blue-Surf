// Made by: Karishma Shah
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import PostCard from '../components/PostCard';

test('PostCard component renders with provided props', async () => {
  const title = 'Post Title';
  const date = new Date();
  const location = 'Location';
  const description = 'Description';
  const tags = ['Tag1', 'Tag2'];

  render(
    <PostCard title={title} date={date} location={location} description={description} tags={tags} />
  );

  // Check if the title, date, location, description, and tags are rendered
  expect(screen.getByTestId('post-title')).toBeInTheDocument();
  expect(screen.getByTestId('post-date-location')).toBeInTheDocument();
  expect(screen.getByTestId('post-description')).toBeInTheDocument();
  tags.forEach((tag) => {
    expect(screen.getByText(tag)).toBeInTheDocument();
  });

  // Check if the post image is rendered
  expect(screen.getByAltText('...')).toBeInTheDocument();
});

test('Like button toggles "liked" class when clicked', async () => {
  const title = 'Post Title';
  const date = new Date();
  const location = 'Location';
  const description = 'Description';
  const tags = ['Tag1', 'Tag2'];

  render(
    <PostCard title={title} date={date} location={location} description={description} tags={tags} />
  );

  const likeButton = screen.getByTestId('like-button');

  expect(likeButton).not.toHaveClass('liked');
  fireEvent.click(likeButton);

  expect(likeButton).toHaveClass('liked');
  fireEvent.click(likeButton);

  expect(likeButton).not.toHaveClass('liked');
});