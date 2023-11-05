import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostDetailsPage.css";
const postImage = require("../assets/post1.jpeg");

const PostDetailsPage: React.FC = () => {
  const { postId } = useParams();
  const postIdNumber = postId ? parseInt(postId) : 0;

  // Define a state to store post data
  const [post, setPost] = useState<any>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [imageSrc, setImageSrc] = useState(postImage);

  useEffect(() => {
    // Fetch the post data for the specified postId
    // You can fetch data from an API or your data source here

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
      // Define mock data for other postIds
    };

    // Check if the postId is valid and exists in your data
    if (!isNaN(postIdNumber) && postIdNumber in mockData) {
      setPost(mockData[0] as any);
    } else {
      // Handle the case where the postId is invalid (e.g., show an error message)
      console.error("Invalid postId:", postId);
    }
  }, [postId]);

  // If the post data is not yet available, you can display a loading message
  if (!post) {
    return <div>Loading...</div>;
  }

  const toggleEdit = () => {
    setIsEditing(!isEditing);
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
    <div className="container bg-white rounded-5 p-5 mt-2 mb-2">
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
          <button className="edit-button" onClick={toggleEdit}>
            {isEditing ? (
              <>
                Save
                <i className="fa fa-floppy-disk"></i>
              </>
            ) : (
              <>
                Edit
                <i className="fa fa-pen-to-square"></i>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="row g-5 m-2">
        <div className="col-md-6">
          <img src={imageSrc} className="card-img-top rounded-edge" alt="..." />
          <div className="row g-5 m-2 d-flex justify-content-center">
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
          </div>
        </div>

        <div className="col-md-6">
          <div className="container-styling">
            <div className="title">
              {isEditing ? (
                <input
                  type="text"
                  value={post.title}
                  onChange={(e) => setPost({ ...post, title: e.target.value })}
                />
              ) : (
                post.title
              )}
            </div>
            <div className="summary">
              {isEditing ? (
                <input
                  type="text"
                  value={post.description}
                  onChange={(e) =>
                    setPost({ ...post, description: e.target.value })
                  }
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
                <input
                  type="text"
                  value={post.extendedDescription}
                  onChange={(e) =>
                    setPost({ ...post, extendedDescription: e.target.value })
                  }
                />
              ) : (
                post.extendedDescription
              )}
            </div>
            <div className="subtitle">Date</div>
            <div className="details">
              {isEditing ? (
                <input
                  type="text"
                  value={post.date.toDateString()}
                  onChange={(e) => setPost({ ...post, date: e.target.value })}
                />
              ) : (
                post.date.toDateString()
              )}
            </div>
            <div className="subtitle">Location</div>
            <div className="details">
              {isEditing ? (
                <input
                  type="text"
                  value={post.location}
                  onChange={(e) =>
                    setPost({ ...post, location: e.target.value })
                  }
                />
              ) : (
                post.location
              )}
            </div>
            <div className="subtitle">Club</div>
            <div className="details">
              {isEditing ? (
                <input
                  type="text"
                  value={post.club}
                  onChange={(e) => setPost({ ...post, club: e.target.value })}
                />
              ) : (
                post.club
              )}
            </div>
            <div className="row g-5 m-2">
              <button className="favourite-button d-flex justify-content-center">
                Favourite?
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostDetailsPage;
