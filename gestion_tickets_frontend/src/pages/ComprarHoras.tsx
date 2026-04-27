// Importa los hooks de estado y efecto desde React
import { useEffect, useState } from "react";

// Importa axios para hacer solicitudes HTTP
import axios from "axios";

// Importa la función que obtiene los usuarios desde la API
import { obtenerUsuarios } from "../services/api";

// Importa los estilos personalizados del componente
import "../styles/ComprarHoras.css";

// Importa las librerías necesarias para exportar a Excel
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

// Interfaz para definir la estructura de un usuario
interface Usuario {
  id: string; // ID único del usuario
  username: string; // Nombre de usuario
  email: string; // Correo electrónico del usuario
}

// Interfaz para definir la estructura de una compra
interface Compra {
  cantidad_horas: number; // Cantidad de horas compradas
  valor_por_hora: number; // Precio por cada hora
  total_pagado: number; // Total pagado por la compra
  fecha_compra: string; // Fecha de la compra
}

// Componente principal ComprarHoras
const ComprarHoras = () => {
  // Estado que almacena la lista de usuarios disponibles
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);

  // Estado que guarda el ID del usuario seleccionado
  const [usuarioId, setUsuarioId] = useState("");

  // Estado que almacena la cantidad de horas a comprar
  const [horas, setHoras] = useState<number>(0);

  // Estado que almacena el precio por hora en USD
  const [precioPorHora, setPrecioPorHora] = useState<number>(0);

  // Estado que muestra mensajes de error o éxito
  const [mensaje, setMensaje] = useState<string>("");

  // Estado que contiene el historial de compras del usuario
  const [compras, setCompras] = useState<Compra[]>([]);

  // useEffect que se ejecuta al montar el componente para cargar los usuarios
  useEffect(() => {
    const cargarUsuarios = async () => {
      try {
        const res = await obtenerUsuarios(); // Llama a la API
        setUsuarios(res); // Guarda los usuarios en estado
      } catch {
        setMensaje("Error al cargar usuarios."); // Manejo de error
      }
    };
    cargarUsuarios(); // Ejecuta la función
  }, []);

  // Función que realiza la compra de horas
  const comprarHoras = async () => {
    // Validación de datos ingresados
    if (!usuarioId || horas <= 0 || precioPorHora <= 0) {
      setMensaje("Complete todos los campos con valores válidos.");
      return;
    }

    try {
      const token = localStorage.getItem("token"); // Obtiene el token JWT

      const response = await axios.post(
        `http://127.0.0.1:8000/comprar_horas/${usuarioId}/`,
        {
          cantidad_horas: horas,
          valor_por_hora: precioPorHora,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`, // Envía el token en el header
          },
        }
      );

      setMensaje("Compra realizada con éxito."); // Mensaje de confirmación
      setCompras([response.data, ...compras]); // Agrega la compra al historial
    } catch (error: any) {
      setMensaje(error.response?.data?.error || "Error al realizar la compra."); // Error personalizado o genérico
    }
  };

  // Función que consulta el historial de compras del usuario
  const consultarCompras = async () => {
    if (!usuarioId) {
      setMensaje("Seleccione un usuario para consultar.");
      return;
    }

    try {
      const token = localStorage.getItem("token"); // Obtiene el token

      const response = await axios.get(
        `http://127.0.0.1:8000/comprar_horas/historial/${usuarioId}/`,
        {
          headers: {
            Authorization: `Bearer ${token}`, // Header con token JWT
          },
        }
      );

      setCompras(response.data); // Almacena historial
      setMensaje(""); // Limpia mensajes
    } catch (error: any) {
      setCompras([]); // Limpia historial si falla
      setMensaje(error.response?.data?.error || "No se encontraron compras.");
    }
  };

  // Función que exporta el historial de compras a un archivo Excel
  const exportarExcel = () => {
    if (compras.length === 0) {
      setMensaje("No hay compras para exportar.");
      return;
    }

    // Formatea los datos para exportarlos con encabezados claros
    const data = compras.map((compra) => ({
      "Horas compradas": compra.cantidad_horas,
      "Precio por hora (USD)": compra.valor_por_hora,
      "Total pagado (USD)": compra.total_pagado,
      "Fecha de compra": compra.fecha_compra,
    }));

    const worksheet = XLSX.utils.json_to_sheet(data); // Crea la hoja de Excel
    const workbook = XLSX.utils.book_new(); // Crea el libro
    XLSX.utils.book_append_sheet(workbook, worksheet, "Compras"); // Agrega la hoja

    const excelBuffer = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
    const blob = new Blob([excelBuffer], { type: "application/octet-stream" });

    saveAs(blob, `compras_usuario_${usuarioId}.xlsx`); // Descarga el archivo
  };

  // Renderiza el componente
  return (
    <div className="comprar-horas-container">
      <h1>Compra de Horas</h1>

      {/* Selector de usuario */}
      <div className="input-group">
        <label>Seleccionar Usuario:</label>
        <select value={usuarioId} onChange={(e) => setUsuarioId(e.target.value)}>
          <option value="">-- Selecciona un usuario --</option>
          {usuarios.map((u) => (
            <option key={u.id} value={u.id}>
              {u.username} ({u.id})
            </option>
          ))}
        </select>
      </div>

      {/* Campo: Horas a comprar */}
      <div className="input-group">
        <label>Horas a Comprar:</label>
        <input
          type="number"
          value={horas}
          onChange={(e) => setHoras(parseInt(e.target.value))}
          placeholder="Ingrese cantidad de horas"
        />
      </div>

      {/* Campo: Precio por hora en USD */}
      <div className="input-group">
        <label>Precio por Hora (USD):</label>
        <input
          type="number"
          value={precioPorHora}
          onChange={(e) => setPrecioPorHora(parseFloat(e.target.value))}
          placeholder="Ingrese el precio en dólares"
        />
      </div>

      {/* Cálculo del total en tiempo real */}
      {horas > 0 && precioPorHora > 0 && (
        <p style={{ color: "white", fontWeight: "bold", marginTop: "-10px" }}>
          Total a Pagar: ${(horas * precioPorHora).toFixed(2)} USD
        </p>
      )}

      {/* Botón para realizar la compra */}
      <button className="btn comprar" onClick={comprarHoras}>
        Comprar Horas
      </button>

      {/* Botón para consultar historial */}
      <button className="btn consultar" onClick={consultarCompras}>
        Consultar Compras
      </button>

      {/* Mostrar mensaje */}
      {mensaje && <p className="mensaje">{mensaje}</p>}

      {/* Mostrar tabla solo si hay historial */}
      {compras.length > 0 && (
      <div className="compras-lista">
        <h3>Historial de Compras</h3>
        <table>
          <thead>
            <tr>
              <th>Horas</th>
              <th>Precio/Hora (USD)</th>
              <th>Total (USD)</th>
              <th>Fecha</th>
            </tr>
          </thead>
          <tbody>
            {compras.map((compra, index) => (
              <tr key={index}>
                <td>{compra.cantidad_horas}</td>
                <td>${compra.valor_por_hora}</td>
                <td>${compra.total_pagado}</td>
                <td>{compra.fecha_compra}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <button className="btn" style={{ marginTop: "20px" }} onClick={exportarExcel}>
          Exportar a Excel
        </button>
      </div>
    )}

   
    </div>

)}
      

// Exportamos el componente para usarlo en las rutas
export default ComprarHoras;
