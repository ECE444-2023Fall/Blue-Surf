import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/LandingPage.css";
import PostCard from "./PostCard";
import FilterField from "./FilterField";
import SortBy from "./SortBy";
import SearchBar from "./SearchBar";
import DeletePopUp from "./DeletePopUp";
import API_URL from "../config";

// this is mock data, to be replaced later once database is setup
const postCardData = {
  title: "Fall Career Week",
  date: new Date(),
  location: "Myhal 5th Floor",
  description:
    "Come out to the Fall Career Week to meet recruiters from companies like RBC, Tesla and more!",
  tags: ["Professional Development"],
};

const filterOptionValuesByAPI = [
  {
    title: "Tag",
    values: ["All"],
  },
  {
    title: "Location",
    values: ["All", "Myhal 5th Floor", "Bahen", "Remote"],
  },
  {
    title: "Club",
    values: ["All", "YNCN", "Dance Club", "Design Club", "Sport Club"],
  },
  {
    title: "Date",
    values: ["All", "Today", "Tomorrow", "Never"],
  },
];

interface User {
  userId: string;
  username: string;
}

interface LandingPageProps {
  token: string;
  user: User;
  setAuth: (token: string | null, user: User | null) => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ token, user, setAuth }) => {
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showDeletePopUp, setShowDeletePopUp] = useState(false);
  const [postToBeDeleted, setPostToBeDeleted] = useState<number>();
  const [posTitleToBeDeleted, setPosTitleToBeDeleted] = useState<string>();
  const [filterParams, setFilterParams] = useState<{ [key: string]: string }>(
    {}
  );
  const navigate = useNavigate();

  const getFilterNames = async (filterName: string): Promise<any[] | null> => {
    let routeName = "tags";
    if (filterName === "Location") {
      routeName = "locations";
    } else if (filterName === "Club") {
      routeName = "clubs";
    }

    const response = await fetch(`${API_URL}/api/get-all-${routeName}`);
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      console.error(`Failed to fetch all ${filterName} names`);
      return null;
    }
  };

  const fetchDataAndInitializeFilters = async (filterName: string) => {
    const data = await getFilterNames(filterName);
    if (data) {
      const tagEntry = filterOptionValuesByAPI.find(
        (entry) => entry.title === filterName
      );
      if (tagEntry) {
        tagEntry.values = ["All", ...data];
      } else {
        filterOptionValuesByAPI.push({ title: filterName, values: data });
      }
    }
  };

  const fetchEvents = async () => {
    try {
      const response = await fetch(`${API_URL}/api/`); // Change this to the actual API endpoint
      if (response.ok) {
        const data = await response.json();
        setSearchResults(data);
      } else {
        console.error("Failed to fetch data");
      }
    } catch (error) {
      console.error("An error occurred while fetching data", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = async (
    filterTitle: string,
    selectedValue: string
  ) => {
    if (
      filterTitle.toLowerCase() === "end_time" &&
      selectedValue === "no_end_time"
    ) {
      setFilterParams((prevParams) => {
        const { end_time, ...restParams } = prevParams;
        return restParams;
      });
    } else if (
      filterTitle.toLowerCase() === "start_time" &&
      selectedValue === "no_start_time"
    ) {
      setFilterParams((prevParams) => {
        const { start_time, ...restParams } = prevParams;
        return restParams;
      });
    } else {
      setFilterParams((prevParams) => ({
        ...prevParams,
        [filterTitle.toLowerCase()]: selectedValue,
      }));
    }
  };

  useEffect(() => {
    fetchEvents();
    fetchDataAndInitializeFilters("Tag");
    fetchDataAndInitializeFilters("Location");
    fetchDataAndInitializeFilters("Club");
  }, []);

  useEffect(() => {
    // Fetch data when filter parameters change
    const fetchData = async () => {
      try {
        const queryParams = new URLSearchParams(filterParams);
        const response = await fetch(`${API_URL}/api/filter?${queryParams}`);
        if (response.ok) {
          const data = await response.json();
          setSearchResults(data);
        } else {
          console.error("Failed to fetch data");
        }
      } catch (error) {
        console.error("An error occurred while fetching data", error);
      }
    };

    fetchData();
  }, [filterParams]);

  const handleSearchData = (query: string) => {
    setFilterParams((prevParams) => ({
      ...prevParams,
      query,
    }));
  };

  const handleSortChange = (selectedValue: string) => {
    setFilterParams((prevParams) => ({
      ...prevParams,
      sortby: selectedValue.toLowerCase(),
    }));
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
          fetchEvents();
        } else {
          const errorMessage = await response.text();
          throw new Error(errorMessage || "Delete request failed");
        }
      } catch (error) {
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

  return (
    <div className="landing-page-wrapper">
      <div className="row">
        <div className="custom-col-md-3">
          {filterOptionValuesByAPI.map((option, index) => (
            <FilterField
              key={index}
              title={option.title}
              values={option.values}
              onFilterChange={handleFilterChange}
            />
          ))}
        </div>
        <div className="col-md-9">
          <div className="row">
            <div className="col-12">
              <SearchBar onDataReceived={handleSearchData} />
            </div>
          </div>
          <div className="row">
            <div className="col-12">
              <SortBy
                options={[
                  "Not Selected",
                  "Alphabetical",
                  "Trending",
                  "Start Time",
                ]}
                onSortChange={handleSortChange}
              />
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
        {showDeletePopUp && posTitleToBeDeleted && (
          <DeletePopUp
            postTitle={posTitleToBeDeleted}
            handleDelete={handleDelete}
          />
        )}
      </div>
    </div>
  );
};

export default LandingPage;
