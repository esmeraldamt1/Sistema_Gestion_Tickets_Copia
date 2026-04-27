// Reportes.tsx con estilos actualizados y comentados

// Importamos hooks y componentes necesarios
import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableCell,
} from "@/components/ui/table";
import { Download } from "lucide-react";
import "@/styles/Reportes.css"; // Importamos los estilos para este componente
import { obtenerUsuarios } from "../services/api"; // Función que trae los usuarios desde la API

// Interfaces para tipar los datos
interface Ticket {
  id: string;
  asunto: string;
  descripcion: string;
  estado: string;
  tipo: string;
  prioridad: string;
  solicitante: string;
  asignado: string;
  departamento: string;
  fecha_creacion: string;
}

interface Usuario {
  id: string;
  username: string;
  rol: string;
}

// Componente principal para los reportes de tickets
export default function ReporteTickets() {
  // Estados para los filtros y datos cargados
  const [estado, setEstado] = useState(""); // Filtro por estado del ticket
  const [asignado, setAsignado] = useState(""); // Filtro por usuario asignado
  const [solicitante, setSolicitante] = useState(""); // Filtro por usuario solicitante
  const [tickets, setTickets] = useState<Ticket[]>([]); // Tickets obtenidos del backend
  const [usuarios, setUsuarios] = useState<Usuario[]>([]); // Lista de usuarios disponibles
  const [filtroAplicado, setFiltroAplicado] = useState(false); // Estado para saber si ya se aplicó el filtro

  // Cargar lista de usuarios al montar componente
  useEffect(() => {
    const cargarUsuarios = async () => {
      try {
        const res = await obtenerUsuarios(); // Obtenemos los usuarios desde la API
        setUsuarios(res); // Guardamos los usuarios en el estado
      } catch (error) {
        console.error("Error al cargar usuarios", error);
      }
    };
    cargarUsuarios(); // Ejecutamos la función una vez al cargar el componente
  }, []);

  // Función para consultar tickets filtrados
  const fetchReportes = async () => {
    try {
      let queryParams = new URLSearchParams(); // Construimos los parámetros de la URL
      if (estado) queryParams.append("estado", estado);
      if (asignado) queryParams.append("asignado", asignado);
      if (solicitante) queryParams.append("solicitante", solicitante);

      const response = await fetch(
        `http://localhost:8000/reportes/tickets/?${queryParams.toString()}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      const data = await response.json(); // Obtenemos los datos de la respuesta
      setFiltroAplicado(true); // Indicamos que ya se aplicó el filtro

      if (response.ok) {
        setTickets(data.tickets); // Si la respuesta fue exitosa, guardamos los tickets
      } else {
        setTickets([]); // Si no, dejamos la lista vacía
      }
    } catch (error) {
      console.error("Error al obtener reportes", error);
    }
  };

  // Exporta tickets a archivo Excel
  const descargarExcel = async () => {
    try {
      const queryParams = new URLSearchParams();
      if (estado) queryParams.append("estado", estado);
      if (asignado) queryParams.append("asignado", asignado);
      if (solicitante) queryParams.append("solicitante", solicitante);

      const token = localStorage.getItem("token");
      const response = await fetch(
        `http://localhost:8000/reportes/tickets/exportar/?${queryParams.toString()}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) throw new Error("Error al descargar el reporte");
      const blob = await response.blob(); // Convertimos la respuesta a archivo
      const url = window.URL.createObjectURL(blob); // Creamos una URL temporal para el archivo
      const a = document.createElement("a");
      a.href = url;
      a.download = "reporte_tickets.xlsx"; // Nombre del archivo descargado
      a.click();
      window.URL.revokeObjectURL(url); // Liberamos la URL del archivo
    } catch (error) {
      console.error("Error al exportar el reporte:", error);
    }
  };

  // Separar usuarios por rol para selects
  const agentes = usuarios.filter((u) => u.rol === "agente"); // Solo usuarios con rol agente
  const solicitantes = usuarios.filter((u) => u.rol === "solicitante"); // Solo usuarios solicitantes

  return (
    <div className="container">
      <div className="content">
        <h1 className="title">Reportes de Tickets</h1>

        {/* Sección de filtros */}
        <div className="filter-section">
          {/* Campo de filtro por estado */}
          <Input
            placeholder="Estado"
            value={estado}
            onChange={(e) => setEstado(e.target.value)}
            className="input-field"
          />

          {/* Selector de usuario asignado */}
          <select
            className="input-field"
            value={asignado}
            onChange={(e) => setAsignado(e.target.value)}
          >
            <option value="">-- Asignado --</option>
            {agentes.map((u) => (
              <option key={u.id} value={u.id}>
                {u.username} ({u.id})
              </option>
            ))}
          </select>

          {/* Selector de usuario solicitante */}
          <select
            className="input-field"
            value={solicitante}
            onChange={(e) => setSolicitante(e.target.value)}
          >
            <option value="">-- Solicitante --</option>
            {solicitantes.map((u) => (
              <option key={u.id} value={u.id}>
                {u.username} ({u.id})
              </option>
            ))}
          </select>
        </div>

        {/* Sección de botones */}
        <div className="button-section">
          {/* Botón para aplicar filtros */}
          <Button onClick={fetchReportes} className="filter-button">
            Filtrar
          </Button>
          {/* Botón para exportar resultados a Excel */}
          <Button onClick={descargarExcel} className="export-button">
            <Download className="icon" size={14} /> Exportar Excel
          </Button>
        </div>

        {/* Tabla con resultados del filtro */}
        {filtroAplicado && (
          <Table className="table">
            <TableHeader>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Asunto</TableCell>
                <TableCell>Descripción</TableCell>
                <TableCell>Estado</TableCell>
                <TableCell>Tipo</TableCell>
                <TableCell>Prioridad</TableCell>
                <TableCell>Solicitante</TableCell>
                <TableCell>Asignado</TableCell>
                <TableCell>Departamento</TableCell>
                <TableCell>Fecha de creación</TableCell>
              </TableRow>
            </TableHeader>
            <TableBody>
              {tickets.length > 0 ? (
                tickets.map((ticket) => (
                  <TableRow key={ticket.id}>
                    <TableCell>{ticket.id}</TableCell>
                    <TableCell>{ticket.asunto}</TableCell>
                    <TableCell>{ticket.descripcion}</TableCell>
                    <TableCell>{ticket.estado}</TableCell>
                    <TableCell>{ticket.tipo}</TableCell>
                    <TableCell>{ticket.prioridad}</TableCell>
                    <TableCell>{ticket.solicitante}</TableCell>
                    <TableCell>{ticket.asignado}</TableCell>
                    <TableCell>{ticket.departamento}</TableCell>
                    <TableCell>{ticket.fecha_creacion}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={10} className="no-data">
                    No hay reportes disponibles
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
