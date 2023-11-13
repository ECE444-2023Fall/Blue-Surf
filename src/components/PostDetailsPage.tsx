import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import moment from "moment-timezone";
import { faPlus, faXmark } from "@fortawesome/free-solid-svg-icons";
import { Dropdown } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostDetailsPage.css";
import AutoSizeTextArea from "./AutoSizeTextArea";
import DeletePopUp from "./DeletePopUp";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import API_URL from "../config";
import { ToastContainer, toast } from 'react-toastify';
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
  const navigate = useNavigate();
  const [post, setPost] = useState<Post>();
  const [editedPost, setEditedPost] = useState<Post>();
  const [isEditing, setIsEditing] = useState(false);
  const [imageSrc, setImageSrc] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [isLiked, setIsLiked] = useState<boolean>(false);
  const [dateMessage, setDateMessage] = useState<string>("");
  const [showDeletePopUp, setShowDeletePopUp] = useState(false);

  const isAuthor = user && post && parseInt(user.userId) === post.author_id;

  const [alertMessage, setAlertMessage] = useState({
    titleAlert: "",
    summaryAlert: "",
  });
  const [blankMessage, setBlankMessage] = useState({
    blankErrorMessage: "",
  });

  const checkIfLiked = (data: any, eventId: string) => {
    setIsLiked(
      data && data.some((event: any) => event.id === parseInt(eventId))
    );
  };

  const getTagNames = async (): Promise<any[] | null> => {
    try {
      const response = await fetch(`${API_URL}/api/get-all-tags`);
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error("Failed to fetch all tag names");
      }
    } catch (error) {
      console.error("Tag Error:", error);
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
        throw new Error("Failed to fetch favourited events");
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
        const response = await fetch(`${API_URL}/api/${postId}`);
        if (!response || !response.ok) {
          throw new Error("Cannot fetch post.");
        }
        const data = await response.json();
        setPost(data);
        setEditedPost(data);

        const postImageResponse = await fetch(`${API_URL}/api/${postId}/image`);
        if (!postImageResponse || !postImageResponse.ok) {
          throw new Error("Cannot fetch post image.");
        }

        // Get the image data as a Blob
        const imageBlob = await postImageResponse.blob();

        // Create a File object with the image data
        const imageFile = new File([imageBlob], `image_${postId}.png`, {
          type: "image/png", // Adjust the type based on your image format
        });

        // Set the image file in state
        setImageFile(imageFile);
      } catch (error) {
        console.error("Error fetching post:", error);
        navigate(-1);
        toast.error(`Post does not exist.`, {
          position: toast.POSITION.TOP_CENTER,
        });
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
    const formattedStartDate = moment(editedPost.start_time)
      .tz("America/New_York") // Replace 'desiredTimeZone' with the target time zone
      .format("YYYY-MM-DD HH:mm:ss");

    const formattedEndDate = moment(editedPost.end_time)
      .tz("America/New_York")
      .format("YYYY-MM-DD HH:mm:ss");

    if (editedPost.end_time < editedPost.start_time) {
      setDateMessage("Pick a valid end date");
      return;
    } else {
      setDateMessage("");
    }

    if (editedPost.description.length > 180 && editedPost.title.length > 50) {
      setAlertMessage({
        titleAlert: "Title cannot exceed 50 characters",
        summaryAlert: "Summary cannot exceed 180 characters",
      });
      return;
    }
    if (editedPost.title.length > 50) {
      setAlertMessage({
        titleAlert: "Title cannot exceed 50 characters",
        summaryAlert: "",
      });
      return;
    }
    if (editedPost.description.length > 180) {
      setAlertMessage({
        titleAlert: "",
        summaryAlert: "Summary cannot exceed 180 characters",
      });
      return;
    }

    if (!editedPost.location && !editedPost.title) {
      setBlankMessage({
        blankErrorMessage: "Title and Location are required fields.",
      });
      return;
    }

    if (!editedPost.title) {
      setBlankMessage({
        blankErrorMessage: "Title is a required field.",
      });
      return;
    }

    if (!editedPost.location) {
      setBlankMessage({
        blankErrorMessage: "Location is a required field.",
      });
      return;
    }

    try {
      // Send a POST request to the backend to update the post
      const response = await fetch(`${API_URL}/api/update-post/${postId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(editedPost),
      });

      if (response.ok) {
        setIsEditing(false);
        setPost({ ...editedPost });
        setAlertMessage({ titleAlert: "", summaryAlert: "" });
        setBlankMessage({ blankErrorMessage: "" });
        toast.success(`Edited ${editedPost.title}.`, {
          position: toast.POSITION.TOP_CENTER,
        });
      } else {
        throw new Error("Failed to update post.");
      }
    } catch (error) {
      console.error("Update Post Error:", error);
    }

    // Append the image data to the FormData
    const formData = new FormData();
    formData.append("image", imageFile!);


    try {
      // Send a POST request to the backend to update the post
      const response = await fetch(
        `${API_URL}/api/update-post-image/${postId}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        setIsEditing(false);
        setPost({ ...editedPost });
        setAlertMessage({ titleAlert: "", summaryAlert: "" });
        setBlankMessage({ blankErrorMessage: "" });
      } else {
        throw new Error("Failed to update post.");
      }
    } catch (error) {
      console.error("Update Image Error:", error);
    }
  };

  const handleCancel = () => {
    setEditedPost({ ...post });
    setIsEditing(false);
    setAlertMessage({ titleAlert: "", summaryAlert: "" });
    setBlankMessage({ blankErrorMessage: "" });
    setDateMessage("");
  };

  const handleDelete = async (confirmed: boolean) => {
    if (confirmed) {
      try {
        const response = await fetch(`${API_URL}/api/delete-post/${postId}`, {
          method: "POST",
          headers: {
            Authorization: "Bearer " + token,
          },
        });

        if (response.ok) {
          const data = await response.json();
          data.access_token && setAuth(data.access_token, user);
          navigate(-1);
          toast.success(`Deleted ${editedPost.title}.`, {
            position: toast.POSITION.TOP_CENTER,
          });
        } else {
          const errorMessage = await response.text();
          throw new Error(errorMessage || "Delete request failed");
        }
      } catch (error) {
        console.error("Delete Post Error:", error);
      }
    }
    setShowDeletePopUp(false);
  };

  const handleDeleteButtonClick = () => {
    setShowDeletePopUp(true);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];

    if (selectedFile) {
      setImageFile(selectedFile);

      const reader = new FileReader();
      reader.onload = (e) => {
        const newImageSrc = e.target?.result as string;
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
    setEditedPost({
      ...editedPost,
      tags: [...editedPost.tags, selectedTag],
    });
  };

  const handleTagRemoval = (selectedTag: string) => {
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
        editedPost.like_count += !isLiked ? 1 : -1
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
      {showDeletePopUp && (
        <DeletePopUp postTitle={post.title} handleDelete={handleDelete} />
      )}
      <div className="container background-colour rounded-5 p-5 mt-2 mb-2">
        <div className="row m-2 auto d-flex justify-content-center align-items-center">
          <a
            className="navbar-brand back-nav justify-content-left"
            href="javascript:history.back()"
          >
            <img
              src="https://cdn-icons-png.flaticon.com/512/271/271220.png"
              width="15"
              height="15"
              className="d-inline-block align-items-center"
              alt=""
            />
            <span className="back-text">Back</span>
          </a>
          <div className="col-md-6">
            {blankMessage.blankErrorMessage && (
              <div className="alert">{blankMessage.blankErrorMessage}</div>
            )}
          </div>

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
              <>
                {isAuthor && (
                  <>
                    <button className="edit-button" onClick={toggleEdit}>
                      Edit
                    </button>
                    <button
                      className="trash-button-details-page"
                      onClick={handleDeleteButtonClick}
                    >
                      <i className="fa fa-trash-o trash-icon-custom-size-details-page" />
                    </button>
                  </>
                )}
              </>
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
              {/* TITLE */}
              <div className="title">
                {isEditing ? (
                  <AutoSizeTextArea
                    content={editedPost.title}
                    onChange={(value) =>
                      setEditedPost({ ...editedPost, title: value })
                    }
                    placeholderWord="[enter title here]"
                  />
                ) : (
                  editedPost.title
                )}
              </div>
              {alertMessage.titleAlert && (
                <div className="alert">{alertMessage.titleAlert}</div>
              )}

              {/* SUMMARY */}
              <div className="summary">
                {isEditing ? (
                  <AutoSizeTextArea
                    content={editedPost.description}
                    onChange={(value) =>
                      setEditedPost({ ...editedPost, description: value })
                    }
                    placeholderWord="[enter description here]"
                  />
                ) : (
                  editedPost.description
                )}
              </div>
              {alertMessage.summaryAlert && (
                <div className="alert">{alertMessage.summaryAlert}</div>
              )}

              {/* TAGS */}
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

              {/* EXTENDED DESCRIPTION */}
              <div className="subtitle">About</div>
              <div className="details">
                {isEditing ? (
                  <AutoSizeTextArea
                    content={editedPost.extended_description}
                    onChange={(value) =>
                      setEditedPost({
                        ...editedPost,
                        extended_description: value,
                      })
                    }
                    placeholderWord="[enter extended description here]"
                  />
                ) : (
                  editedPost.extended_description
                )}
              </div>
              <div className="subtitle"> Start Date </div>
              <div className="details">
                {isEditing ? (
                  <input
                    type="datetime-local"
                    value={
                      editedPost.start_time instanceof Date
                        ? new Date(
                            editedPost.start_time.getTime() -
                              editedPost.start_time.getTimezoneOffset() * 60000
                          )
                            .toISOString()
                            .slice(0, -8)
                        : ""
                    }
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                      const newStartTime = new Date(e.target.value);
                      if (!isNaN(newStartTime.getTime())) {
                        setEditedPost({
                          ...editedPost,
                          start_time: newStartTime,
                        });
                      }
                    }}
                  />
                ) : (
                  editedPost.start_time.toLocaleString()
                )}
              </div>
              <div className="subtitle"> End Date </div>
              <div className="details">
                {isEditing ? (
                  <input
                    type="datetime-local"
                    value={
                      editedPost.end_time instanceof Date
                        ? new Date(
                            editedPost.end_time.getTime() -
                              editedPost.end_time.getTimezoneOffset() * 60000
                          )
                            .toISOString()
                            .slice(0, -8)
                        : ""
                    }
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                      const newEndTime = new Date(e.target.value);
                      if (!isNaN(newEndTime.getTime())) {
                        setEditedPost({
                          ...editedPost,
                          end_time: newEndTime,
                        });
                      }
                    }}
                  />
                ) : (
                  editedPost.end_time.toLocaleString()
                )}
              </div>
              {dateMessage && <div className="error-date">{dateMessage}</div>}
              {/* LOCATION */}
              <div className="subtitle">Location</div>
              <div className="details">
                {isEditing ? (
                  <AutoSizeTextArea
                    content={editedPost.location}
                    onChange={(value) =>
                      setEditedPost({ ...editedPost, location: value })
                    }
                    placeholderWord="[enter location here]"
                  />
                ) : (
                  editedPost.location
                )}
              </div>

              {/* CLUB */}
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
                        placeholderWord="[enter club name here if applicable]"
                      />
                    ) : (
                      editedPost.club
                    )}
                  </div>
                </div>
              )}

              {/* FAVOURITE */}
              <div className="row g-5 m-2 d-flex justify-content-center">
                {token && token !== "" && token !== undefined && (
                  <button
                    className={`like-button-details ${
                      isLiked ? "liked-details" : ""
                    } d-flex`}
                    onClick={toggleLike}
                    data-testid="like-button"
                  >
                    <i className={`fa fa-heart${isLiked ? "" : "-o"}`} />
                    {isAuthor && (<div className="like-count">{editedPost.like_count}</div>)}
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
