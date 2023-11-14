import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./../App.css";
import "../styles/PersonalDashboard.css";
import "bootstrap/dist/css/bootstrap.min.css";
import PostCard from "./PostCard";
import DeletePopUp from "./DeletePopUp";
import "bootstrap/dist/css/bootstrap.min.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { faCalendarAlt } from "@fortawesome/free-solid-svg-icons";
import API_URL from "../config";
import { ToastContainer, toast } from "react-toastify";
import * as ics from "ics";

interface User {
  userId: string;
  username: string;
}

interface DashboardProps {
  token: string;
  user: User;
  setAuth: (token: string | null, user: User | null) => void;
}

interface Post {
  title: string;
  start_time: string;
  location: string;
  description: string;
  extended_description: string;
  tags: string[];
  id: number;
  author_id: number;
  is_published: boolean;
  end_time: string;
  like_count: number;
  club?: string;
}

const PersonalDashboard: React.FC<DashboardProps> = ({
  token,
  user,
  setAuth,
}) => {
  const [searchResults, setSearchResults] = useState([]);
  const [selectedButton, setSelectedButton] = useState("My Posts");
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [showDeletePopUp, setShowDeletePopUp] = useState(false);
  const [postToBeDeleted, setPostToBeDeleted] = useState<number>();
  const [posTitleToBeDeleted, setPosTitleToBeDeleted] = useState<string>();

  const fetchEvents = async (buttonName: string) => {
    try {
      let route = `${API_URL}/api/dashboard`;
      if (buttonName === "Favourites") {
        route = `${API_URL}/api/favourites`;
      }
      const response = await fetch(`${route}`, {
        headers: {
          Authorization: "Bearer " + token,
        },
      });

      if (response.ok) {
        const data = await response.json();
        data.access_token && setAuth(data.access_token, user); //Refreshes token if needed
        setSearchResults(data);
      } else {
        throw new Error("Failed to fetch data");
      }
    } catch (error) {
      console.error("An error occurred while fetching data", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents("My Posts");
  }, []);

  const handleButtonClick = (buttonName: string) => {
    setSelectedButton(buttonName);
    fetchEvents(buttonName);
  };

  const handleCreateButtonClick = () => {
    navigate("/create");
  };

  const handleDelete = async (confirmed: boolean) => {
    if (confirmed) {
      try {
        const response = await fetch(
          `${API_URL}/api/delete-post/${postToBeDeleted}`,
          {
            method: "POST",
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          data.access_token && setAuth(data.access_token, user);
          fetchEvents(selectedButton);
          toast.success(`Deleted ${posTitleToBeDeleted}.`, {
            position: toast.POSITION.TOP_CENTER,
          });
        } else {
          const errorMessage = await response.text();
          throw new Error(errorMessage || "Delete request failed");
        }
      } catch (error: any) {
        toast.error(`Oops, something went wrong. Please try again later!`, {
          position: toast.POSITION.TOP_CENTER,
        });
        console.error("Delete Post Error:", error);
      }
    }
    setShowDeletePopUp(false);
  };

  const setUpDelete = (postId: number, postTitle: string) => {
    setPostToBeDeleted(postId);
    setPosTitleToBeDeleted(postTitle);
    setShowDeletePopUp(true);
  };

  function parseDateString(dateString: string): Date {
    const [datePart, timePart] = dateString.split(" ");
    const [year, month, day] = datePart.split("-").map(Number);
    const [hour, minute, second] = timePart.split(":").map(Number);
    return new Date(year, month - 1, day, hour, minute, second);
  }

  // Function to convert an array of events to the ics.EventAttributes format
  function convertToEventAttributes(events: Post[]): ics.EventAttributes[] {
    return events.map((event) => {
      const { title, start_time, location, description, end_time } = event;

      // Convert start_time and end_time to Date objects
      const startDate = parseDateString(start_time);
      const endDate = parseDateString(end_time);

      // Convert start_time to an array representing [year, month, day]
      const startArray: [number, number, number] = [
        startDate.getFullYear(),
        startDate.getMonth() + 1,
        startDate.getDate(),
      ];

      // Calculate duration based on the end_time - start_time
      const durationInMinutes =
        (endDate.getTime() - startDate.getTime()) / (1000 * 60);

      const duration = {
        hours: Math.floor(durationInMinutes / 60),
        minutes: durationInMinutes % 60,
      };

      // Create the ics.EventAttributes object
      const icsEvent: ics.EventAttributes = {
        start: startArray,
        duration,
        title,
        description,
        location,
      };

      return icsEvent;
    });
  }

  const handleExportCalendar = () => {
    //Export events to ics
    const events = convertToEventAttributes(searchResults);

    const { error, value } = ics.createEvents(events);

    if (error || value === undefined) {
      toast.error("Error exporting calendar events.", {
        position: toast.POSITION.TOP_CENTER,
      });
      console.error("Error exporting calendar events:", error);
      return;
    }

    // Create a Blob with the iCalendar data
    const blob = new Blob([value], { type: "text/calendar;charset=utf-8" });

    // Create a download link
    const downloadLink = document.createElement("a");
    downloadLink.href = window.URL.createObjectURL(blob);
    downloadLink.download = "calendar.ics";

    // Append the link to the body
    document.body.appendChild(downloadLink);

    // Trigger a click on the link to start the download
    downloadLink.click();

    // Remove the link from the body
    document.body.removeChild(downloadLink);
  };

  return (
    <div className="container dashboard-wrapper">
      {showDeletePopUp && posTitleToBeDeleted && (
        <DeletePopUp
          postTitle={posTitleToBeDeleted}
          handleDelete={handleDelete}
          page="dashboard"
        />
      )}
      <div className="custom-container">
        <div className="content-container">
          <div className="row">
            <div className="col-md-12">
              <div className="row">
                <div className="col-12 my-3">
                  <div className="d-flex dashboard-buttons">
                    <div className="fill-space"></div>
                    <div className="background-select">
                      <button
                        className={`twobutton-${
                          selectedButton !== "My Posts" ? "notselect" : "select"
                        }`}
                        onClick={() => handleButtonClick("My Posts")}
                      >
                        My Posts
                      </button>
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
                    </div>
                    <div className="create-button-div">
                      {selectedButton === "Favourites" && (
                        <button
                          className="calendar-button"
                          onClick={handleExportCalendar}
                        >
                          <div className="plus-icon">
                            <FontAwesomeIcon icon={faCalendarAlt} />
                          </div>
                          <span>Export iCal</span>
                        </button>
                      )}
                      {selectedButton === "My Posts" && (
                        <button
                          className="create-button"
                          onClick={handleCreateButtonClick}
                        >
                          <div className="plus-icon">
                            <FontAwesomeIcon icon={faPlus} />
                          </div>
                          <span>Create Post</span>
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="row row-cols-1 row-cols-sm-2 row-cols-md-2 row-cols-lg-3 gx-3 gy-3">
          {loading ? (
            <p>Loading...</p>
          ) : (
            searchResults.map((event: any, index: number) => (
              <PostCard
                key={index}
                token={token}
                user={user}
                setAuth={setAuth}
                showDeletePopUp={setUpDelete}
                {...event}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default PersonalDashboard;
