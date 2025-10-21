import React, { useContext } from 'react';
import { notification } from 'antd';

// Create a context to hold the notification logic
const NotificationContext = React.createContext();

// Custom hook to access the notification context
export const useNotifications = () => useContext(NotificationContext);

// Provider component that wraps your app
export const NotificationProvider = ({ children }) => {
  const showNotification = (type, message, description) => {
    notification[type]({
      message,
      description,
    });
  };

  return (
    <NotificationContext.Provider value={{ showNotification }}>
      {children}
    </NotificationContext.Provider>
  );
};
