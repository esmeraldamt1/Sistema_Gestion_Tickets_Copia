import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../styles/Login.css";

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:8000/usuarios/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        navigate("/panel");
      } else {
        setError("Usuario o contraseña incorrectos");
      }
    } catch (error) {
      setError("Error al conectar con el servidor");
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h1>Gestión De Tickets</h1>
        <form onSubmit={handleLogin}>
          <div className="input-group">
            <label htmlFor="username">Usuario</label>
            <input
              id="username"
              type="text"
              placeholder="Ingrese Usuario"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="full-width-input"
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              placeholder="Ingrese Contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="full-width-input"
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button type="submit" className="login-button">
            Iniciar Sesión
          </button>

          <div className="options">
            <Link to="/forgot-password" className="text-white underline hover:text-orange-400">
              Olvidé mi contraseña
            </Link>
            <Link to="/register" className="text-white underline hover:text-orange-400">
              Crear Cuenta
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
