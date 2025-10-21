// This is a new file. Create it with the following content:
import React, { useState } from 'react';
import { Layout, Typography, Spin, Alert, Card, Row, Col, Statistic, Button, Space } from 'antd';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getClients, getDashboardStats, addClient } from '../../services/clientService';
import { useClient } from '../../hooks/useClient';
import { useNotifications } from '../../context/NotificationContext';
import AddNewClientModal from './AddNewClientModal';
import { useNavigate } from 'react-router-dom'; // NEW

const { Content } = Layout;
const { Title } = Typography;

const ClientCard = ({ client, onSelectClient, isActive }) => {
  const { data: stats, isLoading: isLoadingStats, isError: isErrorStats } = useQuery(
    ['dashboardStats', client.client_id],
    () => getDashboardStats(client.client_id),
    {
      enabled: !!client.client_id,
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    }
  );

  return (
    <Card
      title={<Title level={5} style={{ margin: 0 }}>{client.client_name}</Title>}
      extra={
        <Button
          type={isActive ? "primary" : "default"}
          onClick={() => onSelectClient(client.client_id)}
          disabled={isActive}
        >
          {isActive ? 'Current Client' : 'Select'}
        </Button>
      }
      style={{ marginBottom: '16px' }}
      loading={isLoadingStats}
    >
      <Row gutter={16}>
        <Col span={8}>
          <Statistic title="Opportunities" value={stats?.status_counts?.all || 0} />
        </Col>
        <Col span={8}>
          <Statistic title="Qualified" value={stats?.status_counts?.validated || 0} />
        </Col>
        <Col span={8}>
          <Statistic title="Generated" value={stats?.status_counts?.generated || 0} />
        </Col>
      </Row>
      {isErrorStats && (
        <Alert
          message="Error loading stats"
          description={isErrorStats?.message || 'Failed to load dashboard statistics.'}
          type="error"
          style={{ marginTop: '16px' }}
        />
      )}
    </Card>
  );
};

const ClientDashboardPage = () => {
  const { clientId, setClientId } = useClient();
  const { showNotification } = useNotifications();
  const queryClient = useQueryClient();
  const navigate = useNavigate(); // NEW
  const [isModalVisible, setIsModalVisible] = useState(false);

  const { data: clients = [], isLoading, isError, error } = useQuery(
    'clients',
    getClients,
  );

  const { mutate: addClientMutation, isLoading: isAddingClient } = useMutation(
    (newClient) => addClient(newClient),
    {
      onSuccess: () => {
        showNotification('success', 'Client Added', 'New client has been successfully added.');
        queryClient.invalidateQueries('clients'); // Invalidate to refetch client list
        setIsModalVisible(false);
      },
      onError: (err) => {
        showNotification('error', 'Failed to Add Client', err.message || 'An error occurred while adding the client.');
      },
    }
  );

  const handleSelectClient = (selectedClientId) => {
    setClientId(selectedClientId);
    navigate('/dashboard'); // Navigate to the new dashboard page after selecting
  };

  if (isLoading) {
    return <Spin tip="Loading clients..." style={{ display: 'block', marginTop: '50px' }} />;
  }

  if (isError) {
    return <Alert message="Error" description={error?.message || "Failed to load clients. Please try again."} type="error" showIcon />;
  }

  return (
    <Layout style={{ padding: '24px' }}>
      <Content>
        <Title level={2}>Client Dashboard</Title>
        <Space style={{ marginBottom: '16px' }}>
          <Button type="primary" onClick={() => setIsModalVisible(true)}>Add New Client</Button>
        </Space>

        <Row gutter={[16, 16]}>
          {clients.map(client => (
            <Col xs={24} sm={12} md={8} lg={6} key={client.client_id}>
              <ClientCard 
                client={client} 
                onSelectClient={handleSelectClient} 
                isActive={client.client_id === clientId} 
              />
            </Col>
          ))}
        </Row>
      </Content>
      <AddNewClientModal
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        onAddClient={addClientMutation}
        loading={isAddingClient}
      />
    </Layout>
  );
};

export default ClientDashboardPage;
