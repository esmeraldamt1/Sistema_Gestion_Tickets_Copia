import { useState } from "react";
import { FaChevronLeft, FaEnvelope, FaPhone, FaFilePdf, FaWhatsapp } from "react-icons/fa";
import "../styles/ayuda.css";

export default function Ayuda() {
  const [preguntaSeleccionada, setPreguntaSeleccionada] = useState("");

  const preguntasRespuestas = [
    { pregunta: "¿Cómo restablecer mi contraseña?", respuesta: "Para restablecer tu contraseña, ve a la página de inicio de sesión y haz clic en '¿Olvidaste tu contraseña?'. Sigue los pasos para recibir un correo con las instrucciones." },
    { pregunta: "¿Dónde puedo ver mis tickets abiertos?", respuesta: "Puedes ver tus tickets abiertos en la sección 'Mis Tickets' en el panel de navegación. Allí encontrarás el estado de cada solicitud." },
    { pregunta: "¿Cómo solicitar asistencia remota?", respuesta: "Para solicitar asistencia remota, haz clic en el botón 'Asistencia Remota'. Un agente de soporte se pondrá en contacto contigo." }
  ];

  const respuestaSeleccionada = preguntasRespuestas.find(p => p.pregunta === preguntaSeleccionada)?.respuesta || "";

  const abrirTeamViewer = () => {
    const teamViewerURL = "teamviewer10://control?device=YOUR_TEAMVIEWER_ID";
    const teamViewerDownloadURL = "https://www.teamviewer.com/es/descarga/";
    
    window.location.href = teamViewerURL;
    setTimeout(() => {
      window.open(teamViewerDownloadURL, "_blank");
    }, 3000);
  };

  return (
    <div className="ayuda-container">
      <div className="ayuda-content">
        <h1 className="ayuda-title">Ayuda y Soporte</h1>

        <label className="ayuda-label">Preguntas Frecuentes *</label>
        <select
          className="ayuda-select"
          value={preguntaSeleccionada}
          onChange={(e) => setPreguntaSeleccionada(e.target.value)}
        >
          <option value="">Seleccione una pregunta</option>
          {preguntasRespuestas.map((item, index) => (
            <option key={index} value={item.pregunta}>{item.pregunta}</option>
          ))}
        </select>

        {respuestaSeleccionada && (
          <p className="ayuda-respuesta">{respuestaSeleccionada}</p>
        )}

        <button className="ayuda-button" onClick={abrirTeamViewer}>Asistencia Remota</button>

        <div className="ayuda-icons">
          <a href="/panel" className="ayuda-icon-button ayuda-icon-back">
            <FaChevronLeft size={20} />
          </a>
          <a href="https://mail.google.com/mail/?view=cm&fs=1&to=saefdesarrolladores@gmail.com"
          target="_blank"
          rel="noopener noreferrer"
          className="ayuda-icon-button ayuda-icon-email">
          <FaEnvelope size={20} />
          </a>
          <a href="tel:+3182742912" className="ayuda-icon-button ayuda-icon-phone">
            <FaPhone size={20} />
          </a>
                    
          <a href="/documentos/manual.pdf" target="_blank" className="ayuda-icon-button ayuda-icon-pdf">
            <FaFilePdf size={20} />
          </a>
          <a href="https://wa.me/573182742912"  // Número real con código de país (57 para Colombia)
            target="_blank"
            rel="noopener noreferrer"  // Por seguridad
            className="ayuda-icon-button ayuda-icon-chat">
            <FaWhatsapp size={20} />
          </a>
        </div>
      </div>
      </div>
   );
}
