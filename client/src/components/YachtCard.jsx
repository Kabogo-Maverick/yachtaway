import { Link } from "react-router-dom";

const YachtCard = ({ yacht }) => {
  return (
    <div className="yacht-card">
      <h3>{yacht.name}</h3>
      <img src={yacht.image_url} alt={yacht.name} width="300" />
      <p>{yacht.description}</p>
      <p>💰 ${yacht.price_per_day} per day</p>

      <Link to={`/yachts/${yacht.id}`}>
        <button style={styles.button}>Book Now</button>
      </Link>
    </div>
  );
};

const styles = {
  button: {
    padding: "0.5rem 1rem",
    backgroundColor: "#0077cc",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    marginTop: "1rem",
  },
};

export default YachtCard;
