import api from './http';

export const getOpportunities = async () => {
  const { data } = await api.get('/opportunities');
  return data;
};
