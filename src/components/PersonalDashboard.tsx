import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./../App.css";
import "../styles/PersonalDashboard.css";
import "bootstrap/dist/css/bootstrap.min.css";
import PostCard from "./PostCard";
import SearchBar from "./SearchBar";
import "bootstrap/dist/css/bootstrap.min.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";

// this is mock data, to be replaced later once database is setup

const PersonalDashboard: React.FC = (PostCardProps: any) => {
  const [searchResults, setSearchResults] = useState(null);
  const [selectedButton, setSelectedButton] = useState("Favourites");
  const navigate = useNavigate();

  const handleSearchData = (data: any) => {
    setSearchResults(data);
  };

  const handleButtonClick = (buttonName: any) => {
    setSelectedButton(buttonName);
  };

  const handleCreateButtonClick = () => {
    navigate("/create");
  };

  useEffect(() => {
    setSelectedButton("Favourites");
  }, []);

  return (
    <div className="container dashboard-wrapper">
      <div className="custom-container">
        <div className="content-container">
          <div className="row">
            <div className="col-md-12">
              <div className="row">
                <div className="col-12">
                  <SearchBar onDataReceived={handleSearchData} />
                </div>
              </div>
              <div></div>
              <div className="row">
                <div className="col-12 my-3">
                  <div className="d-flex dashboard-buttons">
                    <div className="fill-space"></div>
                    <div className="background-select">
                      <button
                        className={`twobutton-${
                          selectedButton !== "Favourites"
                            ? "notselect"
                            : "select"
                        }`}
                        onClick={() => handleButtonClick("Favourites")}
                      >
                        Favourites
                      </button>
                      <button
                        className={`twobutton-${
                          selectedButton !== "My Posts" ? "notselect" : "select"
                        }`}
                        onClick={() => handleButtonClick("My Posts")}
                      >
                        My Posts
                      </button>
                    </div>
                    <div className="create-button-div">
                      <button
                        className="create-button"
                        onClick={handleCreateButtonClick}
                      >
                        <div className="plus-icon">
                          <FontAwesomeIcon icon={faPlus} />
                        </div>
                        <span>Create Post</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="row row-cols-1 row-cols-sm-2 row-cols-md-2 row-cols-lg-3 gx-3 gy-3">
          {Array.from({ length: 10 }).map((event: any, index: number) => (
            <PostCard key={index} {...event} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default PersonalDashboard;
