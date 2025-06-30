import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import API from "../api/api";
import BookingForm from "../pages/BookingForm";

const YachtDetails = () => {
  const { id } = useParams();
  const [yacht, setYacht] = useState(null);

  useEffect(() => {
    API.get(`/yachts/${id}`)
      .then((res) => setYacht(res.data))
      .catch((err) => console.error("Error:", err));
  }, [id]);

  if (!yacht) return <p>Loading...</p>;

  return (
    <div className="container">
      <h2>{yacht.name}</h2>
      <img src={yacht.image_url} alt={yacht.name} width="100%" />
      <p>{yacht.description}</p>
      <BookingForm yachtId={yacht.id} pricePerDay={yacht.price_per_day} />
    </div>
  );
};

export default YachtDetails;
