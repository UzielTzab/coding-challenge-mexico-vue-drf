export const useFormatters = () => {
  const formatUSD = (value: number) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
  };
  
  const formatBTC = (value: number) => {
    return value.toFixed(8) + ' BTC';
  };
  
  const formatPercent = (value: number) => {
    return value.toFixed(2) + '%';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return { formatUSD, formatBTC, formatPercent, formatDate };
};
