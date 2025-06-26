import { useState, useEffect } from "react";
import API from "../api/api";
import AddOnSelector from "./AddOnSelector";

const BookingForm = ({ yachtId, pricePerDay }) => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [addons, setAddons] = useState([]);
  const [selectedAddOns, setSelectedAddOns] = useState([]);

  const calcTotalPrice = () => {
    const days = (new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24);
    const addonTotal = selectedAddOns.reduce((acc, addon) => acc + addon.price, 0);
    return days > 0 ? (pricePerDay * days) + addonTotal : 0;
  };

  const handleBooking = async () => {
    try {
      const bookingRes = await API.post("/bookings", {
        user_id: 1,  // TEMP: replace with session later
        yacht_id: yachtId,
        start_date: startDate,
        end_date: endDate,
        total_price: calcTotalPrice(),
        special_request: "Please include towels"
      });

      for (const addon of selectedAddOns) {
        await API.post("/booking-addons", {
          booking_id: bookingRes.data.id,
          addon_id: addon.id
        });
      }

      alert("Booking successful!");
    } catch (err) {
      console.error("Booking failed:", err);
      alert("Booking failed.");
    }
  };

  return (
    <div className="booking-form">
      <h3>Book this Yacht</h3>
      <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
      <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
      <AddOnSelector onSelect={setSelectedAddOns} />
      <p>Total Price: ${calcTotalPrice().toFixed(2)}</p>
      <button onClick={handleBooking}>Book Now</button>
    </div>
  );
};

export default BookingForm;
