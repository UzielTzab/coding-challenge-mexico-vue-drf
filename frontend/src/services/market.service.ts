import api from './http';

export const getMarkets = async () => {
  const { data } = await api.get('/markets');
  return data;
};
