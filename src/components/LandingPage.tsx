import React, { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/LandingPage.css";
import PostCard from "./PostCard";
import FilterField from "./FilterField";
import SortBy from "./SortBy";
import SearchBar from "./SearchBar";

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
    values: ["All", "Myhal 5th Floor", "Bahen Lobby", "Remote"],
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

  const getTagNames = async (): Promise<any[] | null> => {
    const response = await fetch("/api/get-all-tags");
    if (response.ok) {
      const data = await response.json();
      console.log(data);
      return data;
    } else {
      console.error("Failed to fetch all tag names");
      return null;
    }
  };

  const fetchDataAndInitializeTags = async () => {
    const data = await getTagNames();
    if (data) {
      const tagEntry = filterOptionValuesByAPI.find(
        (entry) => entry.title === "Tag"
      );
      if (tagEntry) {
        tagEntry.values = ["All", ...data];
      } else {
        filterOptionValuesByAPI.push({ title: "Tag", values: data });
      }
    }
  };

  const fetchEvents = async () => {
    try {
      const response = await fetch("/api/"); // Change this to the actual API endpoint
      if (response.ok) {
        const data = await response.json();
        setSearchResults(data);
        console.log(data);
      } else {
        console.error("Failed to fetch data");
      }
    } catch (error) {
      console.error("An error occurred while fetching data", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
    fetchDataAndInitializeTags();
  }, []);

  const handleSearchData = (data: any) => {
    setSearchResults(data);
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
              <SortBy options={["Sort Option 1", "Sort Option 2"]} />
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
                  {...event}
                />
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
