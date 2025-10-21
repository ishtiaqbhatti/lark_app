import React from 'react';
import { Routes, Route } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import DiscoveryPage from './pages/DiscoveryPage/DiscoveryPage';
import RunDetailsPage from './pages/RunDetailsPage/RunDetailsPage';
import OpportunitiesPage from './pages/OpportunitiesPage/OpportunitiesPage';
import { useAuth } from './context/AuthContext';
import LoginPage from './pages/Auth/LoginPage';
import { Spin } from 'antd'; // For loading state
import DashboardPage from './pages/Dashboard/DashboardPage';
import ClientDashboardPage from './pages/ClientDashboard/ClientDashboardPage';
import OpportunityDetailPage from './pages/opportunity-detail-page/index.jsx';
import ActivityLogPage from './pages/ActivityLog/ActivityLogPage';
import SettingsPage from './pages/Settings/SettingsPage';
import NotFoundPage from './pages/NotFoundPage/NotFoundPage';

import { JobProvider } from './context/JobContext';
import BlogPage from './pages/BlogPage/BlogPage';

// REPLACE the existing `function App() { ... }` block with this:
function App() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Spin size="large" tip="Loading authentication..." />
      </div>
    );
  }

  return (
    <Routes>
      {isAuthenticated ? (
        <>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/clients" element={<ClientDashboardPage />} />
            <Route path="/opportunities" element={<OpportunitiesPage />} />
            <Route path="/opportunities/:opportunityId" element={<OpportunityDetailPage />} />
            <Route path="/discovery/run/:runId" element={<RunDetailsPage />} />
            <Route path="/activity-log" element={<ActivityLogPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="/discovery" element={<DiscoveryPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
          <Route path="/blog/:opportunityId" element={<BlogPage />} />
        </>
      ) : (
        <>
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<LoginPage />} />
        </>
      )}
    </Routes>
  );
}

export default App;