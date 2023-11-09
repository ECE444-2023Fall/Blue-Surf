import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostDetailsPage.css";
import "../styles/PostCreatePage.css";
import AutoSizeTextArea from "./AutoSizeTextArea";
const imageTemplate = require("../assets/post-template.jpg");
//<a href="https://www.freepik.com/free-vector/hand-painted-watercolor-background-with-frame_4366269.htm#query=frame%20blue&position=21&from_view=search&track=ais">Image by denamorado</a> on Freepik

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

const PostCreatePage: React.FC<PostDetailsProps> = ({
  token,
  user,
  setAuth,
}) => {
  const navigate = useNavigate();

  const [editedPost, setEditedPost] = useState<Post>({
    title: "Catchy Event Name Here 🎉",
    start_time: new Date(),
    location: "Where's the action happening? 📍",
    description: "Describe the excitement in a few words! 🌟",
    extended_description: "Dive deeper into your event/club here! 🌊",
    tags: [],
    id: 0,
    author_id: parseInt(user.userId),
    is_published: true,
    end_time: new Date(),
    like_count: 0,
    club: "",
  });
  const [imageSrc, setImageSrc] = useState(imageTemplate);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const handleSave = async () => {
    try {
      if (!editedPost.title && !editedPost.location) {
        setErrorMessage("Title and Location are required fields.");
        return;
      } else if (!editedPost.title) {
        setErrorMessage("Title is a required field.");
        return;
      } else if (!editedPost.location) {
        setErrorMessage("Location is a required field.");
        return;
      } else {
        setErrorMessage("");
      }

      const formattedStartDate = editedPost.start_time
        .toISOString()
        .slice(0, 19)
        .replace("T", " ");
      const formattedEndDate = editedPost.end_time
        .toISOString()
        .slice(0, 19)
        .replace("T", " ");

      const postData = {
        ...editedPost,
        start_time: formattedStartDate,
        end_time: formattedEndDate,
      };

      const response = await fetch(`/api/create-post`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
      });

      if (response.ok) {
        navigate("/dashboard");
      } else {
        const data = await response.json();
        throw new Error(data["error message"]);
      }
    } catch (error) {
      console.error("Create Post Error:", error);
    }
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
    <div className="post-create-wrapper">
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
            <>
              {/* Display the error message */}
              {errorMessage && (
                <div className="error-message">{errorMessage}</div>
              )}
              <button className="edit-button" onClick={handleSave}>
                Post
              </button>
            </>
          </div>
        </div>

        <div className="row g-5 m-2">
          <div className="col-md-6">
            <img
              src={imageSrc}
              className="card-img-top rounded-edge"
              alt="..."
            />
            <div className="row g-5 m-2 d-flex justify-content-center">
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
            </div>
          </div>

          <div className="col-md-6">
            <div className="container-styling">
              <div className="title">
                <AutoSizeTextArea
                  content={editedPost.title}
                  onChange={(value) =>
                    setEditedPost({ ...editedPost, title: value })
                  }
                  placeholderWord="[enter title here]"
                />
              </div>
              <div className="summary">
                <AutoSizeTextArea
                  content={editedPost.description}
                  onChange={(value) =>
                    setEditedPost({ ...editedPost, description: value })
                  }
                  placeholderWord="[enter description here]"
                />
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
                {/* TODO: replace with extendedDescription field */}
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
              </div>
              <div className="subtitle">Date</div>
              <div className="details">
                <AutoSizeTextArea
                  content={editedPost.start_time.toLocaleString()}
                  onChange={(value) =>
                    setEditedPost({
                      ...editedPost,
                      start_time: new Date(value),
                    })
                  }
                />
              </div>
              <div className="subtitle">Location</div>
              <div className="details">
                <AutoSizeTextArea
                  content={editedPost.location}
                  onChange={(value) =>
                    setEditedPost({ ...editedPost, location: value })
                  }
                  placeholderWord="[enter location here]"
                />
              </div>
              <div>
                <div className="subtitle">Club</div>
                <div className="details">
                  <AutoSizeTextArea
                    content={editedPost.club || ""}
                    onChange={(value) =>
                      setEditedPost({ ...editedPost, club: value })
                    }
                    placeholderWord="[enter club name here if applicable]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostCreatePage;
