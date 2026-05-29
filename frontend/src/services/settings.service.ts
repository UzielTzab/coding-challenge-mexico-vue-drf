import api from './http';

export const getSettings = async () => {
  const { data } = await api.get('/settings');
  return data;
};
