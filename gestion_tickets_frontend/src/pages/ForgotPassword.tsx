import React, { useState } from 'react';
import axios from 'axios';
import '../Styles/ForgotPassword.css'; // Importamos los estilos CSS específicos para este formulario

// Componente funcional de recuperación de contraseña
const ForgotPassword: React.FC = () => {
  // Estado para almacenar el correo ingresado por el usuario
  const [correo, setCorreo] = useState('');

  // Estado para mensajes de éxito
  const [mensaje, setMensaje] = useState('');

  // Estado para mensajes de error
  const [error, setError] = useState('');

  // Maneja el envío del formulario
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Evita recargar la página

    try {
      // Se envía una solicitud POST al backend con el correo
      const response = await axios.post('http://localhost:8000/usuarios/enviar-enlace/', {
        correo,
      });

      // Si la respuesta es exitosa, mostramos el mensaje y limpiamos errores
      setMensaje(response.data.mensaje);
      setError('');
    } catch (err: any) {
      // Si ocurre un error, mostramos el mensaje de error correspondiente
      const res = err.response;
      if (res && res.data && res.data.error) {
        setError(res.data.error);
      } else {
        setError('Error al enviar el enlace de recuperación');
      }
      setMensaje('');
    }
  };

  return (
    // Contenedor general con fondo centrado (como en login)
    <div className="forgot-background">
      {/* Formulario centrado con fondo semitransparente */}
      <form className="forgot-form" onSubmit={handleSubmit}>
        {/* Título */}
        <h2>Recuperar Contraseña</h2>

        {/* Campo de entrada para correo */}
        <input
          type="email"
          placeholder="Correo electrónico"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
          required
        />

        {/* Botón para enviar la solicitud */}
        <button type="submit">Enviar enlace de recuperación</button>

        {/* Mensajes de éxito o error */}
        {mensaje && <p className="mensaje">{mensaje}</p>}
        {error && <p className="mensaje" style={{ color: 'red' }}>{error}</p>}

        {/* Enlace para volver al login */}
        <div className="volver-login">
          <a href="/login">Volver al inicio de sesión</a>
        </div>
      </form>
    </div>
  );
};

export default ForgotPassword;
