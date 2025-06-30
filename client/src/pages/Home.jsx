import { useEffect, useState } from "react";
import API from "../api/api";
import YachtCard from "../components/YachtCard";

const Home = () => {
  const [yachts, setYachts] = useState([]);

  useEffect(() => {
    API.get("/yachts")
      .then((res) => setYachts(res.data))
      .catch((err) => console.error("Error fetching yachts:", err));
  }, []);

  return (
    <div className="container">
      <h1>Available Yachts</h1>
      {yachts.map((yacht) => (
        <YachtCard key={yacht.id} yacht={yacht} />
      ))}
    </div>
  );
};

export default Home;
// This component fetches the list of yachts
// from the Flaskbackend and displays
// them using the 
// YachtCard component.