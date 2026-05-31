import api from './http';

export const getWallets = async () => {
  const { data } = await api.get('/api/wallets/');
  return data;
};

export const getWalletMovements = async (params?: any) => {
  const { data } = await api.get('/api/wallets/movements/', { params });
  return data;
};
