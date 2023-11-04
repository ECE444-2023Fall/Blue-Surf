import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostDetailsPage.css";
const postImage = require("../assets/post1.jpeg");

interface PostDetailsProps {
  title: string;
  date: Date;
  location: string;
  description: string;
  tags: string[];
}

const PostDetailsPage: React.FC<PostDetailsProps> = (PostDetailsProps: any) => {
  return (
    <div className="container bg-white rounded-5 p-5 mt-2 mb-2">
      <div className="row m-2">
        <a className="navbar-brand back-nav" href="javascript:history.back()">
          <img
            src="https://cdn-icons-png.flaticon.com/512/271/271220.png"
            width="30"
            height="30"
            className="d-inline-block align-items-center"
            alt=""
          />
          <span className="back-text">Back</span>
        </a>
      </div>
    </div>
  );
};

export default PostDetailsPage;
