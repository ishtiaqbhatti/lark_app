import { Menu, Layout, Typography, Button, Space, Select, Spin, Input, Card, Tag } from 'antd'; // Add Button and Typography
import { DashboardOutlined, SettingOutlined, LogoutOutlined, BulbOutlined, RocketOutlined, ClockCircleOutlined } from '@ant-design/icons'; // Add new icons
import { NavLink, useLocation, useNavigate, Outlet } from 'react-router-dom'; // Add useNavigate
import { useAuth } from '../../context/AuthContext'; // NEW
import { useClient } from '../../context/ClientContext'; // NEW
import { getClients, searchAllAssets } from '../../services/clientService'; // NEW
import { useQuery } from 'react-query'; // NEW
import useDebounce from '../../hooks/useDebounce'; // Assuming you have a useDebounce hook
import React, { useState, useEffect } from 'react';

const { Sider, Header, Content } = Layout;
const { Title, Text } = Typography;

// REPLACE the existing `menuItems` definition with this:
const menuItems = [
  {
    key: '/dashboard',
    icon: <DashboardOutlined />,
    label: <NavLink to="/dashboard">Dashboard</NavLink>,
  },
  {
    key: '/opportunities',
    icon: <BulbOutlined />,
    label: <NavLink to="/opportunities">Opportunities</NavLink>,
  },
  {
    key: '/discovery',
    icon: <RocketOutlined />,
    label: <NavLink to="/discovery">Discovery</NavLink>,
  },
  {
    key: '/activity-log',
    icon: <ClockCircleOutlined />,
    label: <NavLink to="/activity-log">Activity Log</NavLink>,
  },
  {
    key: '/settings',
    icon: <SettingOutlined />,
    label: <NavLink to="/settings">Settings</NavLink>,
  },
];

// REPLACE the existing `MainLayout` component with this:
const MainLayout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { clientId, setClientId } = useClient();
  const { data: clients = [], isLoading: isLoadingClients } = useQuery('clients', getClients);

  const [globalSearchResults, setGlobalSearchResults] = useState([]);
  const [isSearchLoading, setIsSearchLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  useEffect(() => {
    const handleGlobalSearch = async () => {
      if (!debouncedSearchTerm || debouncedSearchTerm.length < 3 || !clientId) {
        setGlobalSearchResults([]);
        return;
      }
      setIsSearchLoading(true);
      try {
        const results = await searchAllAssets(clientId, debouncedSearchTerm);
        setGlobalSearchResults(results);
      } catch (error) {
        console.error("Global search failed:", error);
        setGlobalSearchResults([]);
      } finally {
        setIsSearchLoading(false);
      }
    };

    handleGlobalSearch();
  }, [debouncedSearchTerm, clientId]);

  const handleSearchResultClick = (e) => {
    const [type, id] = e.key.split('-');
    setGlobalSearchResults([]); // Clear search results after selection
    if (type === 'opportunity') navigate(`/opportunities/${id}`);
    if (type === 'discovery_run') navigate(`/discovery/run/${id}`);
    // Add more navigation logic for other types if needed
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleSelectClientFromDropdown = (value) => {
    setClientId(value);
    localStorage.setItem('clientId', value);
    navigate('/dashboard'); // CRITICAL FIX: Redirect to a safe page (dashboard) after switching client
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible breakpoint="lg" collapsedWidth="0">
        <div style={{ padding: '16px', textAlign: 'center' }}>
          <Title level={4} style={{ color: 'white', margin: 0 }}>Content AI</Title>
          <Text style={{ color: 'rgba(255,255,255,0.6)', fontSize: '0.8em' }}>
            {isLoadingClients ? 'Loading Clients...' : `Client: ${clients.find(c => c.client_id === clientId)?.client_name || clientId}`}
          </Text>
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
        />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #f0f0f0' }}>
<div style={{ padding: '0 16px', color: 'rgba(255, 255, 255, 0.65)' }}>
  <Space>
    {isLoadingClients ? <Spin size="small" /> : `Client: ${clients.find(c => c.client_id === clientId)?.client_name || 'N/A'}`}
  </Space>
</div>
          <div style={{ flexGrow: 1, margin: '0 20px', maxWidth: '400px' }}>
            <Input.Search
              placeholder="Search keywords, opportunities, runs..."
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ width: '100%' }}
              allowClear
              loading={isSearchLoading}
            />
            {globalSearchResults.length > 0 && (
              <Card
                size="small"
                style={{ position: 'absolute', zIndex: 100, width: 'inherit', marginTop: '5px' }}
                bodyStyle={{ padding: '0px' }}
              >
                <Menu
  onClick={handleSearchResultClick}
  style={{ width: '100%', borderRight: 0 }}
>
  {globalSearchResults.map(item => {
    const key = `${item.type}-${item.id}`;
    let labelText = item.keyword || item.name || 'N/A';
    let typeTag = item.type.replace(/_/g, ' ').toUpperCase();

    return (
      <Menu.Item key={key} icon={item.type === 'opportunity' ? <BulbOutlined /> : <RocketOutlined />}>
        <Space size="small">
          <Text ellipsis={true} style={{ maxWidth: '200px' }}>{labelText}</Text>
          <Tag color={item.type === 'opportunity' ? 'blue' : 'purple'}>{typeTag}</Tag>
        </Space>
      </Menu.Item>
    );
  })}
</Menu>
              </Card>
            )}
          </div>
          <Space>
            <Select
              value={clientId}
              style={{ width: 180 }}
              onChange={handleSelectClientFromDropdown}
              loading={isLoadingClients}
              disabled={isLoadingClients || clients.length === 0}
              options={clients.map(c => ({ value: c.client_id, label: c.client_name }))}
            />
            <Button icon={<LogoutOutlined />} onClick={handleLogout}>Logout</Button>
          </Space>
        </Header>
        <Content style={{ margin: '16px' }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
