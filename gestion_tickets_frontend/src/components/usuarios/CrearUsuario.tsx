import React, { useState } from "react";  // Importamos React y el hook useState para manejar estados
import { crearUsuario } from "../../services/api";  // Importamos la función para crear usuario desde el servicio API

const CrearUsuario: React.FC = () => {
  // Definimos estados locales para almacenar los datos del formulario
  const [username, setUsername] = useState("");  // Estado para el nombre de usuario
  const [email, setEmail] = useState("");        // Estado para el email
  const [password, setPassword] = useState("");  // Estado para la contraseña

  // Función que maneja la creación del usuario cuando se presiona el botón
  const handleCrearUsuario = async () => {
    // Validamos que todos los campos estén completos antes de enviar la solicitud
    if (!username || !email || !password) {
      alert("Por favor, completa todos los campos.");  // Mostramos alerta si hay campos vacíos
      return;  // Salimos de la función para no continuar con la creación
    }

    try {
      // Intentamos crear un nuevo usuario enviando los datos al backend vía API
      const nuevoUsuario = await crearUsuario({ username, email, password });
      alert(`Usuario creado: ${nuevoUsuario.username}`);  // Confirmación con el nombre del usuario creado
      // Reseteamos los campos del formulario para dejarlo vacío luego de crear
      setUsername("");
      setEmail("");
      setPassword("");
    } catch (error) {
      // Si hay un error en la solicitud, lo mostramos en consola y alertamos al usuario
      console.error("Error creando usuario", error);
      alert("Hubo un error al crear el usuario. Revisa la consola.");
    }
  };

  // Renderizado del formulario para crear usuario
  return (
    <div>
      <h2>Crear Usuario</h2>
      {/* Campo para ingresar nombre de usuario */}
      <input
        type="text"
        placeholder="Nombre de usuario"
        value={username}
        onChange={(e) => setUsername(e.target.value)}  // Actualiza el estado al cambiar el input
      />
      {/* Campo para ingresar email */}
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}  // Actualiza el estado al cambiar el input
      />
      {/* Campo para ingresar contraseña */}
      <input
        type="password"
        placeholder="Contraseña"
        value={password}
        onChange={(e) => setPassword(e.target.value)}  // Actualiza el estado al cambiar el input
      />
      {/* Botón para enviar y crear usuario */}
      <button onClick={handleCrearUsuario}>Crear Usuario</button>
    </div>
  );
};

// Exportamos el componente para poder usarlo en otras partes de la app
export default CrearUsuario;
