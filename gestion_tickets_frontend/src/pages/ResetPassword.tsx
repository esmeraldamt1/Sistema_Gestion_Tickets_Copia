import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "../Styles/ResetPassword.css"; 

const ResetPassword: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();
  const [nuevaContrasena, setNuevaContrasena] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        `http://localhost:8000/usuarios/cambiar-contrasena/${token}/`,
        { nueva_contrasena: nuevaContrasena }
      );

      setMensaje(response.data.mensaje);
      setError("");
      setTimeout(() => navigate("/login"), 3000); // Redirige después de 3 seg
    } catch (err: any) {
      const msg = err?.response?.data?.error || "Error al cambiar la contraseña";
      setError(msg);
      setMensaje("");
    }
  };

  return (
    <div className="reset-container">
      <form className="reset-form" onSubmit={handleSubmit}>
        <h2>Restablecer Contraseña</h2>

        {mensaje && <div className="success-message">{mensaje}</div>}
        {error && <div className="error-message">{error}</div>}

        <input
          type="password"
          placeholder="Nueva contraseña"
          value={nuevaContrasena}
          onChange={(e) => setNuevaContrasena(e.target.value)}
          required
        />

        <button type="submit">Cambiar contraseña</button>
      </form>
    </div>
  );
};

export default ResetPassword;
