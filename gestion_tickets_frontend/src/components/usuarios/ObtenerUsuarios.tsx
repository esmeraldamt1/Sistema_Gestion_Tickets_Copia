import React, { useEffect, useState } from "react";
import {
  obtenerUsuarios,
  eliminarUsuario,
} from "@/services/api"; // Usamos funciones centralizadas

const ObtenerUsuarios: React.FC = () => {
  const [usuarios, setUsuarios] = useState<any[]>([]);

  // 🔄 Cargar usuarios al montar
  useEffect(() => {
    cargarUsuarios();
  }, []);

  const cargarUsuarios = async () => {
    try {
      const data = await obtenerUsuarios();
      setUsuarios(data);
    } catch (error) {
      console.error(" Error al obtener usuarios", error);
    }
  };

  const handleEliminar = async (id: string) => {
    const confirmar = window.confirm("¿Estás seguro de que deseas eliminar este usuario?");
    if (!confirmar) return;

    try {
      await eliminarUsuario(id); // Usamos función de services/api
      alert(" Usuario eliminado correctamente.");
      cargarUsuarios(); // Recargamos usuarios
    } catch (error) {
      console.error(" Error al eliminar usuario", error);
      alert("Hubo un error al eliminar el usuario.");
    }
  };

  return (
    <div>
      <h2>👥 Lista de Usuarios</h2>
      <ul>
        {usuarios.map((usuario) => (
          <li key={usuario.id} style={{ marginBottom: "8px" }}>
            {usuario.username} - {usuario.email}
            <button
              onClick={() => handleEliminar(usuario.id)}
              style={{ marginLeft: "10px", color: "red" }}
            >
              Eliminar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ObtenerUsuarios;
