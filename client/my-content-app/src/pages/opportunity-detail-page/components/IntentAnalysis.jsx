import React from 'react';
import { Card, Typography, Tag, Tooltip } from 'antd';
import { AimOutlined, DollarOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const IntentAnalysis = ({ searchIntentInfo }) => {
  if (!searchIntentInfo) {
    return null;
  }

  const { main_intent, foreign_intent } = searchIntentInfo;

  const intentColor = {
    informational: 'blue',
    commercial: 'gold',
    transactional: 'green',
    navigational: 'purple',
  };

  return (
    <Card title="Search Intent Analysis">
      <Tooltip title="The primary reason a user is searching for this keyword.">
        <div>
          <Text strong>Main Intent: </Text>
          <Tag color={intentColor[main_intent] || 'default'} icon={<AimOutlined />}>
            {main_intent?.toUpperCase()}
          </Tag>
        </div>
      </Tooltip>
      {foreign_intent?.length > 0 && (
        <Tooltip title="Other potential intents this keyword might satisfy.">
          <div style={{ marginTop: '16px' }}>
            <Text strong>Secondary Intents: </Text>
            {foreign_intent.map(intent => (
              <Tag key={intent} color={intentColor[intent] || 'default'} icon={<DollarOutlined />}>
                {intent.toUpperCase()}
              </Tag>
            ))}
          </div>
        </Tooltip>
      )}
    </Card>
  );
};

export default IntentAnalysis;
