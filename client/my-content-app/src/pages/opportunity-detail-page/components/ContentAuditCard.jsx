import React from 'react';
import { Card, Typography, List, Tag, Progress } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const ContentAuditCard = ({ auditResults }) => {
  if (!auditResults) {
    return null;
  }

  const {
    flesch_kincaid_grade,
    readability_assessment,
    entity_coverage_score,
    missing_entities,
    publish_readiness_issues,
  } = auditResults;

  return (
    <Card title="Content Audit" style={{ marginTop: 24 }}>
      <Title level={5}>Readability</Title>
      <Text>{readability_assessment}</Text>
      <Text strong style={{ display: 'block', marginTop: 8 }}>
        Flesch-Kincaid Grade Level: {flesch_kincaid_grade.toFixed(1)}
      </Text>

      <Title level={5} style={{ marginTop: 16 }}>Entity Coverage</Title>
      <Progress percent={entity_coverage_score} />
      {missing_entities && missing_entities.length > 0 && (
        <>
          <Text strong style={{ display: 'block', marginTop: 8 }}>Missing Entities:</Text>
          <List
            dataSource={missing_entities}
            renderItem={(item) => (
              <List.Item>
                <CloseCircleOutlined style={{ color: 'red', marginRight: 8 }} />
                {item}
              </List.Item>
            )}
            size="small"
          />
        </>
      )}

      <Title level={5} style={{ marginTop: 16 }}>Publishing Readiness</Title>
      {publish_readiness_issues && publish_readiness_issues.length > 0 ? (
        <List
          dataSource={publish_readiness_issues}
          renderItem={(item) => (
            <List.Item>
              <CloseCircleOutlined style={{ color: 'red', marginRight: 8 }} />
              <Text>{item.issue}: {item.context}</Text>
            </List.Item>
          )}
          size="small"
        />
      ) : (
        <Space>
          <CheckCircleOutlined style={{ color: 'green' }} />
          <Text>No publishing readiness issues found.</Text>
        </Space>
      )}
    </Card>
  );
};

export default ContentAuditCard;
