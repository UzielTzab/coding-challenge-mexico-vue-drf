import api from './http';

export const getWallets = async () => {
  const { data } = await api.get('/api/wallets/');
  return data;
};
