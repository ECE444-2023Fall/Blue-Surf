import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostCard.css";
const defaultImage = require("../assets/image_placeholder.jpeg");

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
}

const PostCard: React.FC<PostCardProps> = (PostCardProps: any) => {
  const postId = PostCardProps.id;

  const [isLiked, setIsLiked] = React.useState(false);
  const [imageFile, setImageFile] = React.useState<File | null>(null);

  const fetchImage = async () => {
    try {
      const postImageResponse = await fetch(`/api/${postId}/image`);
      if (!postImageResponse || !postImageResponse.ok) {
        throw new Error("Cannot fetch post image.");
      }

      // Get the image data as a Blob
      const imageBlob = await postImageResponse.blob();

      console.log("blob", imageBlob);

      // Create a File object with the image data
      const newImageFile = new File([imageBlob], `image_${postId}.png`, {
        type: "image/png", // Adjust the type based on your image format
      });

      console.log("file", newImageFile);

      // Set the image file in state
      setImageFile(newImageFile);
    } catch (error) {
      console.error("Error fetching postcard image:", error);
    }
  };

  useEffect(() => {
    fetchImage();
  }, []);

  const toggleLike = () => {
    setIsLiked(!isLiked);
  };

  const handleDelete = () => {
    // TODO: display pop up and perform delete upon confirmation
    console.log("Post deleted!");
  };

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
                        <span className="pill" data-testid="post-tags">
                          <span className="pill-tag" key={index}>
                            {tag}
                          </span>
                        </span>
                      ))}
                    </>
                  )}
                </div>
              </div>
              <div className="col-auto">
                <div onClick={(e) => e.preventDefault()}>
                  <button
                    className={`like-button ${isLiked ? "liked" : ""}`}
                    onClick={toggleLike}
                    data-testid="like-button"
                  >
                    <i className={`fa fa-heart${isLiked ? "" : "-o"}`} />
                  </button>
                  <button className="trash-button" onClick={handleDelete}>
                    <i className="fa fa-trash-o trash-icon-custom-size" />
                  </button>
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
