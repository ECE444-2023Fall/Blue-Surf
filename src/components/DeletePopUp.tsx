import React from 'react';
import "../styles/DeletePopUp.css";

const DeletePopUp: React.FC<{
  handleDelete: (confirmed: boolean) => void;
}> = ({ handleDelete }) => {

  const confirmDelete = () => {
    handleDelete(true);
  };

  const cancelDelete = () => {
    handleDelete(false);
  };

  
    return (
        <div className="popup-container">
                <div className="popupbackground">
                    <div className="centered-text">
                            <p className="confirm-text">Are you sure you want to delete the post titled:</p>
                            <p className="event-text">Fall Career Week?</p>
                            <p className="undone-text">This action cannot be undone.</p>
                            <div className="row">
                            <button className = "yes-button" onClick={confirmDelete}>Delete</button>
                            <button className = "no-button" onClick={cancelDelete}>Cancel</button>
                        </div>
                    </div>
                </div>
        </div> 
    );
  };

  
  export default DeletePopUp;
  