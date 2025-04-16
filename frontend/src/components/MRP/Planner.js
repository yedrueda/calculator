import React, { useState } from 'react';
import axios from 'axios';

const Planner = ({ productos }) => {
    const [ordenes, setOrdenes] = useState([]);
    const [plan, setPlan] = useState(null);

    const handlePlanificar = async () => {
        try {
            const response = await axios.post('http://localhost:5000/api/mrp/planificar', {
                ordenes: ordenes.filter(o => o.producto_id && o.cantidad > 0)
            });
            setPlan(response.data);
        } catch (error) {
            console.error('Error al planificar:', error);
        }
    };

    return (
        <div className="mrp-planner">
            <h2>Planificador MRP</h2>
            
            <div className="ordenes-section">
                {ordenes.map((orden, index) => (
                    <div key={index} className="orden-item">
                        <select
                            value={orden.producto_id}
                            onChange={(e) => {
                                const nuevas = [...ordenes];
                                nuevas[index].producto_id = e.target.value;
                                setOrdenes(nuevas);
                            }}
                        >
                            <option value="">Seleccionar Producto</option>
                            {productos.map(p => (
                                <option key={p.id} value={p.id}>{p.nombre}</option>
                            ))}
                        </select>
                        <input
                            type="number"
                            min="1"
                            value={orden.cantidad || 1}
                            onChange={(e) => {
                                const nuevas = [...ordenes];
                                nuevas[index].cantidad = parseInt(e.target.value);
                                setOrdenes(nuevas);
                            }}
                        />
                    </div>
                ))}
                <button onClick={() => setOrdenes([...ordenes, {}])}>
                    + Agregar Orden
                </button>
            </div>

            <button onClick={handlePlanificar}>Generar Plan MRP</button>

            {plan && (
                <div className="resultados-mrp">
                    <h3>Resultados de Planificación</h3>
                    <div className="requerimientos">
                        <h4>Materiales Requeridos:</h4>
                        <ul>
                            {Object.entries(plan.requerimientos).map(([id, cantidad]) => (
                                <li key={id}>Material {id}: {cantidad} unidades</li>
                            ))}
                        </ul>
                    </div>
                    
                    <div className="pedidos-sugeridos">
                        <h4>Pedidos Sugeridos:</h4>
                        {plan.pedidos_sugeridos.map((pedido, idx) => (
                            <div key={idx} className="pedido-card">
                                <p>Material ID: {pedido.material_id}</p>
                                <p>Cantidad a Pedir: {pedido.cantidad}</p>
                                <p>Stock Actual: {pedido.stock_actual}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Planner;