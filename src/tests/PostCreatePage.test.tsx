import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import PostCreatePage from '../components/PostCreatePage';

jest.mock('react-router-dom', () => {
  const originalModule = jest.requireActual('react-router-dom');
  return {
    ...originalModule,
    useNavigate: jest.fn(),
  };
});

describe('PostCreatePage Component', () => {
  it('renders PostCreatePage component without crashing', () => {
    render(
      <MemoryRouter>
        <PostCreatePage />
      </MemoryRouter>
    );
  });

  it('typing in the title field updates state', () => {
    render(
      <MemoryRouter>
        <PostCreatePage />
      </MemoryRouter>
    );
    const titleInput = screen.getByPlaceholderText('[enter title here]');

    fireEvent.change(titleInput, { target: { value: 'New Title' } });

    expect(titleInput).toHaveValue('New Title');
  });

  it('clicking on Cancel button navigates back', () => {
    const mockNavigate = jest.requireMock('react-router-dom').useNavigate;
    mockNavigate.mockClear();
    mockNavigate.mockReturnValue(jest.fn());

    render(
      <MemoryRouter>
        <PostCreatePage />
      </MemoryRouter>
    );

    const cancelButton = screen.getByText('Cancel');
    cancelButton.click();

    expect(mockNavigate).toHaveBeenCalled();
    expect(mockNavigate().mock.calls[0][0]).toEqual(-1);
  });
});
