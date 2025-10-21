// This is a new file. Create it with the following content:
import React from 'react';
import { Modal, Form, Input } from 'antd';

const AddNewClientModal = ({ open, onCancel, onAddClient, loading }) => {
  const [form] = Form.useForm();

  const handleOk = () => {
    form.validateFields()
      .then(values => {
        onAddClient(values);
        form.resetFields();
      })
      .catch(info => {
        console.log('Validate Failed:', info);
      });
  };

  return (
    <Modal
      title="Add New Client"
      open={open}
      onOk={handleOk}
      onCancel={onCancel}
      confirmLoading={loading}
      okText="Add Client"
    >
      <Form
        form={form}
        layout="vertical"
        name="add_client_form"
      >
        <Form.Item
          name="client_name"
          label="Client Name"
          rules={[{ required: true, message: 'Please enter the client\'s name!' }]}
        >
          <Input autoFocus />
        </Form.Item>
        <Form.Item
          name="client_id"
          label="Client ID"
          rules={[{ required: true, message: 'Please enter a unique client ID!' }]}
          extra="This should be a unique identifier for the client (e.g., my_company_name)."
        >
          <Input />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default AddNewClientModal;
