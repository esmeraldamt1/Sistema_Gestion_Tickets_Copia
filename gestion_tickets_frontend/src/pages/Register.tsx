import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../Styles/Register.css';
import axios from 'axios';

const Register: React.FC = () => {
  const navigate = useNavigate();

  // 👉 Aquí defines los estados para los campos del formulario
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Función para manejar el envío del formulario
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      console.log('Datos enviados:', { username, email, password });

      const response = await axios.post("http://localhost:8000/usuarios/register/", {
        username,
        email,
        password,
      });

      if (response.status === 201) {
        alert('Cuenta creada exitosamente');
        navigate('/login');
      }
    } catch (error: any) {
      if (error.response) {
        console.log('Error del backend:', error.response);
        alert(`Error al crear cuenta: ${error.response.data.error || 'Revisa los campos.'}`);
      } else {
        alert('Error de red. Intenta más tarde.');
      }
    }
  };

  return (
    <div className="register-page">
      <form className="auth-container" onSubmit={handleRegister}>
        <h2>Crear Cuenta</h2>
        <input
          className="auth-input"
          type="text"
          placeholder="Nombre de usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          className="auth-input"
          type="email"
          placeholder="Correo electrónico"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className="auth-input"
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button className="auth-button" type="submit">
          Crear Cuenta
        </button>
      </form>
    </div>
  );
};

export default Register;
