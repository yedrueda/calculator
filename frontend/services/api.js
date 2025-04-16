import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'development' 
    ? 'http://localhost:5000/api' 
    : '/api'
});

// Inventario
export const getInventario = () => api.get('/inventario');
export const updateInventario = (id, data) => api.put(`/inventario/${id}`, data);

// Materiales
export const getMateriales = () => api.get('/materiales');

// Órdenes de Producción
export const createOrdenProduccion = (data) => api.post('/ordenes-produccion', data);
export const getOrdenesProduccion = () => api.get('/ordenes-produccion');

export default api;