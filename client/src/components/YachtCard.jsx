import { Link } from "react-router-dom";
import "./YachtCard.css"; // Link to external CSS

const YachtCard = ({ yacht }) => {
  return (
    <div className="yacht-card">
      <h3>{yacht.name}</h3>
      <img
        src={yacht.image_url}
        alt={yacht.name}
        className="yacht-image"
      />
      <p>{yacht.description}</p>
      <p>💰 ${yacht.price_per_day} per day</p>

      <Link to={`/yachts/${yacht.id}`}>
        <button className="book-button">Book Now</button>
      </Link>
    </div>
  );
};

export default YachtCard;
