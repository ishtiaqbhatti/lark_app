// This is a new file. Create it with the following content:
import React, { useState, useEffect } from 'react';
import { Layout, Typography, Tabs, Spin, Alert, Button, Space, Form } from 'antd';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getClientSettings, updateClientSettings } from '../../services/clientSettingsService'; // Corrected
import { useClient } from '../../hooks/useClient'; // NEW
import { useNotifications } from '../../context/NotificationContext'; // NEW
import { SaveOutlined, ReloadOutlined } from '@ant-design/icons';
import DiscoverySettingsTab from './tabs/DiscoverySettingsTab'; // NEW
import ScoringWeightsTab from './tabs/ScoringWeightsTab'; // NEW
import AiContentSettingsTab from './tabs/AiContentSettingsTab'; // NEW

const { Content } = Layout;
const { Title, Text } = Typography;

// Placeholder tab components
const ApiKeysSettingsTab = ({ settings, form }) => <Alert message="API Keys" description="API key management will go here." type="info" />; // NEW for task 3.3.1 (API Key Management)

const SettingsPage = () => {
  console.log('Rendering SettingsPage');
  const { clientId } = useClient();
  const { showNotification } = useNotifications();
  const queryClient = useQueryClient();
  const [form] = Form.useForm();
  const [isDirty, setIsDirty] = useState(false); // To track if form has unsaved changes

  const { data: currentSettings, isLoading, isError, error, refetch } = useQuery(
    ['clientSettings', clientId],
    () => getClientSettings(clientId),
    {
      enabled: !!clientId,
      onSuccess: (data) => {
        form.setFieldsValue(data); // Populate form with fetched settings
        setIsDirty(false); // Reset dirty state on successful fetch/load
      },
      onError: (err) => {
        showNotification('error', 'Failed to Load Settings', err.message || 'An error occurred while loading settings.');
      },
      staleTime: 5 * 60 * 1000, // Consider settings stale after 5 minutes
    }
  );

  const { mutate: saveSettingsMutation, isLoading: isSavingSettings } = useMutation(
    (updatedSettings) => updateClientSettings(clientId, updatedSettings),
    {
      onSuccess: () => {
        showNotification('success', 'Settings Saved', 'Client settings updated successfully.');
        setIsDirty(false); // Mark as clean after saving
        queryClient.invalidateQueries(['clientSettings', clientId]); // Invalidate to ensure fresh data if re-fetched elsewhere
      },
      onError: (err) => {
        showNotification('error', 'Save Failed', err.message || 'An error occurred while saving settings.');
      },
    }
  );

  const handleFormChange = () => {
    setIsDirty(true); // Mark form as dirty on any change
  };

  const handleSave = () => {
    form.validateFields()
      .then(values => {
        saveSettingsMutation(values);
      })
      .catch(info => {
        showNotification('error', 'Validation Error', 'Please correct the highlighted fields.');
        console.log('Validate Failed:', info);
      });
  };

  const handleResetToCurrent = () => {
    if (currentSettings) {
      form.setFieldsValue(currentSettings);
      setIsDirty(false);
      showNotification('info', 'Reset', 'Form reset to current saved settings.');
    }
  };

  if (isLoading) {
    return <Spin tip="Loading settings..." style={{ display: 'block', marginTop: '50px' }} />;
  }

  if (isError) {
    return <Alert message="Error" description={error?.message || "Failed to load settings."} type="error" showIcon />;
  }

  const tabItems = [
    {
      label: 'Discovery & Filtering',
      key: 'discovery',
      children: <DiscoverySettingsTab settings={currentSettings} form={form} />,
    },
    {
      label: 'Scoring & Weights',
      key: 'scoring',
      children: <ScoringWeightsTab settings={currentSettings} form={form} />,
    },
    {
      label: 'AI & Content Generation',
      key: 'ai-content',
      children: <AiContentSettingsTab settings={currentSettings} form={form} />,
    },
    {
      label: 'API Keys', // NEW tab
      key: 'api-keys',
      children: <ApiKeysSettingsTab settings={currentSettings} form={form} />,
    }
  ];

  return (
    <Layout style={{ padding: '24px' }}>
      <Content>
        <Title level={2}>Client Settings: {clientId}</Title>
        <Form
          form={form}
          layout="vertical"
          onValuesChange={handleFormChange}
          onFinish={handleSave}
          initialValues={currentSettings} // Set initial values from fetched data
        >
          <Tabs defaultActiveKey="discovery" items={tabItems} style={{ marginBottom: '24px' }} />

          <Space>
            <Button 
              type="primary" 
              htmlType="submit" 
              icon={<SaveOutlined />} 
              loading={isSavingSettings} 
              disabled={!isDirty || isSavingSettings}
            >
              Save Changes
            </Button>
            <Button 
              icon={<ReloadOutlined />} 
              onClick={handleResetToCurrent} 
              disabled={!isDirty || isSavingSettings}
            >
              Reset to Current
            </Button>
          </Space>
        </Form>
      </Content>
    </Layout>
  );
};

export default SettingsPage;