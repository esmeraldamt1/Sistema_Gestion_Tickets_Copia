import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css"; // Asegurar estilos

const Navbar: React.FC = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/">Inicio</Link></li>
        <li><Link to="/usuarios">Usuarios</Link></li>
        <li><Link to="/tickets">Tickets</Link></li>
        <li><Link to="/ayuda">Ayuda</Link></li>
        <li><Link to="/reportes">Reportes</Link></li>
        <li><Link to="/saldo">Saldo</Link></li>
        <li><Link to="/comprar-horas">Comprar Horas</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
