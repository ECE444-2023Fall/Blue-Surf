import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostCard.css";
const postImage = require("../assets/post1.jpeg");

interface PostCardProps {
  title: string;
  date: Date;
  location: string;
  description: string;
  tags: string[];
}

const PostCard: React.FC<PostCardProps> = (PostCardProps: any) => {
  const [isLiked, setIsLiked] = React.useState(false);

  const toggleLike = () => {
    setIsLiked(!isLiked);
  };

  return (
    <div className="col">
      <div className="card">
        <img
          src={postImage}
          className="card-img-top rounded-top-34"
          alt="..."
        />
        <div className="card-body">
          <div className="d-flex justify-content-center">
            <span className="h4 card-title text-center">
              {PostCardProps.title}
            </span>
          </div>
          <p className="p text-center">
            {PostCardProps.date.toDateString()} | {PostCardProps.location}
          </p>
          <p className="card-text text-left">{PostCardProps.description}</p>
          <div className="row">
            <div className="col">
              <span className="pill">
                {PostCardProps.tags.map((tag: string, index: number) => (
                  <span className="pill-tag" key={index}>
                    {tag}
                  </span>
                ))}
              </span>
            </div>
            <div className="col-auto">
              <button
                className={`like-button ${isLiked ? "liked" : ""}`}
                onClick={toggleLike}
              >
                <i className={`fa fa-heart${isLiked ? "" : "-o"}`} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostCard;
