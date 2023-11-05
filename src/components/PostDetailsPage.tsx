import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostDetailsPage.css";
import AutoSizeTextArea from "./AutoSizeTextArea";
const postImage = require("../assets/post1.jpeg");

const PostDetailsPage: React.FC = () => {
  const { postId } = useParams();
  const postIdNumber = postId ? parseInt(postId) : 0;

  const [post, setPost] = useState<any>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [imageSrc, setImageSrc] = useState(postImage);

  useEffect(() => {
    // Fetch the post data for the specified postId

    // For now, use mock data based on postId
    const mockData = {
      0: {
        title: "Fall Career Week",
        date: new Date(),
        location: "Myhal 5th Floor",
        description:
          "Come out to the Fall Career Week to meet recruiters from companies like RBC, Tesla and more!",
        extendedDescription:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. RSVP HERE.",
        club: "You’re Next Career Network - YNCN",
        tags: ["Professional Development"],
      },
    };

    // Check if the postId is valid and exists in your data
    if (!isNaN(postIdNumber) && postIdNumber in mockData) {
      setPost(mockData[0] as any);
    } else {
      // PostId is invalid
      console.error("Invalid postId:", postId);
    }
  }, [postId]);

  // Post data is not yet available
  if (!post) {
    return <div>Loading...</div>;
  }

  const toggleEdit = () => {
    setIsEditing(!isEditing);
  };

  const handleSave = () => {
    // Perform the save action (e.g., send data to the server via POST)
    setIsEditing(false);
  };

  const handleCancel = () => {
    // Revert any changes made in editing mode
    setIsEditing(false);
  };

  const handleFileChange = (event: any) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      const reader = new FileReader();

      reader.onload = (e) => {
        const newImageSrc = e.target && e.target.result;
        setImageSrc(newImageSrc);
      };

      reader.readAsDataURL(selectedFile);
    }
  };

  return (
    <div className="container background-colour rounded-5 p-5 mt-2 mb-2">
      <div className="row m-2">
        <a className="navbar-brand back-nav" href="javascript:history.back()">
          <img
            src="https://cdn-icons-png.flaticon.com/512/271/271220.png"
            width="15"
            height="15"
            className="d-inline-block align-items-center"
            alt=""
          />
          <span className="back-text">Back</span>
        </a>
        <div className="row m-2 justify-content-end">
          {isEditing ? (
            <>
              <button className="cancel-button" onClick={handleCancel}>
                Cancel
              </button>
              <button className="edit-button" onClick={handleSave}>
                Save
                <i className="fa fa-floppy-disk"></i>
              </button>
            </>
          ) : (
            <button className="edit-button" onClick={toggleEdit}>
              Edit
              <i className="fa fa-pen-to-square"></i>
            </button>
          )}
        </div>
      </div>

      <div className="row g-5 m-2">
        <div className="col-md-6">
          <img src={imageSrc} className="card-img-top rounded-edge" alt="..." />
          <div className="row g-5 m-2 d-flex justify-content-center">
            {isEditing && (
              <>
                <input
                  type="file"
                  id="fileInput"
                  className="hidden-input"
                  accept="image/*"
                  onChange={handleFileChange}
                />
                <label htmlFor="fileInput" className="custom-file-input">
                  Choose a File
                </label>
              </>
            )}
          </div>
        </div>

        <div className="col-md-6">
          <div className="container-styling">
            <div className="title">
              {isEditing ? (
                <AutoSizeTextArea
                  content={post.title}
                  onChange={(value) => setPost({ ...post, title: value })}
                />
              ) : (
                post.title
              )}
            </div>
            <div className="summary">
              {isEditing ? (
                <AutoSizeTextArea
                  content={post.description}
                  onChange={(value) => setPost({ ...post, description: value })}
                />
              ) : (
                post.description
              )}
            </div>
            <span className="pill">
              {post.tags.map((tag: string, index: number) => (
                <span className="pill-tag" key={index}>
                  {tag}
                </span>
              ))}
            </span>
            <div className="subtitle">About</div>
            <div className="details">
              {isEditing ? (
                <AutoSizeTextArea
                  content={post.extendedDescription}
                  onChange={(value) =>
                    setPost({ ...post, extendedDescription: value })
                  }
                />
              ) : (
                post.extendedDescription
              )}
            </div>
            <div className="subtitle">Date</div>
            <div className="details">
              {isEditing ? (
                <AutoSizeTextArea
                  content={post.date.toDateString()}
                  onChange={(value) =>
                    setPost({ ...post, date: new Date(value) })
                  }
                />
              ) : (
                post.date.toDateString()
              )}
            </div>
            <div className="subtitle">Location</div>
            <div className="details">
              {isEditing ? (
                <AutoSizeTextArea
                  content={post.location}
                  onChange={(value) => setPost({ ...post, location: value })}
                />
              ) : (
                post.location
              )}
            </div>
            <div className="subtitle">Club</div>
            <div className="details">
              {isEditing ? (
                <AutoSizeTextArea
                  content={post.club}
                  onChange={(value) => setPost({ ...post, club: value })}
                />
              ) : (
                post.club
              )}
            </div>
            <div className="row g-5 m-2 d-flex justify-content-center">
              <button className="favourite-button ">Favourite?</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostDetailsPage;
