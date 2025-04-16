import React, { useState, useEffect } from 'react';
import { getInventario, getMateriales, updateInventario } from '../../services/api';
import './Inventory.css';

const Inventory = () => {
  const [inventario, setInventario] = useState([]);
  const [materiales, setMateriales] = useState([]);
  const [editando, setEditando] = useState(null);
  const [formData, setFormData] = useState({
    stock: '',
    stock_minimo: ''
  });

  useEffect(() => {
    const cargarDatos = async () => {
      try {
        const [invResponse, matResponse] = await Promise.all([
          getInventario(),
          getMateriales()
        ]);
        
        setInventario(invResponse.data);
        setMateriales(matResponse.data);
      } catch (error) {
        console.error('Error cargando datos:', error);
      }
    };
    
    cargarDatos();
  }, []);

  const handleEditar = (item) => {
    setEditando(item.material_id);
    setFormData({
      stock: item.stock,
      stock_minimo: item.stock_minimo
    });
  };

  const handleActualizar = async () => {
    try {
      const response = await updateInventario(editando, formData);
      
      setInventario(inventario.map(item => 
        item.material_id === editando ? response.data.inventario : item
      ));
      
      setEditando(null);
    } catch (error) {
      console.error('Error actualizando inventario:', error);
    }
  };

  return (
    <div className="inventario-container">
      <h2>Gestión de Inventario</h2>
      
      <table className="inventario-table">
        <thead>
          <tr>
            <th>Material</th>
            <th>Unidad</th>
            <th>Stock Actual</th>
            <th>Stock Mínimo</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {inventario.map(item => {
            const material = materiales.find(m => m.id === item.material_id);
            
            return (
              <tr key={item.material_id} 
                  className={item.stock < item.stock_minimo ? 'stock-bajo' : ''}>
                <td>{material?.nombre || 'N/A'}</td>
                <td>{material?.unidad || '-'}</td>
                
                {editando === item.material_id ? (
                  <>
                    <td>
                      <input
                        type="number"
                        value={formData.stock}
                        onChange={(e) => setFormData({...formData, stock: e.target.value})}
                        min="0"
                        step="0.01"
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        value={formData.stock_minimo}
                        onChange={(e) => setFormData({...formData, stock_minimo: e.target.value})}
                        min="0"
                        step="0.01"
                      />
                    </td>
                    <td>
                      <button className="btn-guardar" onClick={handleActualizar}>✓</button>
                      <button className="btn-cancelar" onClick={() => setEditando(null)}>✗</button>
                    </td>
                  </>
                ) : (
                  <>
                    <td>{item.stock}</td>
                    <td>{item.stock_minimo}</td>
                    <td>
                      <button className="btn-editar" onClick={() => handleEditar(item)}>
                        Editar
                      </button>
                    </td>
                  </>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default Inventory;