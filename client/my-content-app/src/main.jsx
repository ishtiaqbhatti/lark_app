import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ClientProvider } from './context/ClientContext';
import { NotificationProvider } from './context/NotificationContext';
import { AuthProvider } from './context/AuthContext';
import App from './App';
import 'antd/dist/reset.css'; // Ant Design's base styles
import './index.css'; // Your global custom styles

import { JobProvider } from './context/JobContext';
import GlobalJobTracker from './components/GlobalJobTracker';

// ... (other imports)

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false, // Don't refetch automatically on window focus
      retry: 1, // Retry failed queries once
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <NotificationProvider>
          <AuthProvider>
            <ClientProvider>
              <JobProvider>
                <App />
                <GlobalJobTracker />
              </JobProvider>
            </ClientProvider>
          </AuthProvider>
        </NotificationProvider>
      </QueryClientProvider>
    </BrowserRouter>
  </React.StrictMode>
);
