import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostDetailsPage.css";
import AutoSizeTextArea from "./AutoSizeTextArea";
const postImage = require("../assets/post1.jpeg");

interface Post {
  title: string;
  start_time: Date;
  location: string;
  description: string;
  tags: string[];
  id: number;
  author_id: number;
  is_published: boolean;
  end_time: Date;
  like_count: number;
  club?: string;
}

const PostDetailsPage: React.FC = () => {
  const { postId } = useParams();

  const [post, setPost] = useState<any>(null);
  const [editedPost, setEditedPost] = useState<any>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [imageSrc, setImageSrc] = useState(postImage);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/api/${postId}`);
        if (!response || !response.ok) {
          throw new Error("Cannot fetch post.");
        }
        const data = await response.json();
        setPost(data);
      } catch (error) {
        console.error("Error fetching suggestions:", error);
      }
    };

    fetchData();
  }, [postId]);

  // Post data is not yet available
  if (!post) {
    return <div>Loading...</div>;
  }

  const toggleEdit = () => {
    if (isEditing) {
      // If you're exiting edit mode, revert changes
      setEditedPost({ ...post });
    }
    setIsEditing(!isEditing);
  };

  const handleSave = async () => {
    try {
      // Send a POST request to the backend to update the post
      const response = await fetch(`/api/update-post/${postId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(editedPost),
      });

      if (response.ok) {
        console.log("Post updated successfully!");
        setIsEditing(false);
        setPost({ ...editedPost });
      } else {
        console.error("Failed to update post.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleCancel = () => {
    setEditedPost({ ...post });
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
              </button>
            </>
          ) : (
            <button className="edit-button" onClick={toggleEdit}>
              Edit
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
                  content={editedPost.title}
                  onChange={(value) =>
                    setEditedPost({ ...editedPost, title: value })
                  }
                />
              ) : (
                editedPost.title
              )}
            </div>
            <div className="summary">
              {isEditing ? (
                <AutoSizeTextArea
                  content={editedPost.description}
                  onChange={(value) =>
                    setEditedPost({ ...editedPost, description: value })
                  }
                />
              ) : (
                editedPost.description
              )}
            </div>
            {/* <span className="pill">
              {post.tags.map((tag: string, index: number) => (
                <span className="pill-tag" key={index}>
                  {tag}
                </span>
              ))}
            </span> */}
            <div className="subtitle">About</div>
            <div className="details">
              {isEditing ? (
                // TODO: replace with extendedDescription field
                <AutoSizeTextArea
                  content={editedPost.extendedDescription}
                  onChange={(value) =>
                    setEditedPost({ ...editedPost, extendedDescription: value })
                  }
                />
              ) : (
                editedPost.extendedDescription
              )}
            </div>
            <div className="subtitle">Date</div>
            <div className="details">
              {isEditing ? (
                <AutoSizeTextArea
                  content={editedPost.date.toDateString()}
                  onChange={(value) =>
                    setEditedPost({ ...editedPost, date: new Date(value) })
                  }
                />
              ) : (
                editedPost.date.toDateString()
              )}
            </div>
            <div className="subtitle">Location</div>
            <div className="details">
              {isEditing ? (
                <AutoSizeTextArea
                  content={editedPost.location}
                  onChange={(value) =>
                    setEditedPost({ ...editedPost, location: value })
                  }
                />
              ) : (
                editedPost.location
              )}
            </div>
            {post.club && (
              <div>
                <div className="subtitle">Club</div>
                <div className="details">
                  {isEditing ? (
                    <AutoSizeTextArea
                      content={editedPost.club}
                      onChange={(value) => setEditedPost({ ...editedPost, club: value })}
                    />
                  ) : (
                    editedPost.club
                  )}
                </div>
              </div>
            )}
            <div className="row g-5 m-2 d-flex justify-content-center">
              <button className="favourite-button">Favourite?</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostDetailsPage;
