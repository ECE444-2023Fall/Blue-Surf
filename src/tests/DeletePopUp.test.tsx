import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import DeletePopUp from '../components/DeletePopUp';

describe('DeletePopUp Component', () => {
  const mockHandleDelete = jest.fn();

  const renderComponent = (postTitle: string, page: string | undefined) => {
    render(
      <DeletePopUp postTitle={postTitle} handleDelete={mockHandleDelete} page={page} />
    );
  };

  it('renders DeletePopUp component without crashing', () => {
    renderComponent('Test Post', 'dashboard');
  });

  it('displays the correct post title', () => {
    renderComponent('Test Post', 'dashboard');

    const postTitleElement = screen.getByText('Test Post');
    expect(postTitleElement).toBeInTheDocument();
  });

  it('calls handleDelete with true when "Delete" button is clicked', () => {
    renderComponent('Test Post', 'dashboard');

    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);

    expect(mockHandleDelete).toHaveBeenCalledWith(true);
  });

  it('calls handleDelete with false when "Cancel" button is clicked', () => {
    renderComponent('Test Post', 'dashboard');

    const cancelButton = screen.getByText('Cancel');
    fireEvent.click(cancelButton);

    expect(mockHandleDelete).toHaveBeenCalledWith(false);
  });
});
