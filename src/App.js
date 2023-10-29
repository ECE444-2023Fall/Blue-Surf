import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import PostCard from "./components/PostCard";
import FilterField from "./components/FilterField";

const postCardData = {
  title: "Fall Career Week",
  date: new Date(),
  location: "Myhal 5th Floor",
  description:
    "Come out to the Fall Career Week to meet recruiters from companies like RBC, Tesla and more!",
  tags: ["Professional Development"],
};

const numberOfCards = 10;

function App() {
  return (
    <div className="container">
      <div className="row">
        <div className="col-lg-3">
          <FilterField
            title="Filter by Tag"
            values={["Professional Development", "Jobs"]}
          />
        </div>

        <div className="row row-cols-1 row-cols-sm-2 row-cols-md-2 row-cols-lg-3 gx-3 gy-3">
          {Array.from({ length: numberOfCards }).map((_, index) => (
            <PostCard key={index} {...postCardData} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
