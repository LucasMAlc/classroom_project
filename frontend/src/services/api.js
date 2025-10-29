import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const login = (username, password) => api.post('/token/', { username, password });
export const getMeusDados = () => api.get('/meus-dados/');
export const getMinhasTurmas = () => api.get('/minhas-turmas/');
export const getTreinamentos = () => api.get('/treinamentos/');
export const createTreinamento = (data) => api.post('/treinamentos/', data);
export const updateTreinamento = (id, data) => api.put(`/treinamentos/${id}/`, data);
export const deleteTreinamento = (id) => api.delete(`/treinamentos/${id}/`);
export const getTurmas = () => api.get('/turmas/');
export const createTurma = (data) => api.post('/turmas/', data);
export const updateTurma = (id, data) => api.put(`/turmas/${id}/`, data);
export const deleteTurma = (id) => api.delete(`/turmas/${id}/`);
export const getRecursos = (turmaId = null) => {
  const url = turmaId ? `/recursos/?turma=${turmaId}` : '/recursos/';
  return api.get(url);
};
export const createRecurso = (data) => api.post('/recursos/', data);
export const updateRecurso = (id, data) => api.put(`/recursos/${id}/`, data);
export const deleteRecurso = (id) => api.delete(`/recursos/${id}/`);
export const getAlunos = () => api.get('/alunos/');
export const getMatriculas = () => api.get('/matriculas/');
export const createMatricula = (data) => api.post('/matriculas/', data);
export const deleteMatricula = (id) => api.delete(`/matriculas/${id}/`);

export default api;