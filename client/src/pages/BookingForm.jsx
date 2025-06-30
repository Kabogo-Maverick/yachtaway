// ✅ src/pages/BookingForm.jsx
import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import API from "../api/api";

const BookingForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [yacht, setYacht] = useState(null);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [addons, setAddons] = useState([]);
  const [selectedAddons, setSelectedAddons] = useState([]);

  useEffect(() => {
    API.get(`/yachts/${id}`).then((res) => setYacht(res.data));
    API.get(`/addons`).then((res) => setAddons(res.data));
  }, [id]);

  const calculateDays = () => {
    const start = new Date(startDate);
    const end = new Date(endDate);
    return (end - start) / (1000 * 60 * 60 * 24);
  };

  const calculateTotalAddOnCost = () => {
    return selectedAddons.reduce((sum, addonId) => {
      const addon = addons.find((a) => a.id === addonId);
      return sum + (addon ? addon.price : 0);
    }, 0);
  };

  const handleBooking = async () => {
    if (!startDate || !endDate || !yacht) {
      alert("Missing required fields");
      return;
    }
  
    try {
      const response = await API.post("/bookings", {
        yacht_id: yacht.id,
        start_date: startDate,
        end_date: endDate,
        total_price: yacht.price_per_day * calculateDays() + calculateTotalAddOnCost(),
        special_request: "Include drinks",
        addon_ids: selectedAddons, // ✅ Only if backend supports it
      });
      alert("Booking successful");
      navigate("/my-bookings");
    } catch (err) {
      console.error("Booking failed:", err.response?.data || err.message);
      alert("Booking failed");
    }
  };
  

  if (!yacht) return <p>Loading...</p>;

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h2>Book {yacht.name}</h2>
      <label>Start Date</label>
      <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
      <label>End Date</label>
      <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
      <h4>Add-ons</h4>
      {addons.map((addon) => (
        <div key={addon.id}>
          <label>
            <input
              type="checkbox"
              checked={selectedAddons.includes(addon.id)}
              onChange={(e) => {
                const checked = e.target.checked;
                setSelectedAddons((prev) =>
                  checked ? [...prev, addon.id] : prev.filter((id) => id !== addon.id)
                );
              }}
            />
            {addon.name} (${addon.price})
          </label>
        </div>
      ))}
      <p><strong>Total Price:</strong> ${yacht.price_per_day * calculateDays() + calculateTotalAddOnCost()}</p>
      <button onClick={handleBooking}>Book Now</button>
    </div>
  );
};

export default BookingForm;