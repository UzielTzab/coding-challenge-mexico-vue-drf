import api from './http';

export const getTrades = async (params?: any) => {
  const { data } = await api.get('/api/trades', { params });
  return data;
};
