import { useEffect, useState } from "react";
import API from "../api/api";

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    API.get("/bookings/my")
      .then((res) => setBookings(res.data))
      .catch(() => alert("Failed to fetch your bookings"));
  }, []);

  return (
    <div>
      <h2>My Bookings</h2>
      {bookings.length === 0 ? (
        <p>No bookings yet.</p>
      ) : (
        bookings.map((b) => (
          <div key={b.id} className="booking-card">
            <h3>{b.yacht.name}</h3>
            <p>{b.start_date} → {b.end_date}</p>
            <p>Total: ${b.total_price}</p>
            <p>Request: {b.special_request}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default MyBookings;
