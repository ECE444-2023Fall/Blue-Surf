import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { MemoryRouter } from 'react-router-dom';
import PersonalDashboard from '../components/PersonalDashboard';

jest.mock('axios'); // Mocking axios

describe('PersonalDashboard Component', () => {
  const mockSetAuth = jest.fn();
  const mockUser = { userId: '123', username: 'testUser' };
  const mockToken = 'mockToken';

  it('renders PersonalDashboard component without crashing', () => {
    render(
      <MemoryRouter>
        <PersonalDashboard token={mockToken} user={mockUser} setAuth={mockSetAuth} />
      </MemoryRouter>
    );
  });

  it('displays loading message initially', () => {
    render(
      <MemoryRouter>
        <PersonalDashboard token={mockToken} user={mockUser} setAuth={mockSetAuth} />
      </MemoryRouter>
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('displays search bar and buttons', () => {
    render(
      <MemoryRouter>
        <PersonalDashboard token={mockToken} user={mockUser} setAuth={mockSetAuth} />
      </MemoryRouter>
    );
  });

  it('fetches and displays posts on button click', async () => {
    render(
      <MemoryRouter>
        <PersonalDashboard token={mockToken} user={mockUser} setAuth={mockSetAuth} />
      </MemoryRouter>
    );

    // Mocking the API response
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([]),
    });

    // Click on the "Favourites" button
    fireEvent.click(screen.getByText('Favourites'));

    // Wait for the asynchronous fetchEvents function to complete
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('favourites'), expect.any(Object));
    });
  });

  it('navigates to the create page on "Create Post" button click', () => {
    const { container } = render(
      <MemoryRouter>
        <PersonalDashboard token={mockToken} user={mockUser} setAuth={mockSetAuth} />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByText('Create Post'));

  });

});
