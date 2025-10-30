import React from 'react';
import { Table, Tag } from 'antd';
import { Link } from 'react-router-dom';

const OpportunityTable = ({ opportunities, isLoading }) => {
  const columns = [
    {
      title: 'Keyword',
      dataIndex: 'keyword',
      key: 'keyword',
      render: (text, record) => <Link to={`/opportunities/${record.id}`}>{text}</Link>,
    },
    {
      title: 'Search Volume',
      dataIndex: ['full_data', 'keyword_info', 'search_volume'],
      key: 'search_volume',
      sorter: (a, b) => a.full_data.keyword_info.search_volume - b.full_data.keyword_info.search_volume,
    },
    {
      title: 'Keyword Difficulty',
      dataIndex: ['full_data', 'keyword_properties', 'keyword_difficulty'],
      key: 'keyword_difficulty',
      sorter: (a, b) => a.full_data.keyword_properties.keyword_difficulty - b.full_data.keyword_properties.keyword_difficulty,
    },
    {
      title: 'CPC',
      dataIndex: ['full_data', 'keyword_info', 'cpc'],
      key: 'cpc',
      sorter: (a, b) => a.full_data.keyword_info.cpc - b.full_data.keyword_info.cpc,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: status => {
        let color = 'geekblue';
        if (status === 'qualified') {
          color = 'green';
        } else if (status === 'rejected') {
          color = 'volcano';
        }
        return (
          <Tag color={color} key={status}>
            {status.toUpperCase()}
          </Tag>
        );
      },
    },
    {
      title: 'Rejected Reason',
      dataIndex: 'blog_qualification_reason',
      key: 'blog_qualification_reason',
      render: (text, record) => record.status === 'rejected' ? text : '-',
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={opportunities}
      loading={isLoading}
      rowKey="id"
    />
  );
};

export default OpportunityTable;
