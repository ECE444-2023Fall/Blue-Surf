import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import userEvent from '@testing-library/user-event';
import SearchBar from './SearchBar'; 

describe('SearchBar Component', () => {
  const mockSearchQuery = 'Sample Event';

  beforeEach( () => {
    global.fetch = jest.fn().mockImplementation(() =>
    Promise.resolve({
        json: () => Promise.resolve([
          {
            "event_id": 1,
            "title": "Sample Event 1",
            "description": "This is the first sample event.",
            "location": "Sample Location 1",
            "start_time": "2023-11-01T08:00:00",
            "end_time": "2023-11-01T17:00:00",
            "user_id": 1,
            "is_published": 'True',
            "is_public": 'True',
            "like_count": 25
          }]),
        ok: true, // Ensure the response is considered 'ok'
      })
    );
  });

  afterEach(() => {
    global.fetch.mockClear(); // Reset the mock function
  });
  
  test('renders SearchBar without crashing', () => {
    render(<SearchBar onDataReceived={jest.fn()}/>);
    const inputElement = screen.getByPlaceholderText('Search...');
    expect(inputElement).toBeInTheDocument();
  });

  test('fetches suggestions on user input change', async () => {
    render(<SearchBar  onDataReceived={jest.fn()}/>);
    const inputElement = screen.getByPlaceholderText('Search...');
    
    userEvent.type(inputElement, mockSearchQuery);
    
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(mockSearchQuery.length);
    });

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/autosuggest?query='+mockSearchQuery);
    });
  });

  test('triggers search on pressing Enter', async () => {
    render(<SearchBar onDataReceived={jest.fn()} />);
    const inputElement = screen.getByPlaceholderText('Search...');

    userEvent.type(inputElement, mockSearchQuery+'{enter}');
    
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(mockSearchQuery.length+1);
    });

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/search?query='+mockSearchQuery);
    });
  });  
});

