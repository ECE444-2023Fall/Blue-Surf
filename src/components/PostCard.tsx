import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
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
  return (
    <div className="col" data-testid="post-card">
      <div className="card">
        <img src={postImage} className="card-img-top rounded-top-34" alt="..." />
        <div className="card-body">
          <div className="d-flex justify-content-center">
            <span className="h4 card-title text-center" data-testid="post-title">
              {PostCardProps.title}
            </span>
          </div>
          <p className="p text-center" data-testid="post-date-location">
            {PostCardProps.date.toDateString()} | {PostCardProps.location}
          </p>
          <p className="card-text text-left" data-testid="post-description">
            {PostCardProps.description}
          </p>
          <span className="pill" data-testid="post-tags">
            {PostCardProps.tags.map((tag: string, index: number) => (
              <span className="pill-tag" key={index}>{tag}</span>
            ))}
          </span>
        </div>
      </div>
    </div>
  );
};

export default PostCard;
