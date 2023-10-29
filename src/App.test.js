import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

test('displays "No search results available." message on initial load', () => {
  render(<App />);
  const messageElement = screen.getByText(/No search results available./i);
  expect(messageElement).toBeInTheDocument();
});