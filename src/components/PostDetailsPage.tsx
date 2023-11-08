import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostDetailsPage.css";
import AutoSizeTextArea from "./AutoSizeTextArea";
const postImage = require("../assets/post1.jpeg");

const EXTENTDED_DESCRIPTION =
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
interface Post {
  title: string;
  start_time: Date;
  location: string;
  description: string;
  extended_description: string;
  tags: string[];
  id: number;
  author_id: number;
  is_published: boolean;
  end_time: Date;
  like_count: number;
  image?: string;
  club?: string;
}

const PostDetailsPage: React.FC = () => {
  const { postId } = useParams();

  const [post, setPost] = useState<Post>();
  const [editedPost, setEditedPost] = useState<Post>();
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
        setEditedPost(data);
      } catch (error) {
        console.error("Error fetching suggestions:", error);
      }
    };

    fetchData();
  }, [postId]);

  // Post data is not yet available
  if (!post || !editedPost) {
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
      // Check if a new image was selected
      if (imageSrc) {
        console.log("here");
        const imageFormData = new FormData();
        imageFormData.append("image", imageSrc);

        // Upload the image using the /api/upload-image endpoint
        const imageUploadResponse = await fetch("/api/upload-image", {
          method: "POST",
          body: imageFormData,
        });

        if (!imageUploadResponse.ok) {
          console.error("Failed to upload the image.");
          return;
        }

        // Get the image path or filename from the imageUploadResponse if needed
        const imageInfo = await imageUploadResponse.json();
        const uploadedImageSrc = imageInfo.imagePath; // Replace with the actual field name

        // Update the edited post with the uploaded image source
        const postToUpdate = { ...editedPost, image: uploadedImageSrc };

        // Now, update the post using the /api/update-post endpoint with the modified post data
        const postUpdateResponse = await fetch(`/api/update-post/${postId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(postToUpdate),
        });

        if (postUpdateResponse.ok) {
          console.log("Post updated successfully!");
          setIsEditing(false);
          setPost({ ...postToUpdate });
        } else {
          console.error("Failed to update post.");
        }
      } else {
        // No new image selected, update the post data directly
        const postUpdateResponse = await fetch(`/api/update-post/${postId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(editedPost),
        });

        if (postUpdateResponse.ok) {
          console.log("Post updated successfully!");
          setIsEditing(false);
          setPost({ ...editedPost });
        } else {
          console.error("Failed to update post.");
        }
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
        console.log("image src", newImageSrc);
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
                  content={editedPost.extended_description}
                  onChange={(value) =>
                    setEditedPost({
                      ...editedPost,
                      extended_description: value,
                    })
                  }
                />
              ) : (
                editedPost.extended_description
              )}
            </div>
            <div className="subtitle">Date</div>
            <div className="details">
              {isEditing ? (
                <AutoSizeTextArea
                  content={editedPost.start_time.toLocaleString()}
                  onChange={(value) =>
                    setEditedPost({
                      ...editedPost,
                      start_time: new Date(value),
                    })
                  }
                />
              ) : (
                editedPost.start_time.toLocaleString()
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
            {editedPost.club && (
              <div>
                <div className="subtitle">Club</div>
                <div className="details">
                  {isEditing ? (
                    <AutoSizeTextArea
                      content={editedPost.club}
                      onChange={(value) =>
                        setEditedPost({ ...editedPost, club: value })
                      }
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
