import api from './http';

export const getTrades = async (params: Record<string, any> = {}) => {
  const { data } = await api.get('/api/trading/simulated-trades/', { params });
  return data;
};
