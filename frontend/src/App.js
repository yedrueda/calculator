import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Planner from './components/MRP/Planner';
import Inventory from './components/MRP/Inventory';
import './App.css';

function App() {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const cargarDatosIniciales = async () => {
      try {
        const response = await axios.get('/api/productos');
        setProductos(response.data);
        setLoading(false);
      } catch (err) {
        setError('Error cargando los productos');
        setLoading(false);
        console.error('Error:', err);
      }
    };

    cargarDatosIniciales();
  }, []);

  if (loading) {
    return <div className="loading-container">Cargando sistema MRP...</div>;
  }

  if (error) {
    return <div className="error-container">{error}</div>;
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>Sistema de Planificación de Materiales (MRP)</h1>
      </header>
      
      <main className="main-container">
        <section className="planner-section">
          <h2>Planificador de Producción</h2>
          <Planner productos={productos} />
        </section>
        
        <section className="inventory-section">
          <h2>Gestión de Inventario</h2>
          <Inventory />
        </section>
      </main>
    </div>
  );
}

export default App;