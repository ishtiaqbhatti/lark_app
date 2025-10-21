import React from 'react';
import { Card, Typography, Tooltip, Progress, List, Tag } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

const scoreCategoryMapping = {
  'Ranking & Competition': ['ease_of_ranking', 'competitor_weakness', 'competitor_performance'],
  'Traffic & Commercial Value': ['traffic_potential', 'commercial_intent', 'growth_trend', 'volume_volatility'],
  'SERP Environment': ['serp_features', 'serp_volatility', 'serp_crowding', 'serp_threat', 'serp_freshness'],
  'Keyword Profile': ['keyword_structure'],
};

const friendlyExplanations = {
  ease_of_ranking: "This score assesses the overall difficulty of ranking on the first page of Google for this keyword. It's a composite metric that considers the authority of competing websites, the keyword's inherent difficulty, and the number of competing pages. A higher score means we've identified a path of lower resistance.",
  competitor_weakness: "We analyze the top-ranking pages to find their weak spots. This score is higher if competitors have low domain authority, few backlinks, or other vulnerabilities that we can strategically exploit to outrank them.",
  competitor_performance: "This score evaluates the technical performance of competing websites, such as their loading speed and mobile-friendliness. Slower or poorly optimized competitor sites present a clear opportunity, as search engines penalize them, making it easier for us to rank higher with a technically superior page.",
  traffic_potential: "This score estimates the potential traffic this keyword could generate. It's not just about raw search volume; it also considers the keyword's cost-per-click (CPC) value, indicating its commercial worth. A high score suggests the keyword can attract a valuable audience.",
  commercial_intent: "We analyze the language of the keyword and the types of ads on the search results page to determine the user's intent. A high score indicates that the user is likely looking to make a purchase or engage a service, making the traffic more valuable.",
  growth_trend: "This score reflects the keyword's popularity over time. We analyze search data from the past year to identify upward trends. A high score means the keyword is becoming more popular, representing a growing area of interest and a sustainable source of future traffic.",
  volume_volatility: "This score measures the stability of the keyword's search volume. A low score indicates high volatility (e.g., a seasonal trend), while a high score suggests a stable, consistent search volume, making it a more reliable target for long-term content strategy.",
  serp_features: "This score identifies opportunities within the Search Engine Results Page (SERP) itself. We look for features like 'Featured Snippets,' 'People Also Ask' boxes, and video carousels. A high score means there are multiple ways to appear on the first page beyond the standard blue links.",
  serp_volatility: "This score measures how frequently the rankings for this keyword change. A highly volatile SERP, where rankings fluctuate often, can be an opportunity to quickly gain a foothold, as it indicates that search engines are still trying to determine the best results.",
  serp_crowding: "This score assesses how 'crowded' the search results page is with non-organic results like ads, image packs, and shopping results. A lower score means the page is very crowded, which can push organic results further down the page and reduce their visibility.",
  serp_threat: "This score identifies the presence of dominant, high-authority domains (like Wikipedia, government sites, or major news outlets) that are extremely difficult to outrank. A high score indicates the absence of such threats, making it a more level playing field.",
  serp_freshness: "This score evaluates the age of the content currently ranking on the first page. If the top results are several years old, it signals a 'freshness' opportunity, where new, up-to-date content is likely to be favored by search engines.",
  keyword_structure: "This score analyzes the composition of the keyword itself. Longer, more specific keywords (long-tail keywords) are often less competitive and signal a more specific user intent, making them easier to rank for. A high score is awarded to these types of keywords.",
};

const StrategicScoreBreakdown = ({ scoreBreakdown }) => {
  if (!scoreBreakdown) {
    return null;
  }

  const getScoreColor = (score) => {
    if (score > 70) return '#52c41a'; // green
    if (score > 40) return '#faad14'; // orange
    return '#f5222d'; // red
  };

  return (
    <Card title="Strategic Score Analysis" style={{ marginTop: 24 }}>
      <Paragraph type="secondary">
        This analysis breaks down the main factors contributing to the overall Strategic Score. Each factor is scored from 0-100, where a higher score indicates a better opportunity.
      </Paragraph>
      {Object.entries(scoreCategoryMapping).map(([category, keys]) => (
        <div key={category}>
          <Title level={4} style={{ marginTop: 24, marginBottom: 16 }}>{category}</Title>
          <List
            itemLayout="vertical"
            dataSource={keys.map(key => ({ key, ...scoreBreakdown[key] })).filter(item => item.name)}
            renderItem={(factor) => (
              <List.Item key={factor.key}>
                <List.Item.Meta
                  title={
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <span>
                        {factor.name}
                        <Tooltip title={friendlyExplanations[factor.key]}>
                          <InfoCircleOutlined style={{ marginLeft: 8, color: '#888' }} />
                        </Tooltip>
                      </span>
                      <Tag color={getScoreColor(factor.score)} style={{ fontSize: '1rem', padding: '4px 8px' }}>
                        {factor.score.toFixed(1)}
                      </Tag>
                    </div>
                  }
                  description={
                    <div>
                      <Progress
                        percent={factor.score}
                        showInfo={false}
                        strokeColor={getScoreColor(factor.score)}
                        style={{ marginBottom: 8 }}
                      />
                      {factor.breakdown.message ? (
                        <Text type="secondary">{factor.breakdown.message}</Text>
                      ) : (
                        <ul style={{ paddingLeft: 20, margin: 0 }}>
                          {Object.entries(factor.breakdown).map(([key, value]) => (
                            <li key={key}>
                              <Text strong>{key}:</Text> {value.value} - <Text type="secondary">{value.explanation}</Text>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        </div>
      ))}
    </Card>
  );
};

export default StrategicScoreBreakdown;
