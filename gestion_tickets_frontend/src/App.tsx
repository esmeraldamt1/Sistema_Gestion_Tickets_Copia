// Importa React, necesario para usar JSX
import React from "react";

// Importa componentes de enrutamiento desde react-router-dom
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

// Importa los componentes de las diferentes páginas de la aplicación
import Login from "./pages/Login";
import Panel from "./pages/Panel";
import Tickets from "./pages/Tickets";
import Ayuda from "./pages/Ayuda";
import Reportes from "./pages/Reportes";
import Saldo from "./pages/Saldo";
import ComprarHoras from "./pages/ComprarHoras";
import Register from "./pages/Register";
import ResetPassword from "./pages/ResetPassword";
import ForgotPassword from "./pages/ForgotPassword"; // 👈 Se mantiene el componente, aunque la ruta cambiará

// Importa los estilos globales de la aplicación
import "./Styles/App.css";
import "./Styles/ResetPassword.css";

// ✅ Función que verifica si el usuario está autenticado
const isAuthenticated = () => {
  // Retorna true si existe un token en el localStorage, false si no
  return localStorage.getItem("token") !== null;
};

// ✅ Componente para proteger rutas que requieren autenticación
const ProtectedRoute: React.FC<{ element: JSX.Element }> = ({ element }) => {
  // Si el usuario está autenticado, muestra el componente solicitado
  // Si no lo está, redirige a la página de login (ruta "/")
  return isAuthenticated() ? element : <Navigate to="/" />;
};

// ✅ Componente principal de la aplicación que contiene las rutas
const App: React.FC = () => {
  return (
    // Usa el enrutador de React Router para manejar navegación
    <Router>
      {/* Define las diferentes rutas de la aplicación */}
      <Routes>
        {/* Ruta pública para el login */}
        <Route path="/" element={<Login />} />

        {/* Rutas protegidas, requieren autenticación */}
        <Route path="/panel" element={<ProtectedRoute element={<Panel />} />} />
        <Route path="/tickets" element={<ProtectedRoute element={<Tickets />} />} />
        <Route path="/ayuda" element={<ProtectedRoute element={<Ayuda />} />} />
        <Route path="/reportes" element={<ProtectedRoute element={<Reportes />} />} />
        <Route path="/saldo" element={<ProtectedRoute element={<Saldo />} />} />
        <Route path="/comprar-horas" element={<ProtectedRoute element={<ComprarHoras />} />} />

        {/* Rutas públicas para registro y recuperación de contraseña */}
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:token" element={<ResetPassword />} />
      </Routes>
    </Router>
  );
};

// Exporta el componente App para que pueda ser usado en otros archivos
export default App;
