import React from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostCard.css";
const postImage = require("../assets/post1.jpeg");

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
  const [isLiked, setIsLiked] = React.useState(false);

  const toggleLike = () => {
    setIsLiked(!isLiked);
  };

  return (
    <div className="col" data-testid="post-card">
      <Link to={`/post/${PostCardProps.id}`} className="text-decoration-none">
        <div className="card">
          <img
            src={postImage}
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
              {PostCardProps.tags.length > 0 && (
                <div className="col">
                  {PostCardProps.tags.map((tag: string, index: number) => (
                    <span className="pill" data-testid="post-tags">
                      <span className="pill-tag" key={index}>
                        {tag}
                      </span>
                    </span>
                  ))}
                </div>
              )}
              <div className="col-auto">
                <div onClick={(e) => e.preventDefault()}>
                  <button
                    className={`like-button ${isLiked ? "liked" : ""}`}
                    onClick={toggleLike}
                    data-testid="like-button"
                  >
                    <i className={`fa fa-heart${isLiked ? "" : "-o"}`} />
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
