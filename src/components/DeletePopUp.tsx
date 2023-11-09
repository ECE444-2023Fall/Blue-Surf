import React, { useState } from 'react';
import "../styles/DeletePopUp.css";

const DeletePopUp: React.FC = () => {
    const [showPopup, setShowPopup] = useState(false);

    const handleDeletePost = () => {
      // Delete post logic here
      console.log('Post deleted.');
      closePopup();
    };
  
    const closePopup = () => {
      setShowPopup(false);
    };

  
    return (
        <div className="container">
                <div className="popupbackground">
                    <div className="centered-text">
                            <p className="confirm-text">Are you sure you want to delete the post titled:</p>
                            <p className="event-text">Fall Career Week?</p>
                            <p className="undone-text">This action cannot be undone.</p>
                            <div className="row">
                            <button className = "yes-button" onClick={handleDeletePost}>Delete</button>
                            <button className = "no-button" onClick={closePopup}>Cancel</button>
                        </div>
                    </div>
                </div>
        </div> 
    );
  };

  
  export default DeletePopUp;
  