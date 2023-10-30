import { render, screen } from '@testing-library/react';
import App from './App';

// Paula Perdomo
test('displays "No search results available." message on initial load', () => {
  render(<App />);
  const messageElement = screen.getByText(/No search results available./i);
  expect(messageElement).toBeInTheDocument();
});