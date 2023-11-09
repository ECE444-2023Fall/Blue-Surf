import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import LoginPage from '../components/LoginPage';

const setAuthMock = jest.fn();

jest.mock('react-router-dom', () => {
  const originalModule = jest.requireActual('react-router-dom');
  return {
    ...originalModule,
    useNavigate: jest.fn(),
  };
});

describe('LoginPage Component', () => {
  it('renders LoginPage component without crashing', () => {
    render(
      <MemoryRouter>
        <LoginPage setAuth={setAuthMock} />
      </MemoryRouter>
    );
  });

  it('typing in the username field updates state', () => {
    render(
      <MemoryRouter>
        <LoginPage setAuth={setAuthMock} />
      </MemoryRouter>
    );
    const usernameInput = screen.getByPlaceholderText('Username/Email');

    fireEvent.change(usernameInput, { target: { value: 'testUser' } });

    expect(usernameInput).toHaveValue('testUser');
  });

  it('typing in the password field updates state', () => {
    render(
      <MemoryRouter>
        <LoginPage setAuth={setAuthMock} />
      </MemoryRouter>
    );
    const passwordInput = screen.getByPlaceholderText('Password');

    fireEvent.change(passwordInput, { target: { value: 'testPassword' } });

    expect(passwordInput).toHaveValue('testPassword');
  });

  it('renders error message when attempting to log in with missing fields', async () => {
    render(
      <MemoryRouter>
        <LoginPage setAuth={setAuthMock} />
      </MemoryRouter>
    );

    const loginButton = screen.getByText('Login');
    fireEvent.click(loginButton);

    await waitFor(() => {
      expect(screen.getByText('Username or email is required')).toBeInTheDocument();
      expect(screen.getByText('Password is required')).toBeInTheDocument();
    });
  });

  it('renders error message when login fails', async () => {
    // Mock the fetch function to simulate a failed login
    jest.spyOn(global, 'fetch').mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ 'error message': 'Invalid username or password' }),
        headers: new Headers({ 'Content-Type': 'application/json' }),
        statusText: 'Unauthorized',
      } as Response);

    render(
      <MemoryRouter>
        <LoginPage setAuth={setAuthMock} />
      </MemoryRouter>
    );

    const usernameInput = screen.getByPlaceholderText('Username/Email');
    const passwordInput = screen.getByPlaceholderText('Password');
    const loginButton = screen.getByText('Login');

    fireEvent.change(usernameInput, { target: { value: 'testUser' } });
    fireEvent.change(passwordInput, { target: { value: 'testPassword' } });

    fireEvent.click(loginButton);

    await waitFor(() => {
      expect(screen.getByText('Invalid username or password')).toBeInTheDocument();
    });
  });

});
