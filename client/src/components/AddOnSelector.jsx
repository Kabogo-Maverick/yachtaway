import { useEffect, useState } from "react";
import API from "../api/api";

const AddOnSelector = ({ onSelect }) => {
  const [addons, setAddons] = useState([]);
  const [selected, setSelected] = useState([]);

  useEffect(() => {
    API.get("/addons")
      .then((res) => setAddons(res.data))
      .catch((err) => console.error("AddOn error:", err));
  }, []);

  const toggleAddOn = (addon) => {
    const isSelected = selected.some((a) => a.id === addon.id);
    const updated = isSelected
      ? selected.filter((a) => a.id !== addon.id)
      : [...selected, addon];
    setSelected(updated);
    onSelect(updated);
  };

  return (
    <div className="addons">
      <h4>Add-Ons</h4>
      {addons.map((addon) => (
        <label key={addon.id}>
          <input
            type="checkbox"
            onChange={() => toggleAddOn(addon)}
            checked={selected.some((a) => a.id === addon.id)}
          />
          {addon.name} (${addon.price})
        </label>
      ))}
    </div>
  );
};

export default AddOnSelector;
