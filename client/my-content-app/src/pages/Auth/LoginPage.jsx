// This is a new file. Create it with the following content:
import React, { useState } from 'react';
import { Form, Input, Button, Card, Typography, Alert, Space } from 'antd';
import { LockOutlined } from '@ant-design/icons';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const { Title } = Typography;

const LoginPage = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { login } = useAuth();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    setError(null);
    try {
      await login(values.password); // Only password is required for dummy login
      navigate('/dashboard'); // Redirect to the main dashboard on success
    } catch (err) {
      setError(err.message || 'Login failed. Please check your password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Space
      direction="vertical"
      align="center"
      style={{
        width: '100%',
        minHeight: '100vh',
        justifyContent: 'center',
        background: '#f0f2f5',
      }}
    >
      <Card style={{ width: 350, textAlign: 'center' }}>
        <Title level={3}>Content AI Login</Title>
        {error && (
          <Alert message="Authentication Failed" description={error} type="error" showIcon style={{ marginBottom: 20 }} />
        )}
        <Form
          name="login"
          initialValues={{ remember: true }}
          onFinish={onFinish}
        >
          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Please enter your password!' }]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="Password" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              Log in
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </Space>
  );
};

export default LoginPage;
