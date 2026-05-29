import api from './http';

export const getOpportunities = async (params: Record<string, any> = {}) => {
  const { data } = await api.get('/api/opportunities/', { params });
  return data;
};
