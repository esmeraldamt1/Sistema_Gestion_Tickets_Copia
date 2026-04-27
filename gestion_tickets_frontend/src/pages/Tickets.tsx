// Importamos React y hooks necesarios
import React, { useState, useEffect, useRef } from "react";

// Importamos funciones del API necesarias
import {
  obtenerUsuarios,
  obtenerDepartamentos,
  crearTicket,
} from "../services/api";

// Importamos los estilos CSS
import "../Styles/Tickets.css";

// Interfaz para los usuarios
interface Usuario {
  id: string;
  username: string;
  rol: string;
}

// Interfaz para los departamentos
interface Departamento {
  id: string;
  nombre: string;
}

// Interfaz para el estado del formulario
interface FormDataType {
  asignado: string;
  solicitante: string;
  departamento: string;
  fecha_creacion: string;
  asunto: string;
  descripcion: string;
  tipo_ticket: string;
  estado_ticket: string;
  prioridad: string;
  fecha_resolucion: string;
  archivo: File | null;
}

// Componente funcional principal
const Tickets: React.FC = () => {
  // Estado para los usuarios
  const [agentes, setAgentes] = useState<Usuario[]>([]);
  const [solicitantes, setSolicitantes] = useState<Usuario[]>([]);

  // Estado para los departamentos
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);

  // Mensaje para mostrar al usuario
  const [mensaje, setMensaje] = useState<string | null>(null);

  // Referencia para limpiar el input de archivo
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Estado del formulario
  const [formData, setFormData] = useState<FormDataType>({
    asignado: "",
    solicitante: "",
    departamento: "",
    fecha_creacion: "",
    asunto: "",
    descripcion: "",
    tipo_ticket: "",
    estado_ticket: "",
    prioridad: "",
    fecha_resolucion: "",
    archivo: null,
  });

  // Cargar usuarios y departamentos al montar el componente
  useEffect(() => {
    obtenerUsuarios()
      .then((res) => {
        console.log("Usuarios recibidos:", res);
        setAgentes(res.filter((u: Usuario) => u.rol === "agente"));
        setSolicitantes(res.filter((u: Usuario) => u.rol === "solicitante"));
      })
      .catch((e) => console.error("Error al cargar usuarios:", e));

    obtenerDepartamentos()
      .then(setDepartamentos)
      .catch((e) => console.error("Error al cargar departamentos:", e));
  }, []);

  // Manejo de cambios en inputs del formulario
  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Manejo del cambio de archivo
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, archivo: e.target.files?.[0] ?? null });
  };

  // Envío del formulario
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMensaje(null);

    // Validación de campos obligatorios
    if (!formData.solicitante || !formData.asignado || !formData.departamento) {
      setMensaje("Todos los campos deben estar seleccionados");
      return;
    }

    // Construcción del FormData para multipart/form-data
    const formDataToSend = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (value !== null && value !== "") {
        if (key === "archivo" && value instanceof File) {
          formDataToSend.append(key, value);
        } else {
          formDataToSend.append(key, value as string);
        }
      }
    });

    // Agregar prioridad por defecto si no se selecciona
    if (!formData.prioridad) {
      formDataToSend.append("prioridad", "Media");
    }

    try {
      // Enviar el ticket al backend
      await crearTicket(formDataToSend);
      setMensaje("Ticket creado con éxito");

      // Limpiar el estado del formulario
      setFormData({
        asignado: "",
        solicitante: "",
        departamento: "",
        fecha_creacion: "",
        asunto: "",
        descripcion: "",
        tipo_ticket: "",
        estado_ticket: "",
        prioridad: "",
        fecha_resolucion: "",
        archivo: null,
      });

      // Limpiar el input de archivo
      if (fileInputRef.current) fileInputRef.current.value = "";
    } catch (error: any) {
      // Mostrar el error en consola para depuración
      console.log("Error al enviar el ticket:", error);

      // Mostrar mensaje amigable al usuario
      setMensaje(
        error.response?.data?.error ||
        error.response?.data?.detail ||
        "Error de conexión con el servidor."
      );
    }
  };

  // Renderizado del formulario
  return (
    <div className="ticket-container">
      <h2>Creación De Tickets</h2>
      {mensaje && <p className="mensaje">{mensaje}</p>}

      <form className="ticket-form" onSubmit={handleSubmit}>
        {/* Asignado y Solicitante */}
        <div className="form-row">
          <div className="input-group">
            <label>Asignado a:</label>
            <select name="asignado" value={formData.asignado} onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              {agentes.map((user) => (
                <option key={user.id} value={user.id}>{user.username}</option>
              ))}
            </select>
          </div>

          <div className="input-group">
            <label>Solicitante:</label>
            <select name="solicitante" value={formData.solicitante} onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              {solicitantes.map((user) => (
                <option key={user.id} value={user.id}>{user.username}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Departamento y Fecha */}
        <div className="form-row">
          <div className="input-group">
            <label>Departamento:</label>
            <select name="departamento" value={formData.departamento} onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              {departamentos.map((dep) => (
                <option key={dep.id} value={dep.id}>{dep.nombre}</option>
              ))}
            </select>
          </div>

          <div className="input-group">
            <label>Fecha de Creación:</label>
            <input type="date" name="fecha_creacion" value={formData.fecha_creacion} onChange={handleChange} required />
          </div>
        </div>

        {/* Asunto y Descripción */}
        <div className="input-group">
          <label>Asunto:</label>
          <input type="text" name="asunto" value={formData.asunto} onChange={handleChange} required />
        </div>

        <div className="input-group">
          <label>Descripción:</label>
          <textarea name="descripcion" value={formData.descripcion} onChange={handleChange} required />
        </div>

        {/* Tipo y Estado */}
        <div className="form-row">
          <div className="input-group">
            <label>Tipo de Ticket:</label>
            <select name="tipo_ticket" value={formData.tipo_ticket} onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              <option value="Problema">Problema</option>
              <option value="Solicitud de servicio">Solicitud de servicio</option>
              <option value="Consulta">Consulta</option>
              <option value="Incidente">Incidente</option>
            </select>
          </div>

          <div className="input-group">
            <label>Estado del Ticket:</label>
            <select name="estado_ticket" value={formData.estado_ticket} onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              <option value="Abierto">Abierto</option>
              <option value="En proceso">En proceso</option>
              <option value="Cerrado">Cerrado</option>
            </select>
          </div>
        </div>

        {/* Prioridad */}
        <div className="input-group">
          <label>Prioridad:</label>
          <select name="prioridad" value={formData.prioridad} onChange={handleChange}>
            <option value="">Selecciona una prioridad</option>
            <option value="Urgente">Urgente</option>
            <option value="Alta">Alta</option>
            <option value="Media">Media</option>
            <option value="Baja">Baja</option>
          </select>
        </div>

        {/* Adjuntar archivo */}
        <div className="input-group">
          <label>Adjuntar Archivo:</label>
          <input type="file" name="archivo" ref={fileInputRef} onChange={handleFileChange} accept="image/*,application/pdf" />
        </div>

        {/* Fecha de resolución */}
        <div className="input-group">
          <label>Fecha de Resolución:</label>
          <input type="date" name="fecha_resolucion" value={formData.fecha_resolucion} onChange={handleChange} />
        </div>

        {/* Botón para crear */}
        <button type="submit" className="btn-crear">
          Crear Ticket
        </button>
      </form>
    </div>
  );
};

// Exportamos el componente
export default Tickets;
