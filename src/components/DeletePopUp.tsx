import React from "react";
import "../styles/DeletePopUp.css";

const DeletePopUp: React.FC<{
  postTitle: string;
  handleDelete: (confirmed: boolean) => void;
  page?: string;
}> = ({ postTitle, handleDelete, page }) => {
  const confirmDelete = () => {
    handleDelete(true);
  };

  const cancelDelete = () => {
    handleDelete(false);
  };

  const containerStyle = {
    width: page === "dashboard" ? "90%" : "100%",
  };

  return (
    <div className="popup-container" style={containerStyle}>
      <div className="popupbackground">
        <div className="centered-text">
          <p className="confirm-text">
            Are you sure you want to delete the post titled:
          </p>
          <p className="event-text">{postTitle}</p>
          <p className="undone-text">This action cannot be undone.</p>
          <div className="row">
            <button className="yes-button" onClick={confirmDelete}>
              Delete
            </button>
            <button className="no-button" onClick={cancelDelete}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeletePopUp;
