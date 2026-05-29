import api from './http';

export const getLogs = async () => {
  const { data } = await api.get('/logs');
  return data;
};
