import React, { useState, useEffect } from "react";
import "./../App.css";
import "../styles/PersonalDashboard.css";
import "bootstrap/dist/css/bootstrap.min.css";
import PostCard from "./PostCard";
import SearchBar from "./SearchBar";
import "bootstrap/dist/css/bootstrap.min.css";

// this is mock data, to be replaced later once database is setup


const PersonalDashboard: React.FC = (PostCardProps: any) => {
  const [searchResults, setSearchResults] = useState(null);
  const [selectedButton, setSelectedButton] = useState("Favorites");

  const handleSearchData = (data: any) => {
    setSearchResults(data);
  };

  const handleButtonClick = (buttonName: any) => {
    setSelectedButton(buttonName);
  };

  useEffect(() => {
    setSelectedButton("Favorites");
  }, []);

  return (
    <div className="container">
        <div className="custom-container">
          <div className="content-container">
            <div className="row">
              <div className="col-md-12">
                <div className="row">
                  <div className="col-12">
                    <SearchBar onDataReceived={handleSearchData} />
                  </div>
                </div>
                <div>
                </div>
                <div className="row">
                  <div className="col-12 my-3 d-flex justify-content-around">
                  <div className="background-select">
                  <div className="d-flex justify-content-center"> 
                  <button
                      className={`twobutton-${selectedButton !== "Favorites" ? "notselect" : "select"}`}
                      onClick={() => handleButtonClick("Favorites")}>Favorites
                    </button>
                    <button
                      className={`twobutton-${selectedButton !== "My Posts" ? "notselect" : "select"}`}
                      onClick={() => handleButtonClick("My Posts")}>My Posts
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
}

export default PersonalDashboard;
