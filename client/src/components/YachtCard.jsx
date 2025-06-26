const YachtCard = ({ yacht }) => {
    return (
      <div className="yacht-card">
        <h2>{yacht.name}</h2>
        <img src={yacht.image_url} alt={yacht.name} width="100%" style={{ borderRadius: '10px' }} />
        <p>{yacht.description}</p>
        <p><strong>Location:</strong> {yacht.location}</p>
        <p><strong>Price per Day:</strong> ${yacht.price_per_day}</p>
      </div>
    );
  };
  
  export default YachtCard;
  