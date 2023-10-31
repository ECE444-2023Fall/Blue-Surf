import React, { useState } from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/PostCreation.css";
import ImageUpload from './ImageUpload';
//import ImageUploadButton from './ImageUploadButton';
//import DisplayImage from './DisplayImage';

{/*interface TagOptions{
    title: string; 
    value: string[]; 
}*/}

const PostCreation: React.FC = () => {

  const [uploadedImageUrl, setUploadedImageUrl] = useState<string | null>(null);

  const handleImageUpload = (imageUrl: string) => {
    setUploadedImageUrl(imageUrl);
  };

  return (
    <div>
      {/* Head Content */}
      <head>
        <title>Post Creation</title>
        <link rel="stylesheet" type="text/css" href="../static/postcreation-styles.css" />
        <link href="https://fonts.googleapis.com/css?family=Karla:400,700" rel="stylesheet" />
        <script src="../animations/postcreation.js"></script>
      </head>

      {/* Content */}
      <div className="split-container">
        <div className="left">
        {uploadedImageUrl && (
          <div className="uploaded-image">
            <img src={uploadedImageUrl} alt="Uploaded" style={{ width: '400px', height: '500px' }} />
          </div>
        )}
          <div className="preview-container">
            <button type="button" className="preview-button">See Preview</button>
          </div>
        </div>
        <div className="right">
          <div className="post-input">
            <form method="post" action="/">
              <div className="form-group">
                <label htmlFor="title" className="title-label">Title</label>
                <input type="text" id="title" name="title" className="form-control input-boxes" placeholder="Post Title" />
              </div>
              <div className="form-group">
                <label htmlFor="location" className="input-labels">Location</label>
                <input type="text" id="location" name="location" className="form-control input-boxes" placeholder="Location" />
              </div>
              <div className="form-group">
                <label htmlFor="event-time" className="input-labels">Event Time</label>
                <input type="datetime-local" id="event-time" name="event-time" className="event-time" />
              </div>
              <div className="form-group">
                <label htmlFor="expiry-date" className="input-labels">Expiry Date</label>
                <input type="datetime-local" id="expiry-date" name="expiry-time" className="event-time" />
              </div>
              <div className="form-group">
                <label htmlFor="details" className="input-labels">Details</label>
                <input type="text" id="details" name="details" className="form-control input-boxes" placeholder="Enter any other details." />
              </div>
              <div className="image-upload">
                <label htmlFor="customFile" className="input-labels">Image</label>
                <div>
                  <ImageUpload onImageUpload={handleImageUpload} />
                </div>
              </div>
              <div className="dropdown">
                <select name="language" id="language">
                  <option value="Tags" selected>Tags</option>
                  <option value="javascript">JavaScript</option>
                  <option value="python">Python</option>
                  <option value="c++" disabled>C++</option>
                  <option value="java">Java</option>
                </select>
              </div>
              <div className="save-delete">
                <button type="submit" className="save-button" id="saveButton">Save</button>
                <button type="button" className="delete-button" id="deleteButton">Delete</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostCreation;
