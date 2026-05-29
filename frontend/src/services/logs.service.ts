import api from './http';

export const getLogs = async () => {
  const { data } = await api.get('/api/logs/');
  return data;
};
