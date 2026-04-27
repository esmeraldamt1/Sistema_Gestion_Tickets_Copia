//  Importamos axios para realizar peticiones HTTP al backend
import axios from "axios";

// Definimos la URL base del backend
const API_BASE = "http://localhost:8000";

// Función auxiliar que devuelve los headers con token de autenticación
const authHeaders = () => {
  const token = localStorage.getItem("token"); //  Tomamos el token almacenado en localStorage
  return token ? { Authorization: `Bearer ${token}` } : {}; //  Si hay token, lo agregamos al header
};

// ─────────────────────────────────────
//  USUARIOS
// ─────────────────────────────────────

// 👤 Obtener todos los usuarios (con token de autenticación)
export const obtenerUsuarios = async () => {
  const res = await axios.get(`${API_BASE}/usuarios/`, {
    headers: authHeaders(), //  Incluimos token
  });
  return res.data;
};

// Filtrar usuarios con rol "agente"
export const obtenerAgentes = async () => {
  const res = await obtenerUsuarios(); //  Usamos la función general
  return res.filter((u: any) => u.rol === "agente");
};

// Filtrar usuarios con rol "solicitante"
export const obtenerSolicitantes = async () => {
  const res = await obtenerUsuarios();
  return res.filter((u: any) => u.rol === "solicitante");
};

// ─────────────────────────────────────
//  DEPARTAMENTOS
// ─────────────────────────────────────

//  Obtener todos los departamentos
export const obtenerDepartamentos = async () => {
  const res = await axios.get(`${API_BASE}/departamentos/`, {
    headers: authHeaders(), //  Incluimos token
  });
  return res.data;
};

// ─────────────────────────────────────
//  TICKETS
// ─────────────────────────────────────

//  Crear un nuevo ticket usando multipart/form-data
export const crearTicket = async (formData: FormData) => {
  const res = await axios.post(`${API_BASE}/tickets/`, formData, {
    headers: {
      ...authHeaders(), //  Token
      "Content-Type": "multipart/form-data", // Para archivos
    },
  });
  return res.data;
};

//  Obtener todos los tickets
export const obtenerTickets = async () => {
  const res = await axios.get(`${API_BASE}/tickets/`, {
    headers: authHeaders(), //  Incluimos token
  });
  return res.data;
};

//  Actualizar un ticket existente por ID
export const actualizarTicket = async (ticketId: string, data: any) => {
  const res = await axios.put(`${API_BASE}/tickets/${ticketId}/`, data, {
    headers: authHeaders(), // Incluimos token
  });
  return res.data;
};

//  Eliminar un ticket por ID
export const eliminarTicket = async (ticketId: string) => {
  const res = await axios.delete(`${API_BASE}/tickets/${ticketId}/`, {
    headers: authHeaders(), //  Incluimos token
  });
  return res.data;
};

// Asignar automáticamente tickets sin asignar
export const asignacionAutomatica = async () => {
  const res = await axios.post(`${API_BASE}/tickets/asignacion_automatica/`, null, {
    headers: authHeaders(), // Incluimos token
  });
  return res.data;
};

// 👤 Asignar un usuario específico a un ticket
export const asignarUsuarioATicket = async (ticketId: string, userId: string) => {
  const res = await axios.post(
    `${API_BASE}/tickets/${ticketId}/asignar_usuario/`,
    { asignado: userId },
    { headers: authHeaders() } // Incluimos token
  );
  return res.data;
};

// ─────────────────────────────────────
//  REPORTES
// ─────────────────────────────────────

//  Obtener reportes disponibles
export const obtenerReportes = async () => {
  const res = await axios.get(`${API_BASE}/reportes/`, {
    headers: authHeaders(), // Incluimos token
  });
  return res.data;
};

// ─────────────────────────────────────
//  COMPRAR HORAS
// ─────────────────────────────────────

//  Comprar una cierta cantidad de horas
export const comprarHoras = async (cantidad: number) => {
  const res = await axios.post(`${API_BASE}/comprar-horas/`, { cantidad }, {
    headers: authHeaders(), // Incluimos token
  });
  return res.data;
};

//  Obtener el historial de compras de horas
export const obtenerHistorialCompras = async () => {
  const res = await axios.get(`${API_BASE}/comprar-horas/historial/`, {
    headers: authHeaders(), //  Incluimos token
  });
  return res.data;
};

// ─────────────────────────────────────
//  SALDO
// ─────────────────────────────────────

//  Consultar el saldo de un usuario por ID
export const consultarSaldo = async (usuarioId: string) => {
  const res = await axios.get(`${API_BASE}/saldo/consultar/${usuarioId}/`, {
    headers: authHeaders(), //  Incluimos token
  });
  return res.data;
};

//  Actualizar (sumar/restar) saldo del usuario
export const actualizarSaldo = async (usuarioId: string, cambio_saldo: number, descripcion: string = "") => {
  const res = await axios.post(
    `${API_BASE}/saldo/actualizar/${usuarioId}/`,
    { cambio_saldo, descripcion },
    { headers: authHeaders() } // Incluimos token
  );
  return res.data;
};

//  Obtener historial de movimientos del saldo del usuario
export const obtenerMovimientosSaldo = async (usuarioId: string) => {
  const res = await axios.get(`${API_BASE}/saldo/movimientos/${usuarioId}/`, {
    headers: authHeaders(), //  Incluimos token
  });
  return res.data;
};
