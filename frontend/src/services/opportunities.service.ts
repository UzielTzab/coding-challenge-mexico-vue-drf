import api from './http';

export const getOpportunities = async (params?: any) => {
  const { data } = await api.get('/api/opportunities/', { params });
  return data;
};
