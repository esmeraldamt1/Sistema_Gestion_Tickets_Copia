// Importamos hooks de React
import { useEffect, useState } from "react";

// Importamos funciones del servicio API
import {
  consultarSaldo,
  actualizarSaldo,
  obtenerMovimientosSaldo,
  obtenerUsuarios,
} from "../services/api";

// Importamos estilos del componente
import "../styles/Saldo.css";

// Importamos librerías para exportar a Excel
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

// ─────────────────────────────────────
// Interfaces
// ─────────────────────────────────────

// Interfaz para representar un usuario
interface Usuario {
  id: string;         // ID de MongoDB
  username: string;    // Nombre visible
  email: string;       // Correo del usuario
}

// Interfaz para representar un movimiento de saldo
interface Movimiento {
  id: string;          // ID del movimiento
  cambio: number;      // Monto del cambio (positivo o negativo)
  descripcion: string; // Texto opcional
  fecha: string;       // Fecha del movimiento
}

// ─────────────────────────────────────
// Componente principal
// ─────────────────────────────────────

const Saldo = () => {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [usuarioId, setUsuarioId] = useState<string>("");
  const [saldo, setSaldo] = useState<number | null>(null);
  const [cambioSaldo, setCambioSaldo] = useState<number>(0);
  const [mensaje, setMensaje] = useState<string>("");
  const [movimientos, setMovimientos] = useState<Movimiento[]>([]);

  // Cargar lista de usuarios
  useEffect(() => {
    const cargarUsuarios = async () => {
      try {
        const res = await obtenerUsuarios();
        setUsuarios(res);
      } catch (error) {
        setMensaje("Error al cargar usuarios.");
      }
    };
    cargarUsuarios();
  }, []);

  // Consultar saldo y movimientos al seleccionar usuario
  useEffect(() => {
    if (usuarioId) {
      handleConsultarSaldo();
    }
  }, [usuarioId]);

  // Consulta saldo y movimientos del usuario
  const handleConsultarSaldo = async () => {
    if (!usuarioId) return;
    try {
      const saldoRes = await consultarSaldo(usuarioId);
      setSaldo(saldoRes.saldo_actual);

      const movimientosRes = await obtenerMovimientosSaldo(usuarioId);
      setMovimientos(movimientosRes.movimientos);

      setMensaje("");
    } catch (error: any) {
      setMensaje(error.response?.data?.error || "Error al consultar saldo.");
    }
  };

  // Actualiza el saldo del usuario
  const handleActualizarSaldo = async () => {
    if (!usuarioId || cambioSaldo === 0) {
      setMensaje("Seleccione un usuario y un monto válido.");
      return;
    }
    try {
      const res = await actualizarSaldo(usuarioId, cambioSaldo);
      setSaldo(res.nuevo_saldo);
      setMensaje("Saldo actualizado correctamente.");
      setCambioSaldo(0);
      const movimientosRes = await obtenerMovimientosSaldo(usuarioId);
      setMovimientos(movimientosRes.movimientos);
    } catch (error: any) {
      setMensaje(error.response?.data?.error || "Error al actualizar saldo.");
    }
  };

  // Exporta movimientos a Excel
  const exportarExcel = () => {
    if (movimientos.length === 0) {
      setMensaje("No hay movimientos para exportar.");
      return;
    }
    const data = movimientos.map((mov) => ({
      "Cambio": mov.cambio,
      "Fecha": new Date(mov.fecha).toLocaleString(),
    }));
    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Movimientos");
    const excelBuffer = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
    const blob = new Blob([excelBuffer], { type: "application/octet-stream" });
    saveAs(blob, `movimientos_saldo_${usuarioId}.xlsx`);
  };

  // Renderizado
  return (
    <div className="saldo-container">
      <h2>Gestión de Saldo</h2>

      <div className="input-group">
        <label>Seleccionar Usuario:</label>
        <select
          value={usuarioId}
          onChange={(e) => setUsuarioId(e.target.value)}
        >
          <option value="">-- Selecciona un usuario --</option>
          {usuarios.map((u) => (
            <option key={u.id} value={u.id}>
              {u.username} ({u.id})
            </option>
          ))}
        </select>
      </div>

      {saldo !== null && <p style={{ color: "white" }}>Saldo Actual: ${saldo}</p>}

      <div className="input-group">
        <label>Cambio de Saldo:</label>
        <input
          type="number"
          value={cambioSaldo}
          onChange={(e) => setCambioSaldo(parseFloat(e.target.value))}
          placeholder="Ingrese el monto a modificar"
        />
      </div>

      <button className="btn actualizar" onClick={handleActualizarSaldo}>
        Actualizar Saldo
      </button>

      {mensaje && <p className="mensaje">{mensaje}</p>}

      {movimientos.length > 0 && (
        <div className="tabla-movimientos">
          <h3 className="titulo-historial">Historial de Movimientos</h3>
          <table>
            <thead>
              <tr>
                <th>Cambio</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {movimientos.map((mov) => (
                <tr key={mov.id}>
                  <td>{mov.cambio > 0 ? `+${mov.cambio}` : mov.cambio}</td>
                  <td>{new Date(mov.fecha).toLocaleString()}</td>
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
  );
};

export default Saldo;
