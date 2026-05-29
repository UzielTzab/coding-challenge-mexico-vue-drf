import api from './http';

export const getDashboardSummary = async () => {
  const { data } = await api.get('/dashboard/summary');
  return data;
};
