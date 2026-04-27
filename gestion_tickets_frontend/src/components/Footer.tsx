// Componente: Footer.tsx
// Descripción: Pie de página de la aplicación

import React from "react";

const Footer: React.FC = () => {
  return (
    <footer style={{ padding: "10px", background: "#282c34", color: "white", textAlign: "center", marginTop: "20px" }}>
      <p>© 2025 Sistema de Gestión de Tickets - Todos los derechos reservados</p>
    </footer>
  );
};

export default Footer; // Exportación del componente para su uso en otras partes de la aplicación
