import React, { useState } from 'react';
import { Table, Button, Modal } from 'antd';
import { LineChartOutlined } from '@ant-design/icons';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const OpportunityTable = ({ opportunities }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedKeyword, setSelectedKeyword] = useState(null);

  const showModal = (keyword) => {
    setSelectedKeyword(keyword);
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setSelectedKeyword(null);
  };

  const columns = [
    {
      title: 'Keyword',
      dataIndex: 'keyword',
      key: 'keyword',
    },
    {
      title: 'Search Volume',
      dataIndex: ['keyword_info', 'search_volume'],
      key: 'search_volume',
    },
    {
      title: 'Difficulty',
      dataIndex: ['keyword_properties', 'keyword_difficulty'],
      key: 'difficulty',
    },
    {
      title: 'CPC',
      dataIndex: ['keyword_info', 'cpc'],
      key: 'cpc',
      render: (cpc) => `$${cpc}`,
    },
    {
      title: 'Competition',
      dataIndex: ['keyword_info', 'competition'],
      key: 'competition',
    },
    {
      title: 'Trend',
      key: 'trend',
      render: (_, record) => (
        <Button icon={<LineChartOutlined />} onClick={() => showModal(record)} />
      ),
    },
  ];

  const chartData = selectedKeyword?.keyword_info?.monthly_searches?.map(monthly => ({
    month: `${monthly.year}-${String(monthly.month).padStart(2, '0')}`,
    search_volume: monthly.search_volume,
  }));

  return (
    <>
      <Table dataSource={opportunities} columns={columns} rowKey="keyword" />
      <Modal
        title={`Search Volume Trend for "${selectedKeyword?.keyword}"`}
        visible={isModalVisible}
        onCancel={handleCancel}
        footer={null}
        width={800}
      >
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="search_volume" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </Modal>
    </>
  );
};

export default OpportunityTable;
