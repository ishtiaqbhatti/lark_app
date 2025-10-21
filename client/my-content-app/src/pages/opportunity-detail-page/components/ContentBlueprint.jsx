import React, { useState, useEffect } from 'react';
import { Card, Typography, List, Tag, Descriptions, Button, Tooltip, Select } from 'antd';
import { CopyOutlined, LinkOutlined, BulbOutlined, PlusOutlined } from '@ant-design/icons';
import { useNotifications } from '../../../context/NotificationContext';
import NoData from './NoData';

const { Title, Paragraph, Text } = Typography;
const { Option } = Select;

const ContentBlueprint = ({ blueprint, overrides, setOverrides }) => {
  const { showNotification } = useNotifications();
  const [paaToAdd, setPaaToAdd] = useState(null);

  if (!blueprint) {
    return <Card><Paragraph type="secondary">No content blueprint available.</Paragraph></Card>;
  }

  const { ai_content_brief, content_intelligence, recommended_strategy } = blueprint;
  const people_also_ask = blueprint.serp_overview?.people_also_ask || [];

  const handleCopyOutline = () => {
    const outline = overrides
      .map((item) => {
        const h3s = item.h3s.map((h3) => `  - ${h3}`).join('\n');
        return `${item.h2}\n${h3s}`;
      })
      .join('\n\n');
    navigator.clipboard.writeText(outline);
    showNotification('success', 'Copied to Clipboard', 'The article outline has been copied.');
  };

  const handleAddPaa = () => {
    if (!paaToAdd) return;

    const faqSectionIndex = overrides.findIndex(sec => sec.h2.toLowerCase().includes('frequently asked questions'));
    
    if (faqSectionIndex > -1) {
      const newStructure = [...overrides];
      newStructure[faqSectionIndex].h3s.push(paaToAdd);
      setOverrides(newStructure);
      showNotification('success', 'Question Added', `"${paaToAdd}" was added to the outline.`);
    } else {
      showNotification('warning', 'Section Not Found', 'Could not find a "Frequently Asked Questions" section to add this to.');
    }
    setPaaToAdd(null);
  };
  
  return (
    <Card title="AI Content Blueprint">
      <Descriptions bordered column={1} size="small" style={{ marginBottom: '24px' }}>
        <Descriptions.Item label="Target Audience">{ai_content_brief?.target_audience_persona || 'Not available'}</Descriptions.Item>
        <Descriptions.Item label="Primary Goal">{ai_content_brief?.primary_goal || 'Not available'}</Descriptions.Item>
        <Descriptions.Item label="Target Word Count">{ai_content_brief?.target_word_count || 'Not available'}</Descriptions.Item>
      </Descriptions>

      <Title level={5}>Dynamic SERP Instructions</Title>
      <List
        dataSource={ai_content_brief.dynamic_serp_instructions}
        renderItem={(item) => <List.Item><BulbOutlined style={{ marginRight: 8 }} />{item}</List.Item>}
        style={{ marginBottom: '24px' }}
        size="small"
      />

      <Title level={5}>Content Gaps & Unique Angles</Title>
      <List
        dataSource={content_intelligence.identified_content_gaps}
        renderItem={(item) => <List.Item>{item}</List.Item>}
        style={{ marginBottom: '24px' }}
      />

      <Title level={5}>Recommended Article Structure</Title>
      <div style={{ marginBottom: 16 }}>
        <Select
          showSearch
          placeholder="Select a 'People Also Ask' question to add to your outline"
          style={{ width: 'calc(100% - 120px)', marginRight: 8 }}
          onChange={value => setPaaToAdd(value)}
          value={paaToAdd}
        >
          {people_also_ask.map(q => <Option key={q} value={q}>{q}</Option>)}
        </Select>
        <Button icon={<PlusOutlined />} onClick={handleAddPaa} disabled={!paaToAdd}>Add</Button>
        <Button
          icon={<CopyOutlined />}
          onClick={handleCopyOutline}
          style={{ float: 'right' }}
        >
          Copy Outline
        </Button>
      </div>
      <List
        dataSource={overrides}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta
              title={item.h2}
              description={
                <div style={{ paddingLeft: '20px' }}>
                  {item.h3s.map(h3 => <p key={h3} style={{ margin: '4px 0' }}>- {h3}</p>)}
                </div>
              }
            />
          </List.Item>
        )}
        style={{ marginBottom: '24px' }}
      />

      <Title level={5}>Key Entities to Mention</Title>
      <div style={{ marginBottom: '24px' }}>
        {content_intelligence.key_entities_from_competitors.map((entity) => (
          <Tag key={entity} style={{ margin: '4px' }}>{entity}</Tag>
        ))}
      </div>

      <Title level={5}>Focus Competitors</Title>
      <List
        dataSource={recommended_strategy.focus_competitors}
        renderItem={(item) => (
          <List.Item>
            <a href={item.url} target="_blank" rel="noopener noreferrer">
              <LinkOutlined style={{ marginRight: 8 }} />
              {item.title}
            </a>
          </List.Item>
        )}
        style={{ marginBottom: '24px' }}
        bordered
        size="small"
      />

      <Title level={5}>Internal Linking Suggestions</Title>
      {blueprint.internal_linking_suggestions && blueprint.internal_linking_suggestions.length > 0 ? (
        <List
          dataSource={blueprint.internal_linking_suggestions}
          renderItem={(item) => (
            <List.Item>
              <Tooltip title={`Link to: ${item.url}`}>
                <Text>Anchor Text: "{item.anchor_text}"</Text>
              </Tooltip>
            </List.Item>
          )}
          bordered
          size="small"
        />
      ) : (
        <NoData description="No internal linking suggestions were generated." />
      )}
    </Card>
  );
};

export default ContentBlueprint;
