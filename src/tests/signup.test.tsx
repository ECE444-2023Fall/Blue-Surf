import React from 'react';
import { render, fireEvent, screen, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import SignupPage from '../components/SignupPage';

jest.mock('react-router-dom', () => {
  const originalModule = jest.requireActual('react-router-dom');
  return {
    ...originalModule,
    useNavigate: jest.fn(),
  };
});

//Checks the page renders 
describe('SignupPage Component', () => {
  it('renders SignupPage component without crashing', () => {
    render(
      <MemoryRouter>
        <SignupPage />
      </MemoryRouter>
    );
  });
  
//Checks if the following fields are updated on userinput 
  it('typing in the username field updates state', () => {
    render(
      <MemoryRouter>
        <SignupPage />
      </MemoryRouter>
    );
    const usernameInput = screen.getByPlaceholderText('Username');

    fireEvent.change(usernameInput, { target: { value: 'NewUser' } });

    expect(usernameInput).toHaveValue('NewUser');
  });

  it('typing in the email field updates state', () => {
    render(
      <MemoryRouter>
        <SignupPage />
      </MemoryRouter>
    );
    const emailInput = screen.getByPlaceholderText('Email');

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });

    expect(emailInput).toHaveValue('test@example.com');
  });

  it('typing in the password field updates state', () => {
    render(
      <MemoryRouter>
        <SignupPage />
      </MemoryRouter>
    );
    const passwordInput = screen.getByPlaceholderText('Password');

    fireEvent.change(passwordInput, { target: { value: 'Password123' } });

    expect(passwordInput).toHaveValue('Password123');
  });

  it('typing in the confirmPassword field updates state', () => {
    render(
      <MemoryRouter>
        <SignupPage />
      </MemoryRouter>
    );
    const confirmPasswordInput = screen.getByPlaceholderText('Confirm Password');

    fireEvent.change(confirmPasswordInput, { target: { value: 'Password123' } });

    expect(confirmPasswordInput).toHaveValue('Password123');
  });

  it('clicking the "Create Account" button calls the signMeUp function', async () => {
    render(
      <MemoryRouter>
        <SignupPage />
      </MemoryRouter>
    );

    const createAccountButton = screen.getByText('Create Account');

    await act(async () => {
      fireEvent.click(createAccountButton);
    });

  });
});
