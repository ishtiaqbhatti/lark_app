import React from 'react';
import { Typography, Row, Col, Statistic, Tooltip } from 'antd';
import './FunnelChart.css'; // Specific styles for the funnel chart

const { Text, Title } = Typography;

const FunnelChart = ({ totalRaw = 0, unique = 0, qualified = 0, disqualified = 0, addedToDB = 0 }) => {
  const data = [
    { label: "Total Found", value: totalRaw },
    { label: "Unique Keywords", value: unique },
    { label: "Qualified Keywords", value: qualified },
    { label: "Disqualified", value: disqualified },
    { label: "Added to Pipeline", value: addedToDB },
  ];

  const getColor = (label) => {
    switch(label) {
      case "Total Found": return "#1890ff";
      case "Unique Keywords": return "#2db7f5";
      case "Qualified Keywords": return "#52c41a";
      case "Disqualified": return "#f5222d";
      case "Added to Pipeline": return "#722ed1";
      default: return "#d9d9d9";
    }
  };

  return (
    <div className="funnel-chart-container">
      <Title level={5} style={{ marginBottom: '24px', textAlign: 'center' }}>Discovery Funnel</Title>
      <div className="funnel-steps">
        {data.map((item, index) => (
          <Tooltip title={item.label} key={index}>
            <div className="funnel-step" style={{ 
                backgroundColor: getColor(item.label),
                width: `${Math.max(20, (item.value / totalRaw) * 100)}%`, // Scale width
                zIndex: data.length - index // Ensure larger bars are behind
            }}>
              <Text strong className="funnel-value">{item.value.toLocaleString()}</Text>
            </div>
          </Tooltip>
        ))}
      </div>
      <Row gutter={[16, 16]} justify="space-around" style={{ marginTop: '24px' }}>
        {data.map((item, index) => (
          <Col key={index} span={Math.floor(24 / data.length)}>
            <Statistic 
              title={item.label} 
              value={item.value.toLocaleString()} 
              valueStyle={{ color: getColor(item.label) }} 
            />
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default FunnelChart;
