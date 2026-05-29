import api from './http';

export const getWallets = async () => {
  const { data } = await api.get('/wallets');
  return data;
};
