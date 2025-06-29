// src/pages/BookingForm.jsx
import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import API from "../api/api";

const BookingForm = () => {
  const { id } = useParams(); // Yacht ID from URL
  const navigate = useNavigate();
  const { user } = useAuth();

  const [yacht, setYacht] = useState(null);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // 🛥️ Fetch yacht details
  useEffect(() => {
    API.get(`/yachts/${id}`)
      .then((res) => {
        setYacht(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading yacht:", err);
        setError("Could not load yacht data.");
        setLoading(false);
      });
  }, [id]);

  const calculateDays = () => {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diff = (end - start) / (1000 * 60 * 60 * 24);
    return diff > 0 ? diff : 0;
  };

  const handleBooking = async () => {
    if (!user) {
      alert("Please log in to book a yacht.");
      return;
    }

    try {
      const totalDays = calculateDays();
      const payload = {
        yacht_id: parseInt(id), // 👈 force int to avoid Flask type issues
        start_date: startDate,
        end_date: endDate,
        total_price: yacht.price_per_day * totalDays,
        special_request: "Please include drinks 🍹",
      };

      console.log("Sending booking:", payload);

      const res = await API.post("/bookings", payload);
      alert("Booking successful!");
      navigate("/my-bookings");
    } catch (err) {
      console.error("Booking failed:", err.response?.data || err.message);
      alert(err.response?.data?.error || "Booking failed.");
    }
  };

  if (loading) return <p>Loading yacht details...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Book {yacht.name}</h2>
      <p><strong>Location:</strong> {yacht.location}</p>
      <p><strong>Price per day:</strong> ${yacht.price_per_day}</p>

      <label htmlFor="startDate">Start Date:</label><br />
      <input
        id="startDate"
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
      /><br />

      <label htmlFor="endDate">End Date:</label><br />
      <input
        id="endDate"
        type="date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
      /><br />

      <p><strong>Total Days:</strong> {calculateDays()}</p>
      <p><strong>Total Price:</strong> ${yacht.price_per_day * calculateDays()}</p>

      <button onClick={handleBooking}>Confirm Booking</button>
    </div>
  );
};

export default BookingForm;
