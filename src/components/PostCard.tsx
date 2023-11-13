import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostCard.css";
import API_URL from '../config';
const defaultImage = require("../assets/image_placeholder.jpeg");


interface User {
  userId: string;
  username: string;
}

interface PostCardProps {
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
  token: string;
  user: User;
  setAuth: (token: string | null, user: User | null) => void;
  showDeletePopUp: (postId: number, postTitle: string) => void;
}

const PostCard: React.FC<PostCardProps> = (PostCardProps: any) => {
  const postId = PostCardProps.id;

  const [isLiked, setIsLiked] = React.useState(false);
  const [imageFile, setImageFile] = React.useState<File | null>(null);

  const fetchImage = async () => {
    try {
      const postImageResponse = await fetch(`${API_URL}/api/${postId}/image`);
      if (!postImageResponse || !postImageResponse.ok) {
        throw new Error("Cannot fetch post image.");
      }

      // Get the image data as a Blob
      const imageBlob = await postImageResponse.blob();

      // console.log("blob", imageBlob);

      // Create a File object with the image data
      const newImageFile = new File([imageBlob], `image_${postId}.png`, {
        type: "image/png", // Adjust the type based on your image format
      });

      // console.log("file", newImageFile);

      // Set the image file in state
      setImageFile(newImageFile);
    } catch (error) {
      console.error("Error fetching postcard image:", error);
    }
  };

  useEffect(() => {
    fetchImage();
  }, []);

  const checkIfLiked = (data: any, eventId: number) => {
    setIsLiked(data && data.some((event: any) => event.id === eventId));
  };

  const isAuthor =
    PostCardProps.user &&
    parseInt(PostCardProps.user.userId) === PostCardProps.author_id;

  const toggleLike = async () => {
    try {
      let route = `${API_URL}/api/like`;
      if (isLiked) {
        route = `${API_URL}/api/unlike`;
      }
      const response = await fetch(`${route}/${PostCardProps.id}`, {
        method: "POST",
        headers: {
          Authorization: "Bearer " + PostCardProps.token,
        },
      });

      const data = await response.json();
      if (response.ok) {
        data.access_token &&
          PostCardProps.setAuth(data.access_token, PostCardProps.user);
        setIsLiked(!isLiked);
      } else {
        throw new Error(data["error message"]);
      }
    } catch (error) {
      console.error("Like Error:", error);
    }
  };

  const fetchFavouritedEvents = async () => {
    try {
      const response = await fetch(`${API_URL}/api/favourites`, {
        headers: {
          Authorization: "Bearer " + PostCardProps.token,
        },
      });
      if (response.ok) {
        const data = await response.json();
        data.access_token &&
          PostCardProps.setAuth(data.access_token, PostCardProps.user);
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

  const handleDeleteButtonClick = () => {
    PostCardProps.showDeletePopUp(PostCardProps.id, PostCardProps.title);
  };

  React.useEffect(() => {
    if (
      PostCardProps.token &&
      PostCardProps.token !== "" &&
      PostCardProps.token !== undefined
    ) {
      const fetchData = async () => {
        const data = await fetchFavouritedEvents();
        checkIfLiked(data, PostCardProps.id);
      };

      fetchData();
    }
  }, [PostCardProps.id]);

  return (
    <div className="col" data-testid="post-card">
      <Link to={`/post/${PostCardProps.id}`} className="text-decoration-none">
        <div className="card">
          <img
            src={imageFile ? URL.createObjectURL(imageFile) : defaultImage}
            className="card-img-top rounded-top-34"
            alt="..."
          />
          <div className="card-body">
            <div className="d-flex justify-content-center">
              <span
                className="h4 card-title text-center"
                data-testid="post-title"
              >
                {PostCardProps.title}
              </span>
            </div>
            <p className="p text-center" data-testid="post-date-location">
              {PostCardProps.start_time} | {PostCardProps.location}
            </p>
            <p className="card-text text-left" data-testid="post-description">
              {PostCardProps.description}
            </p>
            <div className="row">
              <div className="col">
                <div className="tags-container">
                  {PostCardProps.tags && PostCardProps.tags.length > 0 && (
                    <>
                      {PostCardProps.tags.map((tag: string, index: number) => (
                        <span
                          className="pill"
                          data-testid="post-tags"
                          key={tag}
                        >
                          <span className="pill-tag">{tag}</span>
                        </span>
                      ))}
                    </>
                  )}
                </div>
              </div>
              <div className="col-auto">
                <div onClick={(e) => e.preventDefault()}>
                  {PostCardProps.token &&
                    PostCardProps.token !== "" &&
                    PostCardProps.token !== undefined && (
                      <button
                        className={`like-button ${isLiked ? "liked" : ""}`}
                        onClick={toggleLike}
                        data-testid="like-button"
                      >
                        <i className={`fa fa-heart${isLiked ? "" : "-o"}`} />
                      </button>
                    )}
                  {isAuthor && (
                    <button className="trash-button" onClick={handleDeleteButtonClick}>
                      <i className="fa fa-trash-o trash-icon-custom-size" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default PostCard;
