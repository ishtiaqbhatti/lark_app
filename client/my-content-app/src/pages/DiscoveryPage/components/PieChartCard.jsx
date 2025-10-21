import React from 'react';
import { Card, Typography, Empty, Tooltip } from 'antd';
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';

const { Title } = Typography;

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF19AF'];

const PieChartCard = ({ title, data, onSliceClick }) => {
  const chartData = Object.entries(data).map(([name, value]) => ({ name, value }));

  if (chartData.length === 0) {
    return (
      <Card>
        <Title level={5} style={{ marginBottom: '16px' }}>{title}</Title>
        <Empty description={`No ${title.toLowerCase()} data`} />
      </Card>
    );
  }

  const renderLegend = (props) => {
    const { payload } = props;
    return (
      <ul style={{ listStyle: 'none', padding: '0', margin: '0', maxHeight: '300px', overflowY: 'auto' }}>
        {payload.map((entry, index) => {
          const { value, color } = entry;
          const maxLength = 40;
          const isTruncated = value.length > maxLength;
          const truncatedValue = isTruncated ? `${value.substring(0, maxLength)}...` : value;

          return (
            <li key={`item-${index}`} style={{ marginBottom: '4px', display: 'flex', alignItems: 'center' }}>
              <span style={{ width: '10px', height: '10px', backgroundColor: color, marginRight: '10px', display: 'inline-block' }}></span>
              {isTruncated ? (
                <Tooltip title={value}>
                  <span style={{ cursor: 'default' }}>{truncatedValue}</span>
                </Tooltip>
              ) : (
                <span>{value}</span>
              )}
            </li>
          );
        })}
      </ul>
    );
  };


  return (
    <Card>
      <Title level={5} style={{ marginBottom: '16px' }}>{title}</Title>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
            nameKey="name"
            onClick={(data) => onSliceClick && onSliceClick(data.name)}
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <RechartsTooltip />
          <Legend content={renderLegend} />
        </PieChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default PieChartCard;
