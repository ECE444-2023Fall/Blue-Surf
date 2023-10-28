import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import userEvent from '@testing-library/user-event';
import SearchBar from './SearchBar'; 

// Mocking the fetch API call
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve(["Apple", "Orange"]),
  })
);

beforeEach(() => {
  fetch.mockClear();
});

describe('SearchBar Component', () => {
  test('renders SearchBar without crashing', () => {
    render(<SearchBar />);
    const inputElement = screen.getByPlaceholderText('Search...');
    expect(inputElement).toBeInTheDocument();
  });
});

