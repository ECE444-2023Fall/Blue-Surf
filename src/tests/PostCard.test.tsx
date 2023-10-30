// Made by: Karishma Shah
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
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

  console.log(document.body.innerHTML);

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
