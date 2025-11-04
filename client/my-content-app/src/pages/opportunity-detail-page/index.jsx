import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Layout, Spin, Alert, Row, Col, Tabs } from 'antd';
import { useOpportunityData } from './hooks/useOpportunityData';
import OpportunityHeader from './components/OpportunityHeader';
import ActionCenter from './components/ActionCenter';
import ExecutiveSummary from './components/ExecutiveSummary';
import KeywordMetrics from './components/KeywordMetrics';
import StrategicScoreBreakdown from './components/StrategicScoreBreakdown';
import SerpAnalysis from './components/SerpAnalysis';
import ContentBlueprint from './components/ContentBlueprint';
import ArticlePreview from './components/ArticlePreview';
import ContentAuditCard from './components/ContentAuditCard';
import SocialMediaTab from './components/SocialMediaTab';
import VerdictCard from './components/VerdictCard';
import FactorsCard from './components/FactorsCard';
import RecommendedStrategyCard from './components/RecommendedStrategyCard';
import StrategicNotes from './components/StrategicNotes';
import CompetitorBacklinks from './components/CompetitorBacklinks';
import IntentAnalysis from './components/IntentAnalysis';
import SerpVitals from './components/SerpVitals';
import GrowthTrend from './components/GrowthTrend';

import WorkflowTracker from './components/WorkflowTracker';

const { TabPane } = Tabs;

const OpportunityDetailPageV2 = () => {
  const { opportunityId } = useParams();
  const { opportunity, isLoading, isError, error, refetch } = useOpportunityData(opportunityId);
  const [blueprintOverrides, setBlueprintOverrides] = useState(null);

  useEffect(() => {
    if (opportunity?.blueprint?.content_intelligence?.article_structure) {
      setBlueprintOverrides(opportunity.blueprint.content_intelligence.article_structure);
    }
  }, [opportunity]);

  if (isLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Spin tip="Loading opportunity..." size="large" />
      </div>
    );
  }

  if (isError) {
    return <Alert message="Error" description={error.message} type="error" showIcon />;
  }

  if (!opportunity) {
    return null;
  }

  const { blueprint, ai_content, social_media_posts_json, score_breakdown, full_data } = opportunity;

  return (
    <Layout style={{ padding: '24px', background: '#f0f2f5' }}>
      <OpportunityHeader
        keyword={opportunity.keyword}
        strategicScore={opportunity.strategic_score}
        status={opportunity.status}
        dateAdded={opportunity.date_added}
        recommendation={blueprint?.final_qualification_assessment?.recommendation}
      />
      <ActionCenter 
        status={opportunity.status} 
        opportunityId={opportunity.id} 
        overrides={blueprintOverrides} 
        refetch={refetch}
        style={{ marginTop: 24, marginBottom: 24 }}
      />
      <WorkflowTracker opportunity={opportunity} />
      <Tabs defaultActiveKey="1">
        <TabPane tab="Overview" key="1">
          <Row gutter={[24, 24]}>
            <Col xs={24} lg={8}>
              <VerdictCard 
                recommendation={blueprint?.final_qualification_assessment?.recommendation}
                confidenceScore={blueprint?.final_qualification_assessment?.confidence_score}
              />
              <RecommendedStrategyCard strategy={blueprint?.recommended_strategy} />
              <KeywordMetrics 
                keywordInfo={opportunity.keyword_info} 
                keywordProperties={opportunity.keyword_properties}
              />
              <IntentAnalysis searchIntentInfo={opportunity.search_intent_info} />
              <GrowthTrend scoreBreakdown={score_breakdown} />
            </Col>
            <Col xs={24} lg={16}>
              <StrategicNotes notes={blueprint?.analysis_notes} />
              <FactorsCard 
                positiveFactors={blueprint?.final_qualification_assessment?.positive_factors}
                negativeFactors={blueprint?.final_qualification_assessment?.negative_factors}
              />
              <ExecutiveSummary summary={blueprint?.executive_summary} />
              <StrategicScoreBreakdown scoreBreakdown={score_breakdown} />
              <CompetitorBacklinks avgBacklinksInfo={full_data?.avg_backlinks_info} />
              <SerpVitals scoreBreakdown={score_breakdown} />
            </Col>
          </Row>
        </TabPane>
        <TabPane tab="SERP Analysis" key="2">
          <SerpAnalysis blueprint={blueprint} />
        </TabPane>
        <TabPane tab="Content Blueprint" key="3">
          <ContentBlueprint
            blueprint={blueprint}
            overrides={blueprintOverrides}
            setOverrides={setBlueprintOverrides}
          />
        </TabPane>
        <TabPane tab="Publishing" key="4">
          <Tabs defaultActiveKey="article">
            <TabPane tab="Article" key="article">
              <ArticlePreview
                aiContent={ai_content}
                finalPackage={opportunity.final_package_json}
              />
            </TabPane>
            <TabPane tab="Social Media" key="social">
              <SocialMediaTab socialMediaPosts={social_media_posts_json} />
            </TabPane>
          </Tabs>
        </TabPane>
        <TabPane tab="Audit" key="5">
          <ContentAuditCard auditResults={ai_content?.audit_results} />
        </TabPane>
      </Tabs>
    </Layout>
  );
};

export default OpportunityDetailPageV2;
