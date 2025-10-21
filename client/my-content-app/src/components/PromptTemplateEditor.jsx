// This is a new file. Create it with the following content:
import React, { useRef, useState, useEffect } from 'react';
import { Input, Button, Space, Tooltip, Typography, List, Divider, Row, Col, Card } from 'antd';
import { BulbOutlined, CopyOutlined } from '@ant-design/icons';

const { TextArea } = Input;
const { Text } = Typography;

const PLACEHOLDERS = [
  { name: "[TOPIC]", desc: "The main keyword or topic of the article." },
  { name: "[PRIMARY KEYWORD]", desc: "The exact target keyword for SEO." },
  { name: "[LSI/secondary keywords]", desc: "List of related keywords/entities to include." },
  { name: "[WORD_COUNT]", desc: "The target word count for the article." },
  { name: "[CTA_URL]", desc: "The call-to-action URL to promote." },
  { name: "[[IMAGE: <prompt>]]", desc: "Placeholder for in-article images (AI will fill <prompt>)." },
  // Add other placeholders as they become relevant
];

const PromptTemplateEditor = ({ value, onChange, disabled }) => {
  const textAreaRef = useRef(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (copied) {
      const timer = setTimeout(() => setCopied(false), 2000);
      return () => clearTimeout(timer);
    }
  }, [copied]);

  const handleInsertPlaceholder = (placeholder) => {
    const textarea = textAreaRef.current?.resizableTextArea?.textArea;
    if (textarea) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newValue = value.substring(0, start) + placeholder + value.substring(end, value.length);
      onChange(newValue);
      // Move cursor after inserted placeholder
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + placeholder.length;
        textarea.focus();
      }, 0);
    }
  };

  return (
    <Row gutter={16}>
      <Col span={18}>
        <TextArea
          ref={textAreaRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          rows={20}
          placeholder="Enter your custom AI prompt template here..."
          disabled={disabled}
          autoSize={{ minRows: 15, maxRows: 30 }}
        />
        <Space style={{ marginTop: '10px' }}>
          <Tooltip title="Copy entire prompt to clipboard">
            <Button icon={<CopyOutlined />} onClick={() => { handleInsertPlaceholder(value); setCopied(true); }}>
              {copied ? 'Copied!' : 'Copy Full Prompt'}
            </Button>
          </Tooltip>
        </Space>
      </Col>
      <Col span={6}>
        <Card title={<Space><BulbOutlined /> Available Placeholders</Space>} size="small">
          <List
            size="small"
            dataSource={PLACEHOLDERS}
            renderItem={item => (
              <List.Item
                actions={[
                  <Button
                    key="insert"
                    type="link"
                    size="small"
                    onClick={() => handleInsertPlaceholder(item.name)}
                    disabled={disabled}
                  >
                    Insert
                  </Button>
                ]}
              >
                <List.Item.Meta
                  title={<Text code>{item.name}</Text>}
                  description={<Text type="secondary" ellipsis={{tooltip: item.desc}}>{item.desc}</Text>}
                />
              </List.Item>
            )}
          />
          <Divider style={{ margin: '16px 0' }} />
          <Text type="secondary" style={{fontSize: '0.8em'}}>
            These placeholders will be dynamically replaced with data from your opportunity blueprint.
          </Text>
        </Card>
      </Col>
    </Row>
  );
};

export default PromptTemplateEditor;