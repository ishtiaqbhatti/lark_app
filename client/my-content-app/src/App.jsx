import React, { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import { useAuth } from './context/AuthContext';
import LoginPage from './pages/Auth/LoginPage';
import { Spin } from 'antd'; // For loading state

// Dynamically import page components
const DiscoveryPage = lazy(() => import('./pages/DiscoveryPage/DiscoveryPage'));
const RunDetailsPage = lazy(() => import('./pages/RunDetailsPage/RunDetailsPage'));
const OpportunitiesPage = lazy(() => import('./pages/OpportunitiesPage/OpportunitiesPage'));
const DashboardPage = lazy(() => import('./pages/Dashboard/DashboardPage'));
const ClientDashboardPage = lazy(() => import('./pages/ClientDashboard/ClientDashboardPage'));
const OpportunityDetailPage = lazy(() => import('./pages/opportunity-detail-page/index.jsx'));
const ActivityLogPage = lazy(() => import('./pages/ActivityLog/ActivityLogPage'));
const SettingsPage = lazy(() => import('./pages/Settings/SettingsPage'));
const NotFoundPage = lazy(() => import('./pages/NotFoundPage/NotFoundPage'));
const BlogPage = lazy(() => import('./pages/BlogPage/BlogPage'));

import { JobProvider } from './context/JobContext';

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
    <Suspense fallback={<div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}><Spin size="large" /></div>}>
      <Routes>
        {isAuthenticated ? (
          <>
            <Route path="/" element={<MainLayout />}>
              <Route index element={<DashboardPage />} />
              <Route path="/clients" element={<ClientDashboardPage />} />
              <Route path="/opportunities" element={<OpportunitiesPage />} />
              <Route path="/opportunities/:opportunityId" element={<OpportunityDetailPage />} />
              <Route path="/discovery-run/:runId" element={<RunDetailsPage />} />
              <Route path="/activity-log" element={<ActivityLogPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/discovery" element={<DiscoveryPage />} />
              <Route path="/blog/:opportunityId" element={<BlogPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Route>
          </>
        ) : (
          <>
            <Route path="/login" element={<LoginPage />} />
            <Route path="*" element={<LoginPage />} />
          </>
        )}
      </Routes>
    </Suspense>
  );
}

export default App;