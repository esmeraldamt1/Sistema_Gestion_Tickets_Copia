import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Panel.css";

const Panel: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="panel-container">
      <h1 className="titulo">Gestión de Tickets</h1>
      <h3 className="subtitulo">Panel de Navegación</h3>
      <button onClick={() => navigate("/tickets")}>Tickets</button>
      <button onClick={() => navigate("/ayuda")}>Ayuda y Soporte</button>
      <button onClick={() => navigate("/reportes")}>Reportes</button>
      <button onClick={() => navigate("/saldo")}>Saldo</button>
      <button onClick={() => navigate("/comprar-horas")}>Comprar Horas</button>
      <button onClick={() => navigate("/")}>Cerrar sesión</button>
    </div>
  );
};

export default Panel;
