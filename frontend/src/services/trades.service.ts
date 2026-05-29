import api from './http';

export const getTrades = async () => {
  const { data } = await api.get('/trades');
  return data;
};
