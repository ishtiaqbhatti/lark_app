import React from 'react';
import { Layout, Menu, Typography } from 'antd';
import { RocketOutlined, BulbOutlined } from '@ant-design/icons';
import { NavLink, useLocation } from 'react-router-dom';

const { Sider } = Layout;
const { Title } = Typography;

// Menu items for the sidebar
const menuItems = [
  {
    key: '/',
    icon: <RocketOutlined />,
    label: <NavLink to="/">Discovery</NavLink>,
  },
  {
    key: '/opportunities',
    icon: <BulbOutlined />,
    label: <NavLink to="/opportunities">Opportunities</NavLink>,
  },
  // Add other navigation links here as you build new pages
  // {
  //   key: '/pipeline',
  //   icon: <BranchesOutlined />,
  //   label: <NavLink to="/pipeline">Content Pipeline</NavLink>,
  // },
];

const AppSidebar = () => {
  const location = useLocation(); // To highlight the active menu item

  return (
    <Sider collapsible breakpoint="lg" collapsedWidth="0">
      <div style={{ padding: '16px', textAlign: 'center' }}>
        <Title level={4} style={{ color: 'white', margin: 0 }}>Content AI</Title>
      </div>
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={[location.pathname]} // Highlight the current path
        items={menuItems}
      />
    </Sider>
  );
};

export default AppSidebar;
