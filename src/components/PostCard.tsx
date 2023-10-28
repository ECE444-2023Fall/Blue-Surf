import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/PostCard.css";

interface PostCardProps {
  title: string;
  date: Date;
  location: string;
  description: string;
  tags: string[];
}

const PostCard: React.FC<PostCardProps> = (PostCardProps: any) => {
  return (
    <div className="col">
      <div className="card">
        <img src="../../assets/post1.jpeg" className="card-img-top" alt="..." />
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
          <span className="pill">
            {PostCardProps.tags.map((tag: string, index: number) => (
              <span key={index}>{tag}</span>
            ))}
          </span>
        </div>
      </div>
    </div>
  );
};

export default PostCard;
