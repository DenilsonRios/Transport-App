import React from 'react';
function PassengerPage() {


  return (
    <div className="passenger-container">
    <h1>Bienvenido, Pasajero</h1>
    <p>¡Encuentra tu próximo viaje!</p>
    <div className="user-info">
      <p>Usuario: Pasajero123</p>
      {/* Puedes mostrar más información del usuario aquí */}
    </div>
    <div className="location-section">
      <h2>Selecciona tu ubicación:</h2>
      {/* Agrega aquí algún componente para seleccionar la ubicación */}
    </div>
    <button className="request-button">Pedir Servicio</button>
  </div>
  );

  
};

export default PassengerPage;
