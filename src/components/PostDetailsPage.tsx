import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { faPlus, faXmark } from "@fortawesome/free-solid-svg-icons";
import { Dropdown } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostDetailsPage.css";
import AutoSizeTextArea from "./AutoSizeTextArea";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import API_URL from '../config';
const defaultImage = require("../assets/image_placeholder.jpeg");

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
  club?: string;
  image: string;
}

interface User {
  userId: string;
  username: string;
}

interface PostDetailsProps {
  token: string;
  user: User;
  setAuth: (token: string | null, user: User | null) => void;
}

const PostDetailsPage: React.FC<PostDetailsProps> = ({
  token,
  user,
  setAuth,
}) => {
  const { postId } = useParams();

  const [post, setPost] = useState<Post>();
  const [editedPost, setEditedPost] = useState<Post>();
  const [isEditing, setIsEditing] = useState(false);
  const [imageSrc, setImageSrc] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [isLiked, setIsLiked] = useState<boolean>(false);

  const checkIfLiked = (data: any, eventId: string) => {
    setIsLiked(data && data.some((event: any) => event.id === parseInt(eventId)));
  };

  const getTagNames = async (): Promise<any[] | null> => {
    const response = await fetch(`${API_URL}/api/get-all-tags`);
    if (response.ok) {
      const data = await response.json();
      console.log(data);
      return data;
    } else {
      console.error("Failed to fetch all tag names");
      return null;
    }
  };

  const fetchFavouritedEvents = async () => {
    try {
      const response = await fetch(`${API_URL}/api/favourites`, {
        headers: {
          Authorization: "Bearer " + token,
        },
      });
      if (response.ok) {
        const data = await response.json();
        data.access_token && setAuth(data.access_token, user);
        return data;
      } else {
        console.error("Failed to fetch favourited events");
      }
    } catch (error) {
      console.error(
        "An error occurred while fetching favourited events",
        error
      );
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      const tags = await getTagNames();
      if (tags) {
        setTags(tags);
      }
    };

    fetchData();
  }, []);

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

        const postImageResponse = await fetch(`/api/${postId}/image`);
        if (!postImageResponse || !postImageResponse.ok) {
          throw new Error("Cannot fetch post image.");
        }

        // Get the image data as a Blob
        const imageBlob = await postImageResponse.blob();

        console.log("blob", imageBlob);

        // Create a File object with the image data
        const imageFile = new File([imageBlob], `image_${postId}.png`, {
          type: "image/png", // Adjust the type based on your image format
        });

        console.log("file", imageFile);

        // Set the image file in state
        setImageFile(imageFile);
      } catch (error) {
        console.error("Error fetching post:", error);
      }
    };

    fetchData();
  }, [postId]);

  useEffect(() => {
    if (token && token !== "" && token !== undefined) {
      const fetchData = async () => {
        const data = await fetchFavouritedEvents();
        postId && checkIfLiked(data, postId);
      };

      fetchData();
    }
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
    console.log(editedPost);
    try {
      // Send a POST request to the backend to update the post
      const response = await fetch(`/api/update-post/${postId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(editedPost),
      });

      console.log("content", JSON.stringify(editedPost));

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

    // Append the image data to the FormData
    const formData = new FormData();
    formData.append("image", imageFile!);

    console.log("FormData:");

    for (const [key, value] of formData.entries()) {
      console.log(key, value);
    }

    try {
      // Send a POST request to the backend to update the post
      const response = await fetch(`/api/update-post-image/${postId}`, {
        method: "POST",
        body: formData,
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

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];

    if (selectedFile) {
      setImageFile(selectedFile);

      const reader = new FileReader();
      reader.onload = (e) => {
        const newImageSrc = e.target?.result as string;
        console.log("newImageSrc", newImageSrc);
        setImageSrc(newImageSrc);
      };

      reader.readAsDataURL(selectedFile);
    }
  };

  const calculatePillsWidth = () => {
    const pillTags = document.querySelectorAll(".pill-tag");
    let totalWidth = 0;
    pillTags.forEach((pillTag) => {
      totalWidth += pillTag.clientWidth;
    });
    return totalWidth;
  };

  const handleTagAddition = (selectedTag: string) => {
    console.log("in addition");
    setEditedPost({
      ...editedPost,
      tags: [...editedPost.tags, selectedTag],
    });
  };

  const handleTagRemoval = (selectedTag: string) => {
    console.log("in removal");
    setEditedPost({
      ...editedPost,
      tags: editedPost.tags.filter((tag) => tag !== selectedTag),
    });
  };

  const toggleLike = async () => {
    try {
      let route = `${API_URL}/api/like`;
      if (isLiked) {
        route = `${API_URL}/api/unlike`;
      }
      const response = await fetch(`${route}/${postId}`, {
        method: "POST",
        headers: {
          Authorization: "Bearer " + token,
        },
      });

      if (response.ok) {
        setIsLiked(!isLiked);
      } else {
        const data = await response.json();
        throw new Error(data["error message"]);
      }
    } catch (error) {
      console.error("Like Error:", error);
    }
  };

  return (
    <div className="post-details-wrapper">
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
            <img
              src={imageFile ? URL.createObjectURL(imageFile) : defaultImage}
              className="card-img-top rounded-edge"
              alt="..."
            />
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
              <div className="row align-items-center">
                <div
                  className="col d-flex"
                  style={{ marginRight: calculatePillsWidth() }}
                >
                  <div className="selected-tags-container">
                    {editedPost.tags.length > 0 &&
                      editedPost.tags.map((tag: string, index: number) => (
                        <span className="pill" key={index}>
                          <span className="pill-tag">
                            {tag}
                            {isEditing && (
                              <button
                                className="remove-tag-button"
                                onClick={() => handleTagRemoval(tag)}
                              >
                                <FontAwesomeIcon icon={faXmark} />
                              </button>
                            )}
                          </span>
                        </span>
                      ))}
                    {isEditing && (
                      <Dropdown>
                        <Dropdown.Toggle
                          className="plus-icon"
                          variant="secondary"
                        >
                          <FontAwesomeIcon icon={faPlus} />
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                          {tags.map(
                            (tag: string) =>
                              // Only show tags not already in the post
                              !editedPost.tags.includes(tag) && (
                                <Dropdown.Item
                                  key={tag}
                                  onClick={() => handleTagAddition(tag)}
                                  className="dropdown-item-tag"
                                >
                                  <span className="pill">
                                    <span className="pill-tag"></span>
                                    {tag}
                                  </span>
                                </Dropdown.Item>
                              )
                          )}
                        </Dropdown.Menu>
                      </Dropdown>
                    )}
                  </div>
                </div>
              </div>
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
                {token && token !== "" && token !== undefined && (
                  <button
                    className={`like-button-details ${
                      isLiked ? "liked-details" : ""
                    }`}
                    onClick={toggleLike}
                    data-testid="like-button"
                  >
                    <i className={`fa fa-heart${isLiked ? "" : "-o"}`} />
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostDetailsPage;
