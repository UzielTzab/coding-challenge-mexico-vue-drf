import api from './http';

export const getSettings = async () => {
  const { data } = await api.get('/api/settings/');
  return data;
};

export const updateSettings = async (id: string, payload: any) => {
  const { data } = await api.patch(`/api/settings/${id}/`, payload);
  return data;
};
