import { format as formatDateFns } from 'date-fns';

export const formatNumber = (num) => {
  if (num == null || isNaN(num)) return 'N/A';
  return num.toLocaleString();
};

export const formatCurrency = (amount) => {
  if (amount == null || isNaN(amount)) return 'N/A';
  return `$${amount.toFixed(2)}`;
};

export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  try {
    return formatDateFns(new Date(dateString), 'MMM d, yyyy');
  } catch (error) {
    return 'Invalid Date';
  }
};
