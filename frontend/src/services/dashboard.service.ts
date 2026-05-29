import api from './http';

export const getDashboardSummary = async () => {
  const { data } = await api.get('/api/analytics/performance/');
  return data;
};

export const getExchanges = async () => {
  const { data } = await api.get('/api/exchanges/');
  return data;
};
