import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import PostCard from "./components/PostCard";

const postCardData = {
  title: "Fall Career Week",
  date: new Date(),
  location: "Myhal 5th Floor",
  description:
    "Come out to the Fall Career Week to meet recruiters from companies like RBC, Tesla and more!",
  tags: ["Professional Development", "Jobs"],
};

const numberOfCards = 10;

function App() {
  return (
    <div
      className="container"
    >
      <div className="row row-cols-1 row-cols-sm-2 row-cols-md-2 row-cols-lg-3 gx-3 gy-3">
        {Array.from({ length: numberOfCards }).map((_, index) => (
          <PostCard key={index} {...postCardData} />
        ))}
      </div>
    </div>
  );
}

export default App;
