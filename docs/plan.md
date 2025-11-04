Here is the complete, granular, and explicit implementation plan for the first six tasks. This plan is designed for an AI coding agent to execute, with step-by-step instructions and all necessary code changes, including ripple effects, to ensure a robust and functional solution for real-world usage.

---

### **Task 1: Revamp the Discovery Form for Strategic Control**

**High-Level Goal:** Transform the static `DiscoveryForm` into a dynamic control panel that allows users to configure the `limit`, `depth`, and `exact_match` for each discovery run, and allows for multiple seed keywords.

| # | Sub-Task | Category | Description |
| :-- | :--- | :--- | :--- |
| 1.1 | **Add `Select mode="tags"` for Seed Keywords, Advanced UI Sections & Dynamic Controls** | Frontend | Replaces the simple input for seed keywords with a multi-tag selector, introduces an Ant Design `Collapse` for advanced settings, and adds controls (`InputNumber`, `Slider`, `Switch`) for `limit`, `depth`, and `exact_match`. Includes client-side validation. |
| 1.2 | **Connect Global Settings to Form Defaults (`DiscoveryPage.jsx`)** | Frontend | Modifies `DiscoveryPage.jsx` to fetch client settings and pass them to the form, ensuring initial values reflect saved preferences. |
| 1.3 | **Update Form Submission Logic (`DiscoveryForm.jsx`)** | Frontend | Adjusts `DiscoveryForm.jsx`'s `onFinish` handler to correctly gather and send all new form values to the backend. (Covered in 1.1's code) |
| 1.4 | **Update Discovery History Display (`RunDetailsModal.jsx`)** | Frontend | Modifies `RunDetailsModal.jsx` to show the newly added dynamic parameters for each historical run. |
| 1.5 | **Add `discovery_max_pages`, `discovery_related_depth`, `discovery_exact_match` to `client_settings` Table** | Database | Creates new columns in the `client_settings` table to persist these user-configurable defaults. |
| 1.6 | **Update `ConfigManager` to Load/Save New Settings** | Backend Config | Modifies `app_config/manager.py` to correctly parse and manage the new settings from `settings.ini`. |
| 1.7 | **Update `DatabaseManager` to Handle New Settings** | Backend DB | Updates `DatabaseManager.get_client_settings` and `update_client_settings` to correctly read from and write to the new `client_settings` columns. |

#### **Granular Code Implementation for Task 1**

**Sub-Task 1.1, 1.3: Revamp Discovery Form (`DiscoveryForm.jsx`)**

**File to Modify:** `my-content-app/src/pages/DiscoveryPage/components/DiscoveryForm.jsx`

**Instructions:** Replace the entire content of `my-content-app/src/pages/DiscoveryPage/components/DiscoveryForm.jsx` with the following code.

```javascript
import React from 'react';
import { Input, Button, Typography, Form, Row, Col, InputNumber, Select, Card, Tooltip, Divider, Collapse, Slider, Switch, Space } from 'antd';
import { RocketOutlined, QuestionCircleOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;
const { Panel } = Collapse;

const DiscoveryForm = ({ isSubmitting, onSubmit, settings, isLoadingSettings }) => {
  const [form] = Form.useForm();

  // Set initial values from settings once they are loaded
  React.useEffect(() => {
    if (settings) {
      form.setFieldsValue({
        limit: settings.discovery_max_pages || 100, // Default to 100 if not set in DB/config
        depth: settings.discovery_related_depth || 1, // Default to 1 if not set
        exact_match: settings.discovery_exact_match || false, // Default to false if not set
        // Add other initial values from settings here if needed
      });
    }
  }, [settings, form]);

  const onFinish = (values) => {
    const { seed_keywords, filters_simple, limit, depth, exact_match } = values;

    const runData = {
      seed_keywords: seed_keywords,
      filters: filters_simple || [], // Placeholder for eventual FilterBuilder integration
      limit: limit,
      depth: depth,
      exact_match: exact_match,
      // Add other advanced parameters here as they are added to the form
    };
    
    onSubmit({ runData });
  };

  return (
    <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{
      // Default values before settings are loaded
      limit: 100,
      depth: 1,
      exact_match: false,
    }}>
      <Title level={3}>Start a New Discovery Run</Title>
      <Text type="secondary" style={{ marginBottom: '24px', display: 'block' }}>
        Enter one or more seed keywords to begin exploring related content opportunities.
      </Text>

      <Form.Item 
        name="seed_keywords" 
        rules={[{ required: true, message: 'Please enter at least one seed keyword.' }]}
        label={<Title level={4}>Seed Keywords</Title>}
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Type a keyword and press Enter (e.g., 'AI in marketing')"
          size="large"
          tokenSeparators={[',']}
        />
      </Form.Item>
      
      <Collapse ghost>
        <Panel header="Advanced Run Settings" key="1">
            <Row gutter={24}>
              <Col xs={24} sm={12}>
                <Form.Item 
                  name="limit" 
                  label={
                    <Space>
                      Max Keywords per Source
                      <Tooltip title="Set the maximum number of keywords to fetch from each API source (max 1000). Higher values increase cost and discovery breadth.">
                        <QuestionCircleOutlined />
                      </Tooltip>
                    </Space>
                  }
                  rules={[{ required: true, message: 'Limit is required.'}, { type: 'number', min: 10, max: 1000, message: 'Limit must be between 10 and 1000.'}]}
                >
                  <InputNumber style={{ width: '100%' }} min={10} max={1000} step={50} />
                </Form.Item>
              </Col>
              <Col xs={24} sm={12}>
                <Form.Item 
                  name="depth" 
                  label={
                    <Space>
                      Related Keywords Depth
                      <Tooltip title="Set the discovery depth for the 'Related Keywords' API. A higher depth (max 4) finds exponentially more niche keywords but increases cost.">
                        <QuestionCircleOutlined />
                      </Tooltip>
                    </Space>
                  }
                  rules={[{ required: true, message: 'Depth is required.'}, { type: 'number', min: 1, max: 4, message: 'Depth must be between 1 and 4.'}]}
                >
                  <Slider min={1} max={4} marks={{ 1: 'Shallow', 2: 'Medium', 3: 'Deep', 4: 'Max' }} />
                </Form.Item>
              </Col>
              <Col xs={24} sm={12}>
                <Form.Item 
                  name="exact_match" 
                  label={
                    <Space>
                      Use Exact Match (for Suggestions)
                      <Tooltip title="If enabled, the 'Keyword Suggestions' API will only return phrases that contain your exact seed keyword. Disable for broader, semantic suggestions.">
                        <QuestionCircleOutlined />
                      </Tooltip>
                    </Space>
                  }
                  valuePropName="checked"
                >
                  <Switch />
                </Form.Item>
              </Col>
            </Row>
        </Panel>
      </Collapse>

      <Form.Item style={{ marginTop: '32px', marginBottom: 0 }}>
        <Button type="primary" htmlType="submit" icon={<RocketOutlined />} loading={isSubmitting} size="large" block>
          Find Opportunities
        </Button>
      </Form.Item>
    </Form>
  );
};

export default DiscoveryForm;
```

**Sub-Task 1.2: Connect Global Settings to Form Defaults (`DiscoveryPage.jsx`)**

**File to Modify:** `my-content-app/src/pages/DiscoveryPage/DiscoveryPage.jsx`

**Instructions:** Replace the entire content of `my-content-app/src/pages/DiscoveryPage/DiscoveryPage.jsx` with the following code.

```javascript
import React, { useState } from 'react';
import { Layout, Typography, Spin, Alert, Card, Divider } from 'antd';
import { useQuery } from 'react-query'; // Import useQuery
import { useDiscoveryRuns } from './hooks/useDiscoveryRuns';
import DiscoveryForm from './components/DiscoveryForm';
import DiscoveryHistory from './components/DiscoveryHistory';
import { useClient } from '../../hooks/useClient';
import { getClientSettings } from '../../services/clientSettingsService'; // Import the service
import useDebounce from '../../hooks/useDebounce';

const { Content } = Layout;
const { Title } = Typography;

const DiscoveryPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [dateRange, setDateRange] = useState(null);
  const debouncedSearchQuery = useDebounce(searchQuery, 500);

  const { runs, totalRuns, page, setPage, isLoading, isError, error, startRunMutation, rerunMutation } = useDiscoveryRuns(debouncedSearchQuery, dateRange);
  const { clientId } = useClient();

  // Fetch client settings to use as defaults for the form
  const { data: clientSettings, isLoading: isLoadingSettings } = useQuery(
    ['clientSettings', clientId],
    () => getClientSettings(clientId),
    {
      enabled: !!clientId,
      staleTime: 5 * 60 * 1000, // Cache settings for 5 minutes
    }
  );

  const handleRerun = (runId) => {
      rerunMutation.mutate(runId);
  }

  const handleSearchChange = (query) => {
    setSearchQuery(query);
    setPage(1);
  };

  const handleDateChange = (dates) => {
    setDateRange(dates);
    setPage(1);
  };

  if (isLoading || isLoadingSettings) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Spin size="large" tip="Loading Discovery Hub..." />
      </div>
    );
  }

  if (isError) {
    return (
        <Alert
            message="Error"
            description={error.message || "Failed to load discovery run history. Please try again."}
            type="error"
            showIcon
            style={{ margin: '16px' }}
        />
    );
  }

  return (
    <Layout style={{ padding: '24px', background: '#f0f2f5' }}>
      <Content style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <Spin spinning={startRunMutation.isLoading} tip="Starting discovery run..." size="large">
          <Title level={2} style={{ marginBottom: '24px' }}>Discovery Hub</Title>
          <Card style={{ marginBottom: '32px', boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)' }}>
            <DiscoveryForm
              isSubmitting={startRunMutation.isLoading}
              onSubmit={({ runData }) => {
                startRunMutation.mutate({ clientId, runData });
              }}
              settings={clientSettings}
              isLoadingSettings={isLoadingSettings}
            />
          </Card>

          <Divider />

          <DiscoveryHistory
              runs={runs}
              totalRuns={totalRuns}
              page={page}
              setPage={setPage}
              isLoading={isLoading || startRunMutation.isLoading || rerunMutation.isLoading}
              onRerun={handleRerun}
              isRerunning={rerunMutation.isLoading}
              searchQuery={searchQuery}
              setSearchQuery={handleSearchChange}
              setDateRange={handleDateChange}
          />
        </Spin>
      </Content>
    </Layout>
  );
};

export default DiscoveryPage;
```

**Sub-Task 1.4: Update Discovery History Display (`RunDetailsModal.jsx`)**

**File to Modify:** `my-content-app/src/pages/DiscoveryPage/components/RunDetailsModal.jsx`

**Instructions:** Replace the entire content of `my-content-app/src/pages/DiscoveryPage/components/RunDetailsModal.jsx` with the following code.

```javascript
import React from 'react';
import { Modal, Tag, Row, Col, Descriptions, Statistic, Steps, Card, Typography } from 'antd';
import { formatDistanceStrict } from 'date-fns';
import PieChartCard from './PieChartCard';
import DiscoveryStatsBreakdown from './DiscoveryStatsBreakdown'; 

const { Title, Text } = Typography;
const { Step } = Steps;

const STATUS_CONFIG = {
  completed: { color: 'success', text: 'Completed' },
  failed: { color: 'error', text: 'Failed' },
  running: { color: 'processing', text: 'Running' },
  pending: { color: 'default', text: 'Pending' },
};

const RunDetailsModal = ({ run, open, onCancel }) => {
  if (!run) return null;

  const {
    id,
    start_time,
    end_time,
    status,
    parameters = {},
    results_summary = {},
  } = run;

  const {
    total_cost = 0,
    source_counts = {},
    total_raw_count = 0,
    total_unique_count = 0,
    final_qualified_count = 0,
    duplicates_removed = 0,
    final_added_to_db = 0,
    disqualification_reasons = {},
  } = results_summary;

  const statusInfo = STATUS_CONFIG[status] || STATUS_CONFIG.pending;

  const expandedRowRender = (record) => {
    if (!record.results_summary) {
      return <Text type="secondary">No detailed summary available for this run.</Text>;
    }
    return <DiscoveryStatsBreakdown summary={record.results_summary} runId={record.id} />;
  };

  return (
    <Modal
      title={
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Title level={4} style={{ margin: 0 }}>Discovery Run #{id}</Title>
          <Tag color={statusInfo.color} style={{ marginLeft: '12px' }}>{statusInfo.text}</Tag>
        </div>
      }
      open={open}
      onCancel={onCancel}
      footer={null}
      width="80vw"
      style={{ top: 20 }}
    >
      {/* Key Metrics */}
      <Row gutter={[32, 16]} style={{ marginBottom: '24px' }}>
        <Col><Statistic title="Total Cost" prefix="$" value={total_cost.toFixed(2)} /></Col>
        <Col><Statistic title="Run Duration" value={end_time ? formatDistanceStrict(new Date(end_time), new Date(start_time)) : 'N/A'} /></Col>
        <Col><Statistic title="Keywords Found" value={total_unique_count} /></Col>
        <Col><Statistic title="Added to Pipeline" value={final_added_to_db} valueStyle={{ color: '#3f8600' }} /></Col>
      </Row>

      {/* Processing Funnel */}
      <Card title="Processing Funnel" style={{ marginBottom: '24px' }}>
        <Steps current={5} size="small">
          <Step title="Total Found" description={`${total_raw_count.toLocaleString()}`} />
          <Step title="Unique" description={`${total_unique_count.toLocaleString()}`} />
          <Step title="Qualified" description={`${final_qualified_count.toLocaleString()}`} />
          <Step title="Duplicates Removed" description={`${duplicates_removed.toLocaleString()}`} />
          <Step title="Added to DB" description={<Text strong style={{color: '#3f8600'}}>{final_added_to_db.toLocaleString()}</Text>} />
        </Steps>
      </Card>

      <Row gutter={[24, 24]}>
        {/* Parameters */}
        <Col xs={24} lg={8}>
          <Card title="Run Parameters">
            <Descriptions bordered column={1} size="small">
              <Descriptions.Item label="Seed Keywords">
                {(parameters.seed_keywords || []).map(kw => <Tag key={kw}>{kw}</Tag>)}
              </Descriptions.Item>
              <Descriptions.Item label="Discovery Modes">
                {(parameters.discovery_modes || []).map(mode => <Tag key={mode} color="blue">{mode.replace(/_/g, ' ')}</Tag>)}
              </Descriptions.Item>
              <Descriptions.Item label="Max Keywords per Source">{parameters.limit || 'Default'}</Descriptions.Item>
              <Descriptions.Item label="Related Keywords Depth">{parameters.depth || 'Default'}</Descriptions.Item>
              <Descriptions.Item label="Use Exact Match (Suggestions)">
                {parameters.exact_match ? 'Enabled' : 'Disabled'}
              </Descriptions.Item>
              <Descriptions.Item label="Ignore Synonyms">
                {parameters.ignore_synonyms ? 'Enabled' : 'Disabled'}
              </Descriptions.Item>
              <Descriptions.Item label="Closely Variants">
                {parameters.closely_variants ? 'Enabled' : 'Disabled'}
              </Descriptions.Item>
              <Descriptions.Item label="Include Clickstream Data">
                {parameters.include_clickstream_data ? 'Enabled' : 'Disabled'}
              </Descriptions.Item>
              {Object.entries(parameters.filters_override || {}).map(([key, value]) => (
                <Descriptions.Item key={key} label={key.replace(/_/g, ' ')}>{String(value)}</Descriptions.Item>
              ))}
            </Descriptions>
          </Card>
        </Col>

        {/* Visualizations */}
        <Col xs={24} lg={16}>
          <Row gutter={[24, 24]}>
            <Col xs={24} md={12}>
              <PieChartCard title="Keyword Sources" data={source_counts} />
            </Col>
            <Col xs={24} md={12}>
              <PieChartCard title="Disqualification Reasons" data={disqualification_reasons} />
            </Col>
          </Row>
        </Col>
      </Row>
    </Modal>
  );
};

export default RunDetailsModal;
```

**Sub-Task 1.5: Add `discovery_max_pages`, `discovery_related_depth`, `discovery_exact_match` to `client_settings` Table**

**File to Modify:** `backend/data_access/migrations/028_add_ai_topic_clusters.sql` (or `029_add_discovery_settings_to_client_settings.sql` if 028 is already applied)

**Instructions:** Add the following lines to update the `client_settings` table.

```sql
-- backend/data_access/migrations/028_add_ai_topic_clusters.sql (if you want to use this or a new file)

-- Assuming previous migration added ai_topic_clusters and is_question
ALTER TABLE opportunities ADD COLUMN ai_topic_clusters TEXT;
ALTER TABLE opportunities ADD COLUMN is_question BOOLEAN DEFAULT FALSE;

-- NEW COLUMNS FOR CLIENT_SETTINGS
ALTER TABLE client_settings ADD COLUMN discovery_max_pages INTEGER DEFAULT 100;
ALTER TABLE client_settings ADD COLUMN discovery_related_depth INTEGER DEFAULT 1;
ALTER TABLE client_settings ADD COLUMN discovery_exact_match BOOLEAN DEFAULT FALSE;
```

**Sub-Task 1.6: Update `ConfigManager` to Load/Save New Settings**

**File to Modify:** `backend/app_config/manager.py`

**Instructions:** Add the new settings to the `_setting_types` dictionary. This ensures they are correctly parsed from `settings.ini`.

**Inside the `_setting_types` dictionary, add the following lines:**
```python
    _setting_types = {
        # ... existing integer types ...
        "discovery_max_pages": int, # NEW
        "discovery_related_depth": int, # NEW
        # ... existing boolean types ...
        "discovery_exact_match": bool, # NEW
        # ... rest of _setting_types ...
    }
```
**No direct code change is needed in `_load_and_validate_global` as the generic logic for `getboolean`, `getint` etc. handles these types if defined in `settings.ini`.**

**Sub-Task 1.7: Update `DatabaseManager` to Handle New Settings**

**File to Modify:** `backend/data_access/database_manager.py`

**Instructions:** Modify the `get_client_settings` method to correctly retrieve and convert the new boolean and integer types from the database.

**In `DatabaseManager.get_client_settings`, within the `if row:` block, add `discovery_exact_match` to the `bool_keys` list and `discovery_max_pages`, `discovery_related_depth` to the `int_keys` list.**

**Locate the `bool_keys` list definition:**
```python
                bool_keys = [
                    "enforce_intent_filter",
                    "require_question_keywords",
                    "use_pexels_first",
                    "cleanup_local_images",
                    "onpage_enable_javascript",
                    "onpage_load_resources",
                    "calculate_rectangles",
                    "onpage_disable_cookie_popup",
                    "onpage_return_despite_timeout",
                    "onpage_enable_browser_rendering",
                    "onpage_store_raw_html",
                    "onpage_validate_micromarkup",
                    "discovery_replace_with_core_keyword",
                    "discovery_ignore_synonyms",
                    "enable_automated_internal_linking",
                ]
```
**And replace it with this:**
```python
                bool_keys = [
                    "enforce_intent_filter",
                    "require_question_keywords",
                    "use_pexels_first",
                    "cleanup_local_images",
                    "onpage_enable_javascript",
                    "onpage_load_resources",
                    "calculate_rectangles",
                    "onpage_disable_cookie_popup",
                    "onpage_return_despite_timeout",
                    "onpage_enable_browser_rendering",
                    "onpage_store_raw_html",
                    "onpage_validate_micromarkup",
                    "discovery_replace_with_core_keyword",
                    "discovery_ignore_synonyms",
                    "enable_automated_internal_linking",
                    "discovery_exact_match", # NEW
                ]
```

**Locate the `int_keys` list definition:**
```python
                int_keys = [
                    "num_in_article_images",
                    "location_code",
                    # ... existing integer keys ...
                ]
```
**And replace it with this:**
```python
                int_keys = [
                    "num_in_article_images",
                    "location_code",
                    "serp_freshness_old_threshold_days",
                    "min_competitor_word_count",
                    "max_competitor_technical_warnings",
                    "num_competitors_to_analyze",
                    "num_common_headings",
                    "num_unique_angles",
                    "max_initial_serp_urls_to_analyze",
                    "min_search_volume",
                    "max_keyword_difficulty",
                    "people_also_ask_click_depth",
                    "onpage_max_domains_per_request",
                    "onpage_max_tasks_per_request",
                    "ease_of_ranking_weight",
                    "traffic_potential_weight",
                    "commercial_intent_weight",
                    "growth_trend_weight",
                    "serp_features_weight",
                    "serp_freshness_weight",
                    "serp_volatility_weight",
                    "competitor_weakness_weight",
                    "max_sv_for_scoring",
                    "max_domain_rank_for_scoring",
                    "max_referring_domains_for_scoring",
                    "serp_volatility_stable_threshold_days",
                    "discovery_related_depth",
                    "max_avg_referring_domains_filter",
                    "yearly_trend_decline_threshold",
                    "quarterly_trend_decline_threshold",
                    "max_kd_hard_limit",
                    "max_referring_main_domains_limit",
                    "max_avg_domain_rank_threshold",
                    "min_keyword_word_count",
                    "max_keyword_word_count",
                    "crowded_serp_features_threshold",
                    "min_serp_stability_days",
                    "max_non_blog_results",
                    "max_ai_overview_words",
                    "max_first_organic_y_pixel",
                    "max_words_for_ai_analysis",
                    "max_avg_lcp_time",
                    "discovery_max_pages", # NEW
                    "discovery_related_depth", # NEW
                ]
```
**No explicit change is needed for `update_client_settings` as its logic to update `client_settings` using a loop over `settings.items()` already handles arbitrary key-value pairs if the column exists.**

---

### **Task 2: Decouple and Dynamize the Backend Discovery Endpoint**

**High-Level Goal:** Re-engineer the backend to stop using hardcoded limits and instead honor the dynamic, per-run parameters sent from the revamped frontend.

| # | Sub-Task | Category | Description |
| :-- | :--- | :--- | :--- |
| 2.1 | **Update API Data Model (`DiscoveryRunRequest`)** | Backend API | Expands the Pydantic model to include `limit`, `depth`, `exact_match`, and other new dynamic parameters, with server-side validation. |
| 2.2 | **Update API Endpoint Logic (`start_discovery_run_async`)** | Backend API | Modifies the endpoint to read all new parameters directly from the request body. |
| 2.3 | **Remove Hardcoded Limits in DataForSEO Client** | Backend Logic | Deletes obsolete `KEYWORD_IDEAS_MODE_LIMIT`, `KEYWORD_SUGGESTIONS_MODE_LIMIT`, `RELATED_KEYWORDS_MODE_LIMIT` constants. |
| 2.4 | **Propagate Dynamic Parameters Through Orchestrator** | Backend Logic | Ensures the `run_discovery_and_save` method in `discovery_orchestrator.py` correctly receives and passes all dynamic parameters to the background job. |
| 2.5 | **Update DataForSEO Client to Use Dynamic Parameters** | Backend Logic | Modifies the `get_keyword_ideas` method in `dataforseo_client_v2.py` to directly use the dynamic `limit` and `depth` values received from the orchestrator. |
| 2.6 | **Update `_run_discovery_background` Signature** | Backend Logic | The `_run_discovery_background` method also needs to accept all the new dynamic parameters to pass them down the chain. |
| 2.7 | **Update Re-run Logic to Persist All Parameters** | Backend API | Ensures that "re-running" a job correctly extracts and re-uses all dynamic parameters from the previous run. |

#### **Granular Code Implementation for Task 2**

**Sub-Task 2.1: Update API Data Model (`DiscoveryRunRequest` in `api/models.py`)**

**File to Modify:** `backend/api/models.py`

**Instructions:** Replace the entire `DiscoveryRunRequest` class with the following code. This adds `limit`, `depth`, `exact_match` with validation rules and sane defaults.

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class DiscoveryCostParams(BaseModel):
    seed_keywords: List[str]
    discovery_modes: Optional[List[str]] = ["keyword_ideas", "keyword_suggestions", "related_keywords"]
    limit: Optional[int] = Field(100, ge=10, le=1000, description="Maximum number of keywords to return from each API source.")
    depth: Optional[int] = Field(1, ge=1, le=4, description="Discovery depth for 'Related Keywords' API (1-4).")
    exact_match: Optional[bool] = Field(False, description="If true, 'Keyword Suggestions' will only return exact phrase matches.")
    # Add other dynamic parameters that might be needed for cost estimation
    ignore_synonyms: Optional[bool] = Field(False, description="If true, exclude highly similar keywords from results.")
    include_clickstream_data: Optional[bool] = Field(False, description="If true, include clickstream-based metrics (doubles cost).")
    closely_variants: Optional[bool] = Field(False, description="If true, 'Keyword Ideas' uses phrase-match algorithm; otherwise, broad-match.")


class ContentUpdatePayload(BaseModel):
    article_body_html: str = Field(
        ..., description="The new HTML content for the article body."
    )


class ImageRegenRequest(BaseModel):
    original_prompt: str
    new_prompt: str


class DiscoveryRunRequest(BaseModel):
    seed_keywords: List[str]
    discovery_modes: Optional[List[str]] = Field(["keyword_ideas", "keyword_suggestions", "related_keywords"], description="List of DataForSEO Labs discovery modes to use.")
    filters: Optional[List[Any]] = Field(None, description="List of DataForSEO API filters to apply.")
    order_by: Optional[List[str]] = Field(None, description="List of DataForSEO API sorting rules.")
    filters_override: Optional[Dict[str, Any]] = Field({}, description="Key-value pairs to override specific client settings during discovery.")
    limit: Optional[int] = Field(100, ge=10, le=1000, description="Maximum number of keywords to return from each API source.")
    depth: Optional[int] = Field(1, ge=1, le=4, description="Discovery depth for 'Related Keywords' API (1-4).")
    exact_match: Optional[bool] = Field(False, description="If true, 'Keyword Suggestions' will only return exact phrase matches.")
    ignore_synonyms: Optional[bool] = Field(False, description="If true, exclude highly similar keywords from results.")
    include_clickstream_data: Optional[bool] = Field(False, description="If true, include clickstream-based metrics (doubles cost).")
    closely_variants: Optional[bool] = Field(False, description="If true, 'Keyword Ideas' uses phrase-match algorithm; otherwise, broad-match.")


class KeywordListRequest(BaseModel):
    seed_keywords: List[str]
    include_clickstream_data: Optional[bool] = False


class JobResponse(BaseModel):
    job_id: str
    message: str
    status: Optional[str] = None
    progress: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress_log: Optional[List[Dict[str, Any]]] = None


class LoginRequest(BaseModel):
    password: str


class TemplateContent(BaseModel):
    name: str
    content: str
    description: Optional[str] = None


class TemplateResponse(BaseModel):
    name: str
    content: str
    description: Optional[str] = None
    last_updated: str


class PromptPreviewRequest(BaseModel):
    custom_template_content: Optional[str] = None


class PromptPreviewResponse(BaseModel):
    prompt: str


class ContentHistoryItem(BaseModel):
    id: int
    opportunity_id: int
    timestamp: str
    ai_content_json: Dict[str, Any]


class RestoreRequest(BaseModel):
    version_timestamp: str


class SingleImageRegenRequest(BaseModel):
    opportunity_id: int
    original_prompt: str
    new_prompt: str


class AutoWorkflowRequest(BaseModel):
    override_validation: bool = False


class SocialMediaPostsUpdate(BaseModel):
    social_media_posts: List[Dict[str, Any]]


class GlobalSettingsUpdate(BaseModel):
    settings: Dict[str, Any]


class OpportunityListResponse(BaseModel):
    items: List[Dict[str, Any]]
    total_items: int
    page: int
    limit: int


class AnalysisRequest(BaseModel):
    selected_competitor_urls: Optional[List[str]] = None


class RefineContentRequest(BaseModel):
    html_content: str
    command: str


class ClientSettings(BaseModel):
    brand_tone: Optional[str] = None
    target_audience: Optional[str] = None
    terms_to_avoid: Optional[str] = None


class GenerationOverrides(BaseModel):
    target_word_count: Optional[int] = None
    expert_persona: Optional[str] = None
    additional_instructions: Optional[str] = None


class ApproveAnalysisRequest(BaseModel):
    overrides: Optional[GenerationOverrides] = None
```

**Sub-Task 2.2: Update API Endpoint Logic (`start_discovery_run_async` in `api/routers/discovery.py`)**

**File to Modify:** `backend/api/routers/discovery.py`

**Instructions:** Replace the entire `start_discovery_run_async` function with the provided code. This uses the dynamic values from the request and removes hardcoded ones.

```python
import logging
from fastapi import APIRouter, Depends, HTTPException
from data_access.database_manager import DatabaseManager
from backend.pipeline import WorkflowOrchestrator
from services.discovery_service import DiscoveryService
from ..dependencies import get_db, get_orchestrator, get_discovery_service
from ..models import (
    JobResponse,
    DiscoveryRunRequest,
)

router = APIRouter()
logger = logging.getLogger(__name__)

# ... (get_available_filters remains unchanged) ...

@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    try:
        # Directly use validated and defaulted parameters from the Pydantic model
        parameters = {
            "seed_keywords": request.seed_keywords,
            "discovery_modes": request.discovery_modes,
            "filters": request.filters,
            "order_by": request.order_by,
            "filters_override": request.filters_override,
            "limit": request.limit,
            "depth": request.depth,
            "exact_match": request.exact_match,
            "closely_variants": request.closely_variants,
            "ignore_synonyms": request.ignore_synonyms,
            "include_clickstream_data": request.include_clickstream_data,
        }

        # Create a record of the run with its parameters before starting the job
        run_id = discovery_service.create_discovery_run(
            client_id=client_id, parameters=parameters
        )

        # Pass all dynamic parameters to the orchestrator's job function
        job_id = orchestrator.run_discovery_and_save(
            run_id=run_id,
            seed_keywords=request.seed_keywords,
            discovery_modes=request.discovery_modes,
            filters=request.filters,
            order_by=request.order_by,
            filters_override=request.filters_override,
            limit=request.limit,
            depth=request.depth,
            ignore_synonyms=request.ignore_synonyms,
            include_clickstream_data=request.include_clickstream_data,
            closely_variants=request.closely_variants,
            exact_match=request.exact_match,
        )
        return {"job_id": job_id, "message": f"Discovery run job {job_id} started."}
    except Exception as e:
        logger.error(
            f"Failed to start discovery run for client {client_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to start discovery run: {e}"
        )
```

**Sub-Task 2.3: Remove Hardcoded Limits in DataForSEO Client (`external_apis/dataforseo_client_v2.py`)**

**File to Modify:** `backend/external_apis/dataforseo_client_v2.py`

**Instructions:** Delete the following three lines of code from the `DataForSEOClientV2` class definition.

**Delete these lines:**
```python
    KEYWORD_IDEAS_MODE_LIMIT = 10
    KEYWORD_SUGGESTIONS_MODE_LIMIT = 100
    RELATED_KEYWORDS_MODE_LIMIT = 100
```

**Sub-Task 2.4 & 2.6: Propagate Dynamic Parameters Through Orchestrator and Update Background Job Signature (`pipeline/orchestrator/discovery_orchestrator.py`)**

**File to Modify:** `backend/pipeline/orchestrator/discovery_orchestrator.py`

**Instructions:** Replace the entire `_run_discovery_background` method definition and its call within `run_discovery_and_save`. This ensures all dynamic parameters flow correctly.

**Locate the `_run_discovery_background` method definition.**

**Replace this code block (including the method definition):**
```python
    def _run_discovery_background(
        self,
        job_id: str,
        run_id: int,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Any]],
        order_by: Optional[List[str]],
        filters_override: Optional[Dict[str, Any]],
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = None,
        include_clickstream_data: Optional[bool] = None,
        closely_variants: Optional[bool] = None,
        exact_match: Optional[bool] = None,
    ):
        """Internal method to execute the consolidated discovery phase for a job."""
        log_dir = "discovery_logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"run_{run_id}.log")

        run_logger = logging.getLogger(f"run_{run_id}")
        handler = logging.FileHandler(log_file_path)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        run_logger.addHandler(handler)
        run_logger.setLevel(logging.INFO)

        self.db_manager.update_discovery_run_log_path(run_id, log_file_path)
        self.db_manager.update_discovery_run_status(run_id, "running")
        self.job_manager.update_job_status(job_id, "running", progress=0)

        run_config = self.global_cfg_manager.load_client_config(
            self.client_id, self.db_manager
        )
        if filters_override:
            run_logger.info(f"Applying filter overrides: {filters_override}")
            run_config.update(filters_override)

        run_logger.info(
            f"Starting discovery with modes: {discovery_modes}, filters: {filters}, order_by: {order_by}, limit: {limit}, depth: {depth}"
        )

        try:
            job_status = self.job_manager.get_job_status(job_id)
            if job_status and job_status.get("status") == "failed":
                run_logger.warning(
                    f"Job {job_id} found marked as 'failed' (cancelled). Exiting gracefully."
                )
                self.db_manager.update_discovery_run_status(run_id, "cancelled")
                return {"message": "Job cancelled by user request."}
            
            self.job_manager.update_job_status(
                job_id,
                "running",
                progress=10,
                result={"step": "Fetching Keywords from API..."},
            )
            from pipeline.step_01_discovery.run_discovery import run_discovery_phase

            discovery_result = run_discovery_phase(
                seed_keywords=seed_keywords,
                dataforseo_client=self.dataforseo_client,
                db_manager=self.db_manager,
                client_id=self.client_id,
                client_cfg=run_config,
                discovery_modes=discovery_modes,
                filters=filters,
                order_by=order_by,
                limit=limit,
                depth=depth,
                ignore_synonyms=ignore_synonyms,
                include_clickstream_data=include_clickstream_data,
                closely_variants=closely_variants,
                run_logger=run_logger,
            )

            stats = discovery_result.get("stats", {})
            total_cost = discovery_result.get("total_cost", 0.0)
            processed_opportunities = discovery_result.get("opportunities", [])
            
            self.job_manager.update_job_status(
                job_id, "running", progress=75, result={"step": "Saving Results to Database..."}
            )
            
            num_added = 0
            if processed_opportunities:
                run_logger.info(
                    f"Attempting to save {len(processed_opportunities)} processed opportunities..."
                )
                num_added = self.db_manager.add_opportunities(
                    processed_opportunities, self.client_id, run_id
                )
                run_logger.info(
                    f"Successfully saved {num_added} new keyword records. The database ignored {len(processed_opportunities) - num_added} duplicates."
                )

            results_summary = {
                "total_cost": total_cost,
                "source_counts": stats.get("raw_counts", {}),
                "total_raw_count": stats.get("total_raw_count", 0),
                "total_unique_count": stats.get("total_unique_count", 0),
                "disqualification_reasons": stats.get("disqualification_reasons", {}),
                "disqualified_count": stats.get("disqualified_count", 0),
                "final_qualified_count": stats.get("final_qualified_count", 0),
                "duplicates_removed": len(processed_opportunities) - num_added,
                "final_added_to_db": num_added,
            }

            self.db_manager.update_discovery_run_completed(run_id, results_summary)
            self.job_manager.update_job_status(
                job_id, "completed", progress=100, result=results_summary
            )
            run_logger.info("Discovery run completed successfully.")
            return results_summary
        except Exception as e:
            error_message = f"Discovery workflow failed: {e}\n{traceback.format_exc()}"
            run_logger.error(error_message)
            self.db_manager.update_discovery_run_failed(run_id, str(e))
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
            # --- ADD THIS NEW BLOCK ---
            # Mark any partially processed opportunities from this run as failed.
            run_logger.info(f"Marking partially fetched opportunities from run_id {run_id} as 'failed_scoring'.")
            conn = self.db_manager._get_conn()
            with conn:
                conn.execute(
                    "UPDATE opportunities SET status = 'failed_scoring', error_message = ? WHERE run_id = ? AND status = 'fetched'",
                    (f"Parent discovery job {job_id} failed.", run_id)
                )
            # --- END NEW BLOCK ---
            raise
```
**With this code:**
```python
    def _run_discovery_background(
        self,
        job_id: str,
        run_id: int,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Any]],
        order_by: Optional[List[str]],
        filters_override: Optional[Dict[str, Any]],
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = None,
        include_clickstream_data: Optional[bool] = None,
        closely_variants: Optional[bool] = None,
        exact_match: Optional[bool] = None,
    ):
        """Internal method to execute the consolidated discovery phase for a job."""
        log_dir = "discovery_logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"run_{run_id}.log")

        run_logger = logging.getLogger(f"run_{run_id}")
        handler = logging.FileHandler(log_file_path)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        run_logger.addHandler(handler)
        run_logger.setLevel(logging.INFO)

        self.db_manager.update_discovery_run_log_path(run_id, log_file_path)
        self.db_manager.update_discovery_run_status(run_id, "running")
        self.job_manager.update_job_status(job_id, "running", progress=0)

        run_config = self.global_cfg_manager.load_client_config(
            self.client_id, self.db_manager
        )
        if filters_override:
            run_logger.info(f"Applying filter overrides: {filters_override}")
            run_config.update(filters_override)

        run_logger.info(
            f"Starting discovery with modes: {discovery_modes}, filters: {filters}, order_by: {order_by}, limit: {limit}, depth: {depth}"
        )

        try:
            job_status = self.job_manager.get_job_status(job_id)
            if job_status and job_status.get("status") == "failed":
                run_logger.warning(
                    f"Job {job_id} found marked as 'failed' (cancelled). Exiting gracefully."
                )
                self.db_manager.update_discovery_run_status(run_id, "cancelled")
                return {"message": "Job cancelled by user request."}
            
            self.job_manager.update_job_status(
                job_id,
                "running",
                progress=10,
                result={"step": "Fetching Keywords from API..."},
            )
            from pipeline.step_01_discovery.run_discovery import run_discovery_phase

            discovery_result = run_discovery_phase(
                seed_keywords=seed_keywords,
                dataforseo_client=self.dataforseo_client,
                db_manager=self.db_manager,
                client_id=self.client_id,
                client_cfg=run_config,
                discovery_modes=discovery_modes,
                filters=filters,
                order_by=order_by,
                limit=limit,
                depth=depth,
                ignore_synonyms=ignore_synonyms,
                include_clickstream_data=include_clickstream_data,
                closely_variants=closely_variants,
                exact_match=exact_match, # NEW: Pass exact_match
                run_logger=run_logger,
            )

            stats = discovery_result.get("stats", {})
            total_cost = discovery_result.get("total_cost", 0.0)
            processed_opportunities = discovery_result.get("opportunities", [])
            
            self.job_manager.update_job_status(
                job_id, "running", progress=75, result={"step": "Saving Results to Database..."}
            )
            
            num_added = 0
            if processed_opportunities:
                run_logger.info(
                    f"Attempting to save {len(processed_opportunities)} processed opportunities..."
                )
                num_added = self.db_manager.add_opportunities(
                    processed_opportunities, self.client_id, run_id
                )
                run_logger.info(
                    f"Successfully saved {num_added} new keyword records. The database ignored {len(processed_opportunities) - num_added} duplicates."
                )

            results_summary = {
                "total_cost": total_cost,
                "source_counts": stats.get("raw_counts", {}),
                "total_raw_count": stats.get("total_raw_count", 0),
                "total_unique_count": stats.get("total_unique_count", 0),
                "disqualification_reasons": stats.get("disqualification_reasons", {}),
                "disqualified_count": stats.get("disqualified_count", 0),
                "final_qualified_count": stats.get("final_qualified_count", 0),
                "duplicates_removed": len(processed_opportunities) - num_added,
                "final_added_to_db": num_added,
            }

            self.db_manager.update_discovery_run_completed(run_id, results_summary)
            self.job_manager.update_job_status(
                job_id, "completed", progress=100, result=results_summary
            )
            run_logger.info("Discovery run completed successfully.")
            return results_summary
        except Exception as e:
            error_message = f"Discovery workflow failed: {e}\n{traceback.format_exc()}"
            run_logger.error(error_message)
            self.db_manager.update_discovery_run_failed(run_id, str(e))
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
            run_logger.info(f"Marking partially fetched opportunities from run_id {run_id} as 'failed_scoring'.")
            conn = self.db_manager._get_conn()
            with conn:
                conn.execute(
                    "UPDATE opportunities SET status = 'failed_scoring', error_message = ? WHERE run_id = ? AND status = 'fetched'",
                    (f"Parent discovery job {job_id} failed.", run_id)
                )
            raise
```

**Sub-Task 2.5: Update DataForSEO Client to Use Dynamic Parameters (`external_apis/dataforseo_client_v2.py`)**

**File to Modify:** `backend/external_apis/dataforseo_client_v2.py`

**Instructions:** Modify the `get_keyword_ideas` method by replacing specific `limit` and `depth` assignments within the task dictionaries.

**Locate `get_keyword_ideas` method. Find and replace the `ideas_task` definition:**
```python
            ideas_task = {
                "keywords": seed_keywords,
                "location_code": location_code,
                "language_code": language_code,
                "limit": self.KEYWORD_IDEAS_MODE_LIMIT, # This line
                "include_serp_info": True,
                "ignore_synonyms": ignore_synonyms,
                "closely_variants": closely_variants,
                "filters": sanitized_ideas_filters,
                "order_by": order_by.get("ideas") if order_by else None,
                "include_clickstream_data": include_clickstream,
            }
```
**With this:**
```python
            ideas_task = {
                "keywords": seed_keywords,
                "location_code": location_code,
                "language_code": language_code,
                "limit": limit, # Dynamically assigned
                "include_serp_info": True,
                "ignore_synonyms": ignore_synonyms,
                "closely_variants": closely_variants,
                "filters": sanitized_ideas_filters,
                "order_by": order_by.get("ideas") if order_by else None,
                "include_clickstream_data": include_clickstream,
            }
```

**Next, find and replace the `suggestions_task` definition (within the `if "keyword_suggestions" in discovery_modes:` block):**
```python
                suggestions_task = {
                    "keyword": seed_keyword,
                    "location_code": location_code,
                    "language_code": language_code,
                    "limit": self.KEYWORD_SUGGESTIONS_MODE_LIMIT, # This line
                    "include_serp_info": True,
                    "exact_match": exact_match,
                    "ignore_synonyms": ignore_synonyms,
                    "include_seed_keyword": True,
                    "filters": self._prioritize_and_limit_filters(
                        self._convert_filters_to_api_format(filters.get("suggestions"))
                    ),
                    "order_by": order_by.get("suggestions") if order_by else None,
                    "include_clickstream_data": include_clickstream,
                }
```
**With this:**
```python
                suggestions_task = {
                    "keyword": seed_keyword,
                    "location_code": location_code,
                    "language_code": language_code,
                    "limit": limit, # Dynamically assigned
                    "include_serp_info": True,
                    "exact_match": exact_match,
                    "ignore_synonyms": ignore_synonyms,
                    "include_seed_keyword": True,
                    "filters": self._prioritize_and_limit_filters(
                        self._convert_filters_to_api_format(filters.get("suggestions"))
                    ),
                    "order_by": order_by.get("suggestions") if order_by else None,
                    "include_clickstream_data": include_clickstream,
                }
```

**Finally, find and replace the `related_task` definition (within the `if "related_keywords" in discovery_modes:` block):**
```python
                related_task = {
                    "keyword": seed,
                    "location_code": location_code,
                    "language_code": language_code,
                    "depth": 1, # This line
                    "limit": self.RELATED_KEYWORDS_MODE_LIMIT, # This line
                    "include_serp_info": True,
                    "filters": self._prioritize_and_limit_filters(
                        self._convert_filters_to_api_format(filters.get("related"))
                    ),
                    "order_by": order_by.get("related") if order_by else None,
                    "include_clickstream_data": include_clickstream,
                    "replace_with_core_keyword": client_cfg.get(
                        "discovery_replace_with_core_keyword", False
                    ),
                }
```
**With this:**
```python
                related_task = {
                    "keyword": seed,
                    "location_code": location_code,
                    "language_code": language_code,
                    "depth": depth, # Dynamically assigned
                    "limit": limit, # Dynamically assigned
                    "include_serp_info": True,
                    "filters": self._prioritize_and_limit_filters(
                        self._convert_filters_to_api_format(filters.get("related"))
                    ),
                    "order_by": order_by.get("related") if order_by else None,
                    "include_clickstream_data": include_clickstream,
                    "replace_with_core_keyword": client_cfg.get(
                        "discovery_replace_with_core_keyword", False
                    ),
                }
```

**Sub-Task 2.7: Update Re-run Logic to Persist All Parameters (`api/routers/discovery.py`)**

**File to Modify:** `backend/api/routers/discovery.py`

**Instructions:** Replace the entire `rerun_discovery_run` function with the updated version.

**Replace this code block (including the method definition):**
```python
@router.post("/discovery-runs/rerun/{run_id}")
async def rerun_discovery_run(
    run_id: int,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    db: DatabaseManager = Depends(get_db),
):
    """
    Initiates a new discovery run using the parameters from a previous run.
    """
    previous_run = db.get_discovery_run_by_id(run_id)
    if not previous_run:
        raise HTTPException(status_code=404, detail="Discovery run not found.")

    # Authorization check within the function (using orchestrator's client_id)
    if (
        previous_run["client_id"] != orchestrator.client_id
    ):  # Use orchestrator's client_id
        raise HTTPException(
            status_code=403, detail="You do not have permission to re-run this job."
        )

    try:
        parameters = previous_run.get("parameters", {})
        seed_keywords = parameters.get("seed_keywords", [])
        filters = parameters.get("filters")
        order_by = parameters.get("order_by")
        filters_override = parameters.get("filters_override", {})
        limit = parameters.get("limit")
        depth = parameters.get("depth")

        if not seed_keywords:
            raise HTTPException(
                status_code=400, detail="No seed keywords found in the original run."
            )

        # Dynamic discovery logic based on limit
        limit = limit or 1000
        discovery_modes = ["keyword_ideas", "keyword_suggestions", "related_keywords"]

        if depth is None:
            if limit <= 500:
                depth = 2
            elif limit <= 2000:
                depth = 3
            else:
                depth = 4

        # Reconstruct parameters for the new run to be created
        new_run_parameters = {
            "seed_keywords": seed_keywords,
            "discovery_modes": discovery_modes,
            "filters": filters,
            "order_by": order_by,
            "filters_override": filters_override,
            "limit": limit,
            "depth": depth,
        }

        new_run_id = orchestrator.db_manager.create_discovery_run(
            client_id=previous_run["client_id"], parameters=new_run_parameters
        )
        job_id = orchestrator.run_discovery_and_save(
            new_run_id,
            seed_keywords,
            discovery_modes,
            filters,
            order_by,
            filters_override,
            limit,
            depth,
        )

        return {
            "job_id": job_id,
            "message": f"Re-run of job {run_id} started as new job {job_id}.",
        }
    except Exception as e:
        logger.error(f"Failed to re-run discovery run {run_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start re-run: {e}")
```

**With this code:**
```python
@router.post("/discovery-runs/rerun/{run_id}")
async def rerun_discovery_run(
    run_id: int,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    db: DatabaseManager = Depends(get_db),
):
    """
    Initiates a new discovery run using the exact parameters from a previous run.
    """
    previous_run = db.get_discovery_run_by_id(run_id)
    if not previous_run:
        raise HTTPException(status_code=404, detail="Discovery run not found.")

    if previous_run["client_id"] != orchestrator.client_id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to re-run this job."
        )

    try:
        # Extract ALL parameters from the saved run data
        parameters = previous_run.get("parameters", {})
        
        # Use .get() with defaults to safely extract all required parameters
        seed_keywords = parameters.get("seed_keywords", [])
        if not seed_keywords:
            raise HTTPException(
                status_code=400, detail="No seed keywords found in the original run to re-run."
            )

        discovery_modes = parameters.get("discovery_modes", ["keyword_ideas", "keyword_suggestions", "related_keywords"]) # Default should match DiscoveryRunRequest
        filters = parameters.get("filters")
        order_by = parameters.get("order_by")
        filters_override = parameters.get("filters_override")
        limit = parameters.get("limit", 100) # Ensure defaults match DiscoveryRunRequest
        depth = parameters.get("depth", 1) # Ensure defaults match DiscoveryRunRequest
        ignore_synonyms = parameters.get("ignore_synonyms", False)
        include_clickstream_data = parameters.get("include_clickstream_data", False)
        closely_variants = parameters.get("closely_variants", False)
        exact_match = parameters.get("exact_match", False)

        # Create a new run record in the database with the old parameters
        new_run_id = db.create_discovery_run(
            client_id=previous_run["client_id"], parameters=parameters
        )
        
        # Start the new job, passing all the extracted parameters
        job_id = orchestrator.run_discovery_and_save(
            new_run_id,
            seed_keywords,
            discovery_modes,
            filters,
            order_by,
            filters_override,
            limit,
            depth,
            ignore_synonyms,
            include_clickstream_data,
            closely_variants,
            exact_match,
        )

        return {
            "job_id": job_id,
            "message": f"Re-run of job {run_id} started as new job {job_id}.",
        }
    except Exception as e:
        logger.error(f"Failed to re-run discovery run {run_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start re-run: {e}")
```

---

### **Task 3: Implement AI-Powered Topic Clustering for Content Outlining**

**High-Level Goal:** Use AI to automatically group qualified keywords into a logical structure of H2s and associated keywords, forming the basis for a single, comprehensive blog post.

| # | Sub-Task | Category | Description |
| :-- | :--- | :--- | :--- |
| 3.1 | **Create the AI Clustering Service (`ai_clustering_service.py`)** | Backend Logic | Creates a new service responsible for AI-driven keyword grouping. |
| 3.2 | **Implement the Clustering Logic** | Backend Logic | Defines the `AIClusteringService` class and its `generate_topic_clusters` method, including the OpenAI prompt and schema. |
| 3.3 | **Add `max_keywords_for_clustering` to `settings.ini`** | Config | Introduces a configurable limit for the number of keywords sent to the AI for clustering, preventing token overruns. |
| 3.4 | **Update `ConfigManager` to Load New Setting** | Backend Config | Modifies `app_config/manager.py` to correctly parse `max_keywords_for_clustering`. |
| 3.5 | **Update `WorkflowOrchestrator` Initialization** | Backend Init | Instantiates the `AIClusteringService` when the `WorkflowOrchestrator` is created. |
| 3.6 | **Integrate Clustering into the Analysis Workflow**| Backend Logic | Modifies the `analysis_orchestrator.py` to call the clustering service after `content_intelligence` synthesis, passing all qualified keywords for the run. |
| 3.7 | **Store AI-Generated Structure in Blueprint** | Backend Logic | Updates `BlueprintFactory.create_blueprint` to save the AI-generated `ai_topic_clusters` within the blueprint data and as a top-level field. |
| 3.8 | **Adapt Content Analyzer to Use Clusters** | Backend Logic | Modifies `ContentAnalyzer._build_outline_prompt` to prioritize `ai_topic_clusters` for generating the article outline. |
| 3.9 | **Adapt Prompt Assembler to Inform AI of Clusters** | Backend Logic | Modifies `PromptAssembler._build_prompt` to inject the AI-generated topic clusters into the system prompt for content generation. |
| 3.10| **Add `ai_topic_clusters` Column to Database** | Database | Creates a new JSON column in the `opportunities` table to persist the AI-generated clusters. |
| 3.11| **Update `DatabaseManager` to Handle New Column** | Backend DB | Updates `DatabaseManager.add_opportunities` to correctly save the `ai_topic_clusters` data. |
| 3.12| **Create UI Component for Clustered Keywords** | Frontend | Develops `ClusteredKeywords.jsx` to display the AI-generated H2s and their associated keywords. |
| 3.13| **Integrate `ClusteredKeywords` Component** | Frontend | Renders the new component on the `OpportunityDetailPage` within the "Content Blueprint" tab. |

#### **Granular Code Implementation for Task 3**

**Sub-Task 3.1 & 3.2: Create and Implement the `AIClusteringService` (`backend/services/ai_clustering_service.py`)**

**Action:** Create a new file `backend/services/ai_clustering_service.py`.

**Instructions:** Add the following complete code to the new file.

```python
# backend/services/ai_clustering_service.py
import logging
from typing import List, Dict, Any, Tuple
from backend.external_apis.openai_client import OpenAIClientWrapper

class AIClusteringService:
    def __init__(self, openai_client: OpenAIClientWrapper, config: Dict[str, Any]):
        self.openai_client = openai_client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    def generate_topic_clusters(self, keywords: List[str]) -> Tuple[List[Dict[str, Any]], float]:
        """
        Uses an AI model to group a list of keywords into thematic sub-topics for an article outline.
        """
        if not keywords:
            return [], 0.0

        # Truncate if the list is too long to prevent token limit errors
        max_keywords_for_clustering = self.config.get("max_keywords_for_clustering", 200)
        if len(keywords) > max_keywords_for_clustering:
            self.logger.warning(f"Keyword list for clustering is too long ({len(keywords)}). Truncating to {max_keywords_for_clustering}.")
            keywords = keywords[:max_keywords_for_clustering]

        prompt_messages = self._build_clustering_prompt(keywords)

        schema = {
            "name": "generate_keyword_clusters",
            "type": "object",
            "properties": {
                "topic_clusters": {
                    "type": "array",
                    "description": "An array of thematic topic clusters.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "topic_name": {
                                "type": "string",
                                "description": "A concise, descriptive name for the topic cluster, suitable as an H2 heading.",
                            },
                            "keywords": {
                                "type": "array",
                                "description": "A list of keywords from the original input that belong to this topic.",
                                "items": {"type": "string"},
                            },
                        },
                        "required": ["topic_name", "keywords"],
                    },
                }
            },
            "required": ["topic_clusters"],
        }

        response, error = self.openai_client.call_chat_completion(
            messages=prompt_messages,
            schema=schema,
            model=self.config.get("default_model", "gpt-5-nano"),
            temperature=0.3,
        )

        cost = self.openai_client.latest_cost

        if error or not response or "topic_clusters" not in response:
            self.logger.error(f"Failed to generate topic clusters from AI: {error}")
            return [], cost

        return response["topic_clusters"], cost

    def _build_clustering_prompt(self, keywords: List[str]) -> List[Dict[str, str]]:
        keyword_list_str = "\n".join(f"- {kw}" for kw in keywords)

        prompt = f"""
        You are an expert SEO content strategist and information architect. Your task is to analyze the following list of keywords and group them into logical, thematic sub-topics. Each sub-topic should be suitable as an H2 heading for a single, comprehensive blog post.

        **Keyword List:**
        {keyword_list_str}

        **Instructions:**
        1.  Analyze all keywords to understand the overarching theme and user intents.
        2.  Group related keywords into distinct thematic clusters.
        3.  For each cluster, create a concise and descriptive `topic_name` that would serve as an excellent H2 heading.
        4.  Ensure every keyword from the original list is assigned to exactly one cluster.
        5.  The final output must be a JSON object that strictly adheres to the provided schema.
        """
        return [{"role": "user", "content": prompt}]```

**Sub-Task 3.3: Add `max_keywords_for_clustering` to `settings.ini`**

**File to Modify:** `backend/app_config/settings.ini`

**Instructions:** Add this line to the `[ANALYSIS]` section.

```ini
[ANALYSIS]
enable_deep_competitor_analysis = false
num_competitors_for_ai_analysis = 3
serp_analysis_depth = 100
max_words_for_ai_analysis = 2000
serp_remove_from_url_params = srsltid,utm_source,ref_id
max_keywords_for_clustering = 200 ; NEW: Limit for keywords sent to AI for clustering
```

**Sub-Task 3.4: Update `ConfigManager` to Load New Setting**

**File to Modify:** `backend/app_config/manager.py`

**Instructions:** Add `max_keywords_for_clustering` to the `_setting_types` dictionary.

**Inside the `_setting_types` dictionary, add the following line:**
```python
    _setting_types = {
        # ... existing integer types ...
        "max_keywords_for_clustering": int, # NEW
        # ... rest of _setting_types ...
    }
```

**Sub-Task 3.5: Update `WorkflowOrchestrator` Initialization**

**File to Modify:** `backend/pipeline/orchestrator/main.py`

**Instructions:** Add the import for `AIClusteringService` and instantiate it in the `__init__` method.

**Add this import at the top of the file:**
```python
from backend.services.ai_clustering_service import AIClusteringService
```

**Inside the `WorkflowOrchestrator.__init__` method, after `self.scoring_engine = ScoringEngine(self.client_cfg)` (or similar existing instantiations), add:**
```python
        self.ai_clustering_service = AIClusteringService(self.openai_client, self.client_cfg)
```

**Sub-Task 3.6: Integrate Clustering into the Analysis Workflow (`analysis_orchestrator.py`)**

**File to Modify:** `backend/pipeline/orchestrator/analysis_orchestrator.py`

**Instructions:** Modify the `run_analysis_phase` method to call the `AIClusteringService` and pass its results to the `blueprint_factory`.

**Find this block (within `run_analysis_phase`):**
```python
            # 5. Determine Strategy & Generate Outline
            from pipeline.step_05_strategy.decision_engine import (
                StrategicDecisionEngine,
            )

            strategy_engine = StrategicDecisionEngine(self.client_cfg)
            recommended_strategy = strategy_engine.determine_strategy(
                live_serp_data, competitor_analysis, content_intelligence
            )

            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
                keyword, live_serp_data, content_intelligence
            )
            total_api_cost += outline_api_cost
            content_intelligence.update(ai_outline)

            if not content_intelligence.get("article_structure"):
                self.logger.critical(
                    f"AI outline generation failed to produce an 'article_structure' for keyword: {keyword}."
                )
                raise ValueError("AI outline generation failed.")

            # 6. Assemble and Save Blueprint & Re-Score
            analysis_data = {
                "serp_overview": live_serp_data,
                "competitor_analysis": competitor_analysis,
                "content_intelligence": content_intelligence,
                "recommended_strategy": recommended_strategy,
            }
```
**With this code:**
```python
            # 5. Determine Strategy & Generate Outline
            from pipeline.step_05_strategy.decision_engine import (
                StrategicDecisionEngine,
            )

            strategy_engine = StrategicDecisionEngine(self.client_cfg)
            recommended_strategy = strategy_engine.determine_strategy(
                live_serp_data, competitor_analysis, content_intelligence
            )

            # NEW: Generate Topic Clusters using all qualified keywords from this run
            # Fetch all qualified keywords associated with this run from the DB
            all_qualified_keywords_for_run = self.db_manager.get_keywords_for_run(opportunity_id)
            qualified_keywords_list = [
                kw["keyword"] 
                for kw in all_qualified_keywords_for_run 
                if kw.get("blog_qualification_status") == "qualified"
            ]

            ai_topic_clusters, clustering_cost = self.ai_clustering_service.generate_topic_clusters(
                qualified_keywords_list
            )
            total_api_cost += clustering_cost
            self.job_manager.update_job_status(
                self.job_manager.get_current_job_id(), # Get current job ID
                "running",
                progress=60,
                result={"step": "AI-Powered Topic Clustering Complete"},
            )

            # Store clusters in content_intelligence for easier access within blueprint factory
            content_intelligence["ai_topic_clusters"] = ai_topic_clusters

            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
                keyword, live_serp_data, content_intelligence
            )
            total_api_cost += outline_api_cost
            content_intelligence.update(ai_outline)

            if not content_intelligence.get("article_structure"):
                self.logger.critical(
                    f"AI outline generation failed to produce an 'article_structure' for keyword: {keyword}."
                )
                raise ValueError("AI outline generation failed.")

            # 6. Assemble and Save Blueprint & Re-Score
            analysis_data = {
                "serp_overview": live_serp_data,
                "competitor_analysis": competitor_analysis,
                "content_intelligence": content_intelligence,
                "recommended_strategy": recommended_strategy,
                "ai_topic_clusters": ai_topic_clusters, # Pass clusters to analysis data for blueprint
            }
```

**Sub-Task 3.7: Store AI-Generated Structure in Blueprint (`blueprint_factory.py`)**

**File to Modify:** `backend/core/blueprint_factory.py`

**Instructions:** Modify the `create_blueprint` method to extract and store the `ai_topic_clusters` from the `analysis_data`.

**Locate the `blueprint_data` dictionary assignment in `create_blueprint` and add `ai_topic_clusters`:**
```python
        blueprint_data = {
            "metadata": {
                "seed_topic": seed_topic,
                "blueprint_version": "6.0",
                "generated_at": datetime.now().isoformat(),
                "total_api_cost": round(total_api_cost, 4),
                "client_id": client_id,
            },
            "winning_keyword": winning_keyword_data,
            "serp_overview": analysis_data.get("serp_overview", {}),
            "content_intelligence": analysis_data.get("content_intelligence", {}),
            "competitor_analysis": competitor_analysis_data,
            "recommended_strategy": recommended_strategy,
            "final_qualification_assessment": recommended_strategy_data.get(
                "final_qualification_assessment", {}
            ),
            "analysis_notes": analysis_notes,
            "ai_topic_clusters": analysis_data.get("ai_topic_clusters", []), # NEW: Add ai_topic_clusters here
        }
```

**Sub-Task 3.8: Adapt Content Analyzer to Use Clusters (`ContentAnalyzer._build_outline_prompt`)**

**File to Modify:** `backend/pipeline/step_04_analysis/content_analyzer.py`

**Instructions:** Modify the `_build_outline_prompt` method to use `ai_topic_clusters` if available as the primary H2 structure.

**Locate the `_build_outline_prompt` method. Find the `prompt` string and specifically the `**Analysis Data:**` section.**

**Replace this existing prompt string block:**
```python
        prompt = f"""
        You are an expert SEO content strategist. Create a logical and comprehensive content outline for an article about "{keyword}". The output must be a structured list of sections, each with an H2 and a list of corresponding H3 subheadings.

        **Analysis Data:**
        - **Common Competitor Headings to Incorporate:** {", ".join(content_intelligence.get("common_headings_to_cover", []))}
        - **Unique Angles & Gaps to Address:** {", ".join(content_intelligence.get("unique_angles_to_include", []))}
        - **Key Entities to Mention:** {", ".join(content_intelligence.get("key_entities_from_competitors", []))}
        - **People Also Ask Questions to Answer:** {", ".join(serp_overview.get("paa_questions", []))}

        **Instructions:**
        1. Create a logical flow for the article.
        2. The first section must be titled 'Introduction'.
        3. The last section must be titled 'Conclusion'.
        4. If there are 'People Also Ask' questions, create a dedicated H2 section titled 'Frequently Asked Questions' and use the questions as H3s.
        5. Structure the entire output as a JSON object matching the requested schema.
        """
```
**With this improved prompt logic:**
```python
        # Check if AI-generated topic clusters are available in content_intelligence
        ai_clusters = content_intelligence.get("ai_topic_clusters", [])
        
        prompt_core_instruction = ""
        if ai_clusters:
            # If AI clusters exist, prioritize them to form the core structure
            cluster_structure_description = "\n".join([
                f" - {cluster['topic_name']}: Keywords: {', '.join(cluster['keywords'])}"
                for cluster in ai_clusters
            ])
            prompt_core_instruction = f"""
            **AI-Generated Core Topic Structure (CRITICAL: Use this as the foundation for your H2s):**
            {cluster_structure_description}

            **Instructions for Outline Creation:**
            1.  **Strictly use the `topic_name` from each AI-Generated Core Topic as your primary H2 headings.**
            2.  For each H2, derive relevant H3 subheadings, possibly from the `keywords` within that cluster and other analysis data provided below.
            3.  Ensure the article flows logically and covers the keywords within each H2's cluster.
            """
            
        else:
            # Fallback to previous logic if AI clusters are not available
            prompt_core_instruction = """
            **Instructions for Outline Creation:**
            1. Create a logical flow for the article, starting with an 'Introduction' and ending with a 'Conclusion'.
            """

        prompt = f"""
        You are an expert SEO content strategist. Create a logical and comprehensive content outline for an article about "{keyword}". The output must be a structured list of sections, each with an H2 and a list of corresponding H3 subheadings.

        **Analysis Data:**
        - **Common Competitor Headings to Incorporate:** {", ".join(content_intelligence.get("common_headings_to_cover", []))}
        - **Unique Angles & Gaps to Address:** {", ".join(content_intelligence.get("unique_angles_to_include", []))}
        - **Key Entities to Mention:** {", ".join(content_intelligence.get("key_entities_from_competitors", []))}
        - **People Also Ask Questions to Answer:** {", ".join(serp_overview.get("paa_questions", []))}

        {prompt_core_instruction}

        **General Outline Rules:**
        1. The first H2 heading in the output JSON array must be "Introduction".
        2. The last H2 heading in the output JSON array must be "Conclusion".
        3. If there are 'People Also Ask' questions, create a dedicated H2 section titled 'Frequently Asked Questions' (if not already present from clusters) and use the questions as H3s.
        4. Structure the entire output as a JSON object matching the requested schema.
        """
```

**Sub-Task 3.9: Adapt Prompt Assembler to Inform AI of Clusters (`PromptAssembler._build_prompt`)**

**File to Modify:** `backend/agents/prompt_assembler.py`

**Instructions:** Modify the `_build_prompt` method to inject the AI-generated topic clusters into the system prompt for content generation.

**Locate the `base_instructions` string construction, specifically where other dynamic instructions are added.**

**After the `for placeholder, value in replacements.items():` loop, add this block:**
```python
        # NEW: Incorporate AI-generated topic clusters into the base instructions
        ai_topic_clusters = blueprint.get("ai_topic_clusters", [])
        if ai_topic_clusters:
            base_instructions += "\n\n**AI-GENERATED TOPIC STRUCTURE (PRIORITY):**\n"
            base_instructions += "The following structure represents the core topics and keywords for this article. Ensure you build your sections around these:\n"
            for cluster in ai_topic_clusters:
                base_instructions += f"- **H2: {cluster['topic_name']}** (Keywords to cover in this section: {', '.join(cluster['keywords'])})\n"
            base_instructions += "Ensure these topics are covered comprehensively and use the listed keywords within their respective H2 sections.\n"
```

**Sub-Task 3.10: Add `ai_topic_clusters` Column to Database**

**File to Modify:** `backend/data_access/migrations/028_add_ai_topic_clusters.sql` (if it's the next unapplied migration, or create a new one)

**Instructions:** Add the `ai_topic_clusters` column to the `opportunities` table.

```sql
-- backend/data_access/migrations/028_add_ai_topic_clusters.sql (if using this as the next migration)

ALTER TABLE opportunities ADD COLUMN ai_topic_clusters TEXT;
ALTER TABLE opportunities ADD COLUMN is_question BOOLEAN DEFAULT FALSE; -- Add is_question here too as it's often a related change.
```

**Sub-Task 3.11: Update `DatabaseManager` to Handle New Column**

**File to Modify:** `backend/data_access/database_manager.py`

**Instructions:** Update the `add_opportunities` method to save the `ai_topic_clusters` data.

**Locate the `cursor.execute` statement for inserting new opportunities (the `INSERT INTO opportunities (...) VALUES (...)` block) within `DatabaseManager.add_opportunities`.**

**Inside that SQL string, find the part where columns are listed and add `ai_topic_clusters`:**
```sql
                            "competitor_social_media_tags_json, competitor_page_timing_json, "
                            "social_media_posts_status, search_volume, keyword_difficulty, ai_topic_clusters, is_question" # NEW: Add ai_topic_clusters and is_question
                            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" # Update number of placeholders
```
**Then, in the corresponding tuple of values right after that SQL string, find the end of the list and add `json.dumps(full_data_copy.get("ai_topic_clusters"))` and `opp.get("is_question")`:**
```python
                            competitor_page_timing_json_val,
                            opp.get("social_media_posts_status", "draft"),
                            keyword_info.get("search_volume"),
                            keyword_properties.get("keyword_difficulty"),
                            json.dumps(full_data_copy.get("ai_topic_clusters", [])), # NEW: Add this line for the new column
                            opp.get("is_question", False), # NEW: Add is_question
                        ),
                    )
```

**Sub-Task 3.12: Create UI Component for Clustered Keywords (`ClusteredKeywords.jsx`)**

**Action:** Create a new file `my-content-app/src/pages/opportunity-detail-page/components/ClusteredKeywords.jsx`.

**Instructions:** Add the following complete code to the new file.

```javascript
import React from 'react';
import { Card, Typography, List, Tag } from 'antd';
import { FolderOpenOutlined } from '@ant-design/icons';
import NoData from './NoData';

const { Title, Text } = Typography;

const ClusteredKeywords = ({ clusters }) => {
  if (!clusters || clusters.length === 0) {
    return (
      <Card title="AI-Generated Topic Clusters" style={{ marginTop: 24 }}>
        <NoData description="No topic clusters were generated for this opportunity." />
      </Card>
    );
  }

  return (
    <Card title="AI-Generated Topic Clusters" style={{ marginTop: 24 }}>
      <Text type="secondary" style={{ marginBottom: 16, display: 'block' }}>
        The AI has grouped relevant keywords into these core topics, suggesting a structure for a single, comprehensive article.
      </Text>
      <List
        dataSource={clusters}
        renderItem={(cluster) => (
          <List.Item>
            <List.Item.Meta
              avatar={<FolderOpenOutlined style={{ fontSize: '24px', color: '#1890ff' }} />}
              title={<Title level={5} style={{ margin: 0 }}>{cluster.topic_name}</Title>}
              description={
                <div>
                  {cluster.keywords.map((keyword) => (
                    <Tag key={keyword} style={{ margin: '2px' }}>{keyword}</Tag>
                  ))}
                </div>
              }
            />
          </List.Item>
        )}
      />
    </Card>
  );
};

export default ClusteredKeywords;
```

**Sub-Task 3.13: Integrate `ClusteredKeywords` Component (`opportunity-detail-page/index.jsx`)**

**File to Modify:** `my-content-app/src/pages/opportunity-detail-page/index.jsx`

**Instructions:** Add the import for the new component and render it in the "Content Blueprint" tab.

**At the top of the file, add this import:**
```javascript
import ClusteredKeywords from './components/ClusteredKeywords';
```

**Inside the `OpportunityDetailPageV2` component, within the "Content Blueprint" `TabPane`, add the new component:**
```javascript
        <TabPane tab="Content Blueprint" key="3">
          <ClusteredKeywords clusters={blueprint?.ai_topic_clusters} /> {/* NEW: Add this line */}
          <ContentBlueprint
            blueprint={blueprint}
            overrides={blueprintOverrides}
            setOverrides={setBlueprintOverrides}
          />
        </TabPane>
```

---

### **Task 4: Enhance Scoring with Dynamic SERP Metrics**

**High-Level Goal:** Make the initial scoring more accurate by incorporating SERP freshness and volatility.

| # | Sub-Task | Category | Description |
| :-- | :--- | :--- | :--- |
| 4.1 | **Create SERP Freshness Scoring Component** | Backend Logic | Defines the `calculate_serp_freshness_score` function, which evaluates SERP age. |
| 4.2 | **Create SERP Volatility Scoring Component** | Backend Logic | Defines the `calculate_serp_volatility_score` function, which evaluates SERP update frequency. |
| 4.3 | **Integrate into `ScoringEngine`** | Backend Logic | Adds the new scoring components to the `ScoringEngine`'s calculation, including their weights. |
| 4.4 | **Add Configurable Weights to `settings.ini`** | Config | Introduces new configuration entries for controlling the influence of freshness and volatility on the overall score. |
| 4.5 | **Update `ConfigManager` to Load New Settings** | Backend Config | Modifies `app_config/manager.py` to correctly parse `serp_freshness_weight`, `serp_volatility_weight`, `serp_freshness_old_threshold_days`, `serp_volatility_stable_threshold_days`. |
| 4.6 | **Update `client_settings` DB Table** | Database | Adds new columns to `client_settings` to persist the configurable thresholds for freshness and volatility. |
| 4.7 | **Update `DatabaseManager` for New Settings** | Backend DB | Ensures `DatabaseManager.get_client_settings` and `update_client_settings` correctly read from and write to the new `client_settings` columns. |
| 4.8 | **Update Frontend Settings UI** | Frontend | Adds UI controls for the new SERP Freshness and Volatility weights in the `ScoringWeightsTab.jsx`. |
| 4.9 | **Update Frontend Score Breakdown UI** | Frontend | Modifies `ScoreBreakdownModal.jsx` to display the scores and explanations for SERP Freshness and Volatility. |

#### **Granular Code Implementation for Task 4**

**Sub-Task 4.1: Create `serp_freshness.py`**

**Action:** Create the file `backend/pipeline/step_03_prioritization/scoring_components/serp_freshness.py`.

**Instructions:** Add the following complete code to the new file.

```python
# backend/pipeline/step_03_prioritization/scoring_components/serp_freshness.py
from typing import Dict, Any, Tuple
from datetime import datetime, timezone

def calculate_serp_freshness_score(data: Dict[str, Any], config: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on SERP freshness. An older SERP is generally a better opportunity.
    Score increases as the SERP gets older.
    """
    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}
    last_update_str = serp_info.get("last_updated_time")

    if not last_update_str:
        return 50.0, {"Freshness": {"value": "N/A", "score": 50, "explanation": "No freshness data available to calculate SERP freshness score."}}

    try:
        last_update = datetime.fromisoformat(last_update_str.replace(" +00:00", "")).replace(tzinfo=timezone.utc)
        current_time_utc = datetime.now(timezone.utc)
        days_since_update = (current_time_utc - last_update).days
        
        old_threshold = config.get("serp_freshness_old_threshold_days", 180) # Default: 6 months
        
        # Linear scaling: 0 days = 0 score, old_threshold days = 100 score
        score = min(100, max(0, (days_since_update / old_threshold) * 100))

        explanation = f"SERP last updated {days_since_update} days ago. Older SERPs (threshold > {old_threshold} days) represent a better opportunity for new content."
        breakdown = {"Freshness": {"value": f"{days_since_update} days", "score": round(score), "explanation": explanation}}
        return round(score), breakdown
    except (ValueError, TypeError):
        return 50.0, {"Freshness": {"value": "Error", "score": 50, "explanation": "Could not parse update timestamp for SERP freshness."}}

```

**Sub-Task 4.2: Create `serp_volatility.py`**

**Action:** Create the file `backend/pipeline/step_03_prioritization/scoring_components/serp_volatility.py`.

**Instructions:** Add the following complete code to the new file.

```python
# backend/pipeline/step_03_prioritization/scoring_components/serp_volatility.py
from typing import Dict, Any, Tuple
from datetime import datetime, timezone

def calculate_serp_volatility_score(data: Dict[str, Any], config: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on SERP stability. A more volatile (frequently changing) SERP
    can be an opportunity as it suggests Google is actively looking for better results.
    Score increases with higher volatility (shorter interval between updates).
    """
    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}
    last_update_str = serp_info.get("last_updated_time")
    prev_update_str = serp_info.get("previous_updated_time")

    if not last_update_str or not prev_update_str:
        return 50.0, {"SERP Stability": {"value": "N/A", "score": 50, "explanation": "Insufficient data for SERP volatility calculation."}}

    try:
        last_update = datetime.fromisoformat(last_update_str.replace(" +00:00", "")).replace(tzinfo=timezone.utc)
        prev_update = datetime.fromisoformat(prev_update_str.replace(" +00:00", "")).replace(tzinfo=timezone.utc)
        
        days_between_updates = abs((last_update - prev_update).days)

        stable_threshold = config.get("serp_volatility_stable_threshold_days", 90) # Default: 3 months
        
        # Score is inverted: shorter interval (more volatile) = higher score
        # Example: 0 days = 100 score, stable_threshold days = 0 score
        score = min(100, max(0, 100 - ((days_between_updates / stable_threshold) * 100)))

        explanation = f"SERP typically updates every {days_between_updates} days. More frequent updates (shorter intervals) indicate higher volatility, suggesting an opportunity."
        breakdown = {"SERP Stability": {"value": f"{days_between_updates} days", "score": round(score), "explanation": explanation}}
        return round(score), breakdown
    except (ValueError, TypeError):
        return 50.0, {"SERP Stability": {"value": "Error", "score": 50, "explanation": "Could not parse SERP update timestamps for volatility."}}

```

**Sub-Task 4.3: Integrate into `ScoringEngine`**

**File to Modify:** `backend/pipeline/step_03_prioritization/scoring_components/__init__.py`

**Instructions:** Add the following lines to the `__all__` list.

```python
# backend/pipeline/step_03_prioritization/scoring_components/__init__.py
from .ease_of_ranking import calculate_ease_of_ranking_score
from .traffic_potential import calculate_traffic_potential_score
from .commercial_intent import calculate_commercial_intent_score
from .growth_trend import calculate_growth_trend_score
from .serp_features import calculate_serp_features_score
from .serp_volatility import calculate_serp_volatility_score # Import this
from .competitor_weakness import calculate_competitor_weakness_score
from .serp_crowding import calculate_serp_crowding_score
from .keyword_structure import calculate_keyword_structure_score
from .serp_threat import calculate_serp_threat_score
from .volume_volatility import calculate_volume_volatility_score
from .serp_freshness import calculate_serp_freshness_score # Import this
from .competitor_performance import calculate_competitor_performance_score

__all__ = [
    "calculate_ease_of_ranking_score",
    "calculate_traffic_potential_score",
    "calculate_commercial_intent_score",
    "calculate_growth_trend_score",
    "calculate_serp_features_score",
    "calculate_serp_volatility_score",
    "calculate_competitor_weakness_score",
    "calculate_serp_crowding_score",
    "calculate_keyword_structure_score",
    "calculate_serp_threat_score",
    "calculate_volume_volatility_score",
    "calculate_serp_freshness_score",
    "calculate_competitor_performance_score",
]
```

**File to Modify:** `backend/pipeline/step_03_prioritization/scoring_engine.py`

**Instructions:** Add the imports and the new scoring calculations in `calculate_score`.

**Add these imports at the top of the file:**
```python
from .scoring_components import (
    calculate_ease_of_ranking_score,
    calculate_traffic_potential_score,
    calculate_commercial_intent_score,
    calculate_growth_trend_score,
    calculate_serp_features_score,
    calculate_serp_volatility_score,
    calculate_competitor_weakness_score,
    calculate_serp_crowding_score,
    calculate_keyword_structure_score,
    calculate_serp_threat_score,
    calculate_volume_volatility_score,
    calculate_serp_freshness_score,
    calculate_competitor_performance_score,
)
```

**Within `ScoringEngine.calculate_score`, after the existing calls to `calculate_serp_threat_score` (or similar), add:**
```python
        volume_volatility_score, volume_volatility_breakdown = (
            calculate_volume_volatility_score(data_source, self.config)
        )
        breakdown["volume_volatility"] = {
            "name": "Volume Volatility",
            "score": volume_volatility_score,
            "breakdown": volume_volatility_breakdown,
        }

        freshness_score, freshness_breakdown = calculate_serp_freshness_score(
            data_source, self.config
        )
        breakdown["serp_freshness"] = {
            "name": "SERP Freshness",
            "score": freshness_score,
            "breakdown": freshness_breakdown,
        }

        serp_volatility_score, serp_volatility_breakdown = calculate_serp_volatility_score(
            data_source, self.config
        )
        breakdown["serp_volatility"] = {
            "name": "SERP Volatility",
            "score": serp_volatility_score,
            "breakdown": serp_volatility_breakdown,
        }```

**Next, locate the `weights` dictionary and add the new weights. Ensure `total_weight` correctly sums these.**

**Replace this existing `weights` dictionary:**
```python
        weights = {
            "ease": self.config.get("ease_of_ranking_weight", 25),
            "traffic": self.config.get("traffic_potential_weight", 20),
            "intent": self.config.get("commercial_intent_weight", 15),
            "weakness": self.config.get("competitor_weakness_weight", 10),
            "structure": self.config.get("keyword_structure_weight", 5),
            "trend": self.config.get("growth_trend_weight", 5),
            "features": self.config.get("serp_features_weight", 5),
            "crowding": self.config.get("serp_crowding_weight", 5),
            "volatility": self.config.get("serp_volatility_weight", 5),
            "threat": self.config.get("serp_threat_weight", 5),
            "freshness": self.config.get("serp_freshness_weight", 0),
            "competitor_performance": self.config.get(
                "competitor_performance_weight", 5
            ),
            "volume_volatility": self.config.get("volume_volatility_weight", 0),
        }
```
**With this (ensure all weights from the `weights` dict are used, this is a general correction):**
```python
        weights = {
            "ease": self.config.get("ease_of_ranking_weight", 25),
            "traffic": self.config.get("traffic_potential_weight", 20),
            "intent": self.config.get("commercial_intent_weight", 15),
            "weakness": self.config.get("competitor_weakness_weight", 10),
            "structure": self.config.get("keyword_structure_weight", 5),
            "trend": self.config.get("growth_trend_weight", 5),
            "features": self.config.get("serp_features_weight", 5),
            "crowding": self.config.get("serp_crowding_weight", 5),
            "serp_volatility": self.config.get("serp_volatility_weight", 5), # Updated key
            "threat": self.config.get("serp_threat_weight", 5),
            "serp_freshness": self.config.get("serp_freshness_weight", 5), # Updated key
            "competitor_performance": self.config.get("competitor_performance_weight", 5),
            "volume_volatility": self.config.get("volume_volatility_weight", 0),
        }
```

**Finally, update the `final_score` calculation to include the new components. Make sure to update the `total_weight` sum calculation as well.**

**Replace this `final_score` calculation:**
```python
        final_score = (
            (ease_score * weights["ease"])
            + (traffic_score * weights["traffic"])
            + (intent_score * weights["intent"])
            + (weakness_score * weights["weakness"])
            + (structure_score * weights["structure"])
            + (trend_score * weights["trend"])
            + (features_score * weights["features"])
            + (crowding_score * weights["crowding"])
            + (volatility_score * weights["volatility"]) # Old volatility_score
            + (threat_score * weights["threat"])
            + (freshness_score * weights["freshness"]) # Old freshness_score
            + (volume_volatility_score * weights["volume_volatility"])
            + (performance_score * weights["competitor_performance"])
        ) / total_weight
```
**With this (ensure all new score variables are used with their corresponding weights):**
```python
        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0.0, breakdown  # Avoid division by zero

        final_score = (
            (ease_score * weights.get("ease", 0))
            + (traffic_score * weights.get("traffic", 0))
            + (intent_score * weights.get("intent", 0))
            + (weakness_score * weights.get("weakness", 0))
            + (structure_score * weights.get("structure", 0))
            + (trend_score * weights.get("trend", 0))
            + (features_score * weights.get("features", 0))
            + (crowding_score * weights.get("crowding", 0))
            + (serp_volatility_score * weights.get("serp_volatility", 0)) # Use new serp_volatility_score
            + (threat_score * weights.get("threat", 0))
            + (freshness_score * weights.get("serp_freshness", 0)) # Use new serp_freshness_score
            + (volume_volatility_score * weights.get("volume_volatility", 0))
            + (performance_score * weights.get("competitor_performance", 0))
        ) / total_weight
```

**Sub-Task 4.4: Add Configurable Weights to `settings.ini`**

**File to Modify:** `backend/app_config/settings.ini`

**Instructions:** Add these lines to the `[SCORING_WEIGHTS]` section.

```ini
[SCORING_WEIGHTS]
ease_of_ranking_weight = 40
traffic_potential_weight = 15
commercial_intent_weight = 5
serp_features_weight = 5
growth_trend_weight = 5
serp_freshness_weight = 5 ; NEW
serp_volatility_weight = 5 ; NEW
competitor_weakness_weight = 20
competitor_performance_weight = 5

; NEW: Thresholds for Freshness and Volatility Scoring Components
serp_freshness_old_threshold_days = 180
serp_volatility_stable_threshold_days = 90
```

**Sub-Task 4.5: Update `ConfigManager` to Load New Settings**

**File to Modify:** `backend/app_config/manager.py`

**Instructions:** Update the `_setting_types` dictionary with the new float and integer settings.

**Inside the `_setting_types` dictionary, add the following lines:**
```python
    _setting_types = {
        # ... existing float types ...
        "serp_freshness_weight": float, # NEW
        "serp_volatility_weight": float, # NEW
        # ... existing integer types ...
        "serp_freshness_old_threshold_days": int, # NEW
        "serp_volatility_stable_threshold_days": int, # NEW
        # ... rest of _setting_types ...
    }
```

**Sub-Task 4.6: Update `client_settings` DB Table**

**File to Modify:** `backend/data_access/migrations/028_add_ai_topic_clusters.sql` (or `029_add_serp_scoring_settings.sql` if 028 is applied)

**Instructions:** Add the new columns to the `client_settings` table.

```sql
-- backend/data_access/migrations/028_add_ai_topic_clusters.sql (if using this as the next migration)

ALTER TABLE opportunities ADD COLUMN ai_topic_clusters TEXT;
ALTER TABLE opportunities ADD COLUMN is_question BOOLEAN DEFAULT FALSE;

-- NEW COLUMNS FOR CLIENT_SETTINGS
ALTER TABLE client_settings ADD COLUMN discovery_max_pages INTEGER DEFAULT 100;
ALTER TABLE client_settings ADD COLUMN discovery_related_depth INTEGER DEFAULT 1;
ALTER TABLE client_settings ADD COLUMN discovery_exact_match BOOLEAN DEFAULT FALSE;
ALTER TABLE client_settings ADD COLUMN serp_freshness_weight REAL DEFAULT 5.0; -- NEW
ALTER TABLE client_settings ADD COLUMN serp_volatility_weight REAL DEFAULT 5.0; -- NEW
ALTER TABLE client_settings ADD COLUMN serp_freshness_old_threshold_days INTEGER DEFAULT 180; -- NEW
ALTER TABLE client_settings ADD COLUMN serp_volatility_stable_threshold_days INTEGER DEFAULT 90; -- NEW
```

**Sub-Task 4.7: Update `DatabaseManager` for New Settings**

**File to Modify:** `backend/data_access/database_manager.py`

**Instructions:** Modify the `get_client_settings` method to correctly retrieve and convert the new float and integer types.

**In `DatabaseManager.get_client_settings`, within the `if row:` block, add the new keys to `float_keys` and `int_keys` lists.**

**Locate the `float_keys` list definition:**
```python
                float_keys = [
                    # ... existing float keys ...
                ]
```
**And replace it with this:**
```python
                float_keys = [
                    "informational_score",
                    "commercial_score",
                    "transactional_score",
                    "navigational_score",
                    "question_keyword_bonus",
                    "max_cpc_for_scoring",
                    "min_monthly_trend_percentage",
                    "featured_snippet_bonus",
                    "ai_overview_bonus",
                    "serp_freshness_bonus_max",
                    "min_cpc_filter_api",
                    "category_intent_bonus",
                    "search_volume_volatility_threshold",
                    "max_paid_competition_score",
                    "max_high_top_of_page_bid",
                    "max_pages_to_domain_ratio",
                    "ai_generation_temperature",
                    "recommended_word_count_multiplier",
                    "serp_freshness_weight", # NEW
                    "serp_volatility_weight", # NEW
                ]
```

**Locate the `int_keys` list definition:**
```python
                int_keys = [
                    # ... existing integer keys ...
                ]
```
**And replace it with this:**
```python
                int_keys = [
                    "num_in_article_images",
                    "location_code",
                    "serp_freshness_old_threshold_days",
                    "min_competitor_word_count",
                    "max_competitor_technical_warnings",
                    "num_competitors_to_analyze",
                    "num_common_headings",
                    "num_unique_angles",
                    "max_initial_serp_urls_to_analyze",
                    "min_search_volume",
                    "max_keyword_difficulty",
                    "people_also_ask_click_depth",
                    "onpage_max_domains_per_request",
                    "onpage_max_tasks_per_request",
                    "ease_of_ranking_weight",
                    "traffic_potential_weight",
                    "commercial_intent_weight",
                    "growth_trend_weight",
                    "serp_features_weight",
                    "serp_volatility_weight",
                    "competitor_weakness_weight",
                    "max_sv_for_scoring",
                    "max_domain_rank_for_scoring",
                    "max_referring_domains_for_scoring",
                    "serp_volatility_stable_threshold_days",
                    "discovery_related_depth",
                    "max_avg_referring_domains_filter",
                    "yearly_trend_decline_threshold",
                    "quarterly_trend_decline_threshold",
                    "max_kd_hard_limit",
                    "max_referring_main_domains_limit",
                    "max_avg_domain_rank_threshold",
                    "min_keyword_word_count",
                    "max_keyword_word_count",
                    "crowded_serp_features_threshold",
                    "min_serp_stability_days",
                    "max_non_blog_results",
                    "max_ai_overview_words",
                    "max_first_organic_y_pixel",
                    "max_words_for_ai_analysis",
                    "max_avg_lcp_time",
                    "discovery_max_pages",
                    "discovery_related_depth",
                    "serp_freshness_old_threshold_days", # NEW
                    "serp_volatility_stable_threshold_days", # NEW
                ]
```

**Sub-Task 4.8: Update Frontend Settings UI (`ScoringWeightsTab.jsx`)**

**File to Modify:** `my-content-app/src/pages/Settings/tabs/ScoringWeightsTab.jsx`

**Instructions:** Add new `Slider` components for "SERP Freshness Weight" and "SERP Volatility Weight" and new inputs for their thresholds.

**Locate the `renderWeightInput` function call list:**
```javascript
      <Row gutter={16}>
        {renderWeightInput('ease_of_ranking_weight', 'Ease of Ranking', 'How easy it is to rank (based on KD, backlinks).')}
        {renderWeightInput('traffic_potential_weight', 'Traffic Potential', 'How much traffic the keyword can bring (based on Search Volume).')}
        {renderWeightInput('commercial_intent_weight', 'Commercial Intent', 'How likely the keyword is to lead to a conversion (based on CPC, intent type).')}
        {renderWeightInput('serp_features_weight', 'SERP Features', 'Impact of rich SERP features (Featured Snippets, AI Overviews).')}
        {renderWeightInput('growth_trend_weight', 'Growth Trend', 'How quickly the search volume is growing or declining.')}
        {renderWeightInput('serp_freshness_weight', 'SERP Freshness', 'How recently the SERP was updated (opportunity if stale).')}
        {renderWeightInput('serp_volatility_weight', 'SERP Volatility', 'How often the SERP changes (opportunity if stable).')}
        {renderWeightInput('competitor_weakness_weight', 'Competitor Weakness', 'Exploitable technical or content flaws of top competitors.')}
      </Row>
```
**With this (ensure new `renderWeightInput` calls are present):**
```javascript
      <Row gutter={16}>
        {renderWeightInput('ease_of_ranking_weight', 'Ease of Ranking', 'How easy it is to rank (based on KD, backlinks).')}
        {renderWeightInput('traffic_potential_weight', 'Traffic Potential', 'How much traffic the keyword can bring (based on Search Volume).')}
        {renderWeightInput('commercial_intent_weight', 'Commercial Intent', 'How likely the keyword is to lead to a conversion (based on CPC, intent type).')}
        {renderWeightInput('serp_features_weight', 'SERP Features', 'Impact of rich SERP features (Featured Snippets, AI Overviews).')}
        {renderWeightInput('growth_trend_weight', 'Growth Trend', 'How quickly the search volume is growing or declining.')}
        {renderWeightInput('serp_freshness_weight', 'SERP Freshness', 'How recently the SERP was updated (opportunity if stale).')}
        {renderWeightInput('serp_volatility_weight', 'SERP Volatility', 'How often the SERP changes (opportunity if stable).')}
        {renderWeightInput('competitor_weakness_weight', 'Competitor Weakness', 'Exploitable technical or content flaws of top competitors.')}
      </Row>

      <Divider />

      <Title level={5}>SERP Dynamics Thresholds</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="serp_freshness_old_threshold_days" label="Freshness Threshold (days)">
            <InputNumber min={0} step={10} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="serp_volatility_stable_threshold_days" label="Volatility Stable Threshold (days)">
            <InputNumber min={0} step={10} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
      </Row>
```

**Sub-Task 4.9: Update Frontend Score Breakdown UI (`ScoreBreakdownModal.jsx`)**

**File to Modify:** `my-content-app/src/pages/opportunity-detail-page/components/ScoreBreakdownModal.jsx`

**Instructions:** Add the new components to the render logic in the modal.

**Locate the `renderFactor` function call list:**
```javascript
      <Row gutter={[16, 16]}>
        {renderFactor('ease_of_ranking', <BarChartOutlined />)}
        {renderFactor('traffic_potential', <FireOutlined />)}
        {renderFactor('commercial_intent', <ThunderboltOutlined />)}
        {renderFactor('growth_trend', <RiseOutlined />)}
        {renderFactor('serp_features', <StarOutlined />)}
        {renderFactor('competitor_weakness', <BuildOutlined />)}
        {renderFactor('serp_volatility', <SmileOutlined />)}
        {renderFactor('serp_crowding', <UsergroupAddOutlined />)}
        {renderFactor('keyword_structure', <ApartmentOutlined />)}
        {renderFactor('serp_threat', <WarningOutlined />)}
        {renderFactor('volume_volatility', <CalendarOutlined />)}
        {renderFactor('serp_freshness', <GlobalOutlined />)}
        {renderFactor('competitor_performance', <DashboardOutlined />)}
      </Row>
```
**With this (ensure new `renderFactor` calls are present):**
```javascript
      <Row gutter={[16, 16]}>
        {renderFactor('ease_of_ranking', <BarChartOutlined />)}
        {renderFactor('traffic_potential', <FireOutlined />)}
        {renderFactor('commercial_intent', <ThunderboltOutlined />)}
        {renderFactor('growth_trend', <RiseOutlined />)}
        {renderFactor('serp_features', <StarOutlined />)}
        {renderFactor('serp_freshness', <GlobalOutlined />)} {/* NEW */}
        {renderFactor('serp_volatility', <SmileOutlined />)} {/* NEW */}
        {renderFactor('competitor_weakness', <BuildOutlined />)}
        {renderFactor('serp_crowding', <UsergroupAddOutlined />)}
        {renderFactor('keyword_structure', <ApartmentOutlined />)}
        {renderFactor('serp_threat', <WarningOutlined />)}
        {renderFactor('volume_volatility', <CalendarOutlined />)}
        {renderFactor('competitor_performance', <DashboardOutlined />)}
      </Row>
```

---

### **Task 5: Implement "Question Keyword" Identification and Prioritization**

**High-Level Goal:** Systematically identify and prioritize high-value question-based keywords.

| # | Sub-Task | Category | Description |
| :-- | :--- | :--- | :--- |
| 5.1 | **Create `is_question_keyword` Utility Function** | Backend Logic | Defines a robust utility to detect if a given keyword is a question. |
| 5.2 | **Add `question_keyword_bonus` to `settings.ini`** | Config | Makes the question keyword bonus configurable. |
| 5.3 | **Apply Scoring Bonus for Question Keywords** | Backend Logic | Modifies the `commercial_intent.py` scoring component to award a bonus for question keywords. |
| 5.4 | **Add `is_question` Flag During Discovery** | Backend Logic | Integrates the question detection into the discovery pipeline (`run_discovery.py`) to add a flag to each opportunity. |
| 5.5 | **Persist `is_question` Flag to Database** | Database | Extends the `opportunities` table schema and `DatabaseManager` to store the new flag. |
| 5.6 | **Update Frontend UI to Display Question Indicator** | Frontend | Modifies `OpportunitiesPage.jsx` and `RunDetailsPage.jsx` to visually indicate question keywords. |

#### **Granular Code Implementation for Task 5**

**Sub-Task 5.1: Create `is_question_keyword` Utility Function**

**File to Modify:** `backend/core/utils.py`

**Instructions:** Add the `is_question_keyword` function to `utils.py`.

```python
# backend/core/utils.py

import logging
import re
from typing import Optional, Union, Dict
from datetime import datetime, timezone # Added timezone for robustness

# ... (rest of imports) ...

def slugify(text: str) -> str:
    """
    Convert a string to a URL-friendly slug.
    """
    if not text:
        return ""
    text = text.lower()
    # Remove special characters
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace spaces with hyphens
    text = re.sub(r"\s+", "-", text)
    return text


def is_question_keyword(keyword: str) -> bool:
    """
    Checks if a keyword is likely a question.
    Covers common question formats and leading words.
    """
    if not keyword:
        return False

    keyword_lower = keyword.lower().strip()

    # Common question prefixes
    question_starters = [
        "what", "when", "where", "who", "why", "how", "which", "whose",
        "is", "are", "am", "was", "were", "do", "does", "did",
        "can", "could", "will", "would", "should", "may", "might",
        "have", "has", "had", "are there", "is there", "why do", "how to"
    ]

    # Check if the keyword starts with a question word or ends with a question mark
    if keyword_lower.endswith("?"):
        return True

    for starter in question_starters:
        if keyword_lower.startswith(starter + " "):
            return True

    # Heuristic: Check for common question phrases within the keyword
    if " how " in keyword_lower or " what " in keyword_lower or " why " in keyword_lower:
        return True

    return False


def safe_compare(
    value: Optional[Union[int, float]],
    threshold: Optional[Union[int, float]],
    operation: str,
) -> bool:
    """
    Safely compares a potentially None value against a potentially None threshold.
    Returns False if either value is None to prevent TypeErrors.

    :param value: The value to check (e.g., from API data).
    :param threshold: The threshold to compare against (e.g., from config).
    :param operation: The comparison to perform ('gt' for >, 'lt' for <).
    :return: Boolean result of the comparison, or False if unsafe.
    """
    if value is None or threshold is None:
        return False

    if operation == "gt":
        return value > threshold
    elif operation == "lt":
        return value < threshold
    elif operation == "ge": # Added for >=
        return value >= threshold
    elif operation == "le": # Added for <=
        return value <= threshold

    return False


def parse_datetime_string(dt_str: Optional[str]) -> Optional[str]:
    """
    Parses a DataForSEO datetime string (e.g., "yyyy-mm-dd hh-mm-ss +00:00")
    into a consistent ISO format string or returns None.
    """
    if not dt_str:
        return None

    # Remove timezone offset for consistent parsing if it's always +00:00
    cleaned_dt_str = dt_str.replace(" +00:00", "").strip()

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",  # Added ISO 8601 format
        "%Y-%m-%d %H:%M:%S.%f",  # With microseconds
        "%Y-%m-%d",  # Date only
    ]

    for fmt in formats:
        try:
            return datetime.strptime(cleaned_dt_str, fmt).isoformat()
        except ValueError:
            pass

    logging.getLogger(__name__).warning(
        f"Could not parse datetime string: {dt_str}. Returning None."
    )
    return None


def calculate_serp_times(
    datetime_str: Optional[str], previous_datetime_str: Optional[str]
) -> Dict[str, Optional[int]]:
    """
    Calculates the age of the SERP and the interval between the last two updates.
    """
    days_ago = None
    update_interval_days = None

    if datetime_str:
        parsed_date_iso = parse_datetime_string(datetime_str)
        if parsed_date_iso:
            serp_date = datetime.fromisoformat(parsed_date_iso).replace(tzinfo=timezone.utc) # Ensure UTC
            days_ago = (datetime.now(timezone.utc) - serp_date).days
        else:
            logging.getLogger(__name__).warning(
                f"Could not parse SERP datetime for days_ago: {datetime_str}"
            )

    if datetime_str and previous_datetime_str:
        parsed_last_update_iso = parse_datetime_string(datetime_str)
        parsed_prev_update_iso = parse_datetime_string(previous_datetime_str)

        if parsed_last_update_iso and parsed_prev_update_iso:
            last_update_dt = datetime.fromisoformat(parsed_last_update_iso).replace(tzinfo=timezone.utc) # Ensure UTC
            prev_update_dt = datetime.fromisoformat(parsed_prev_update_iso).replace(tzinfo=timezone.utc) # Ensure UTC
            update_interval_days = abs((last_update_dt - prev_update_dt).days)
        else:
            logging.getLogger(__name__).warning(
                f"Could not parse SERP previous update times for interval: {datetime_str}, {previous_datetime_str}"
            )

    return {"days_ago": days_ago, "update_interval_days": update_interval_days}

```

**Sub-Task 5.2: Add `question_keyword_bonus` to `settings.ini`**

**File to Modify:** `backend/app_config/settings.ini`

**Instructions:** Add this line to the `[INTENT_SCORING]` section.

```ini
[INTENT_SCORING]
informational_score = 100
commercial_score = 70
transactional_score = 50
navigational_score = 10
question_keyword_bonus = 15 ; NEW: Bonus for question keywords
```

**Sub-Task 5.3: Apply Scoring Bonus for Question Keywords**

**File to Modify:** `backend/pipeline/step_03_prioritization/scoring_components/commercial_intent.py`

**Instructions:** Modify the `calculate_commercial_intent_score` function to use the new `is_question_keyword` utility and apply the bonus.

**Within `calculate_commercial_intent_score`, after the primary `intent_score` calculation and before the final `final_score` calculation, add this block:**
```python
    # NEW: Add bonus for question keywords
    if utils.is_question_keyword(keyword):
        bonus = config.get("question_keyword_bonus", 15)
        intent_score = min(100, intent_score + bonus)
        explanation += f" Bonus of +{bonus} for being a question keyword."
```

**Sub-Task 5.4: Add `is_question` Flag During Discovery (`run_discovery.py`)**

**File to Modify:** `backend/pipeline/step_01_discovery/run_discovery.py`

**Instructions:** Modify the main `run_discovery_phase` function to call the `is_question_keyword` utility and add the flag to the `opp` dictionary.

**Locate the loop `for opp in all_expanded_keywords:` within `run_discovery_phase`.**

**Inside the loop, after the `keyword = opp.get("keyword")` line, add:**
```python
        # NEW: Add is_question flag
        opp["is_question"] = utils.is_question_keyword(opp.get("keyword", ""))
```

**Sub-Task 5.5: Persist `is_question` Flag to Database**

**File to Modify:** `backend/data_access/migrations/028_add_ai_topic_clusters.sql` (or create a new migration, e.g., `029_add_is_question_column.sql`)

**Instructions:** Add the `is_question` column to the `opportunities` table.

```sql
-- backend/data_access/migrations/028_add_ai_topic_clusters.sql (if using this as the next migration)

ALTER TABLE opportunities ADD COLUMN ai_topic_clusters TEXT;
ALTER TABLE opportunities ADD COLUMN is_question BOOLEAN DEFAULT FALSE; -- NEW: Add is_question column
```

**File to Modify:** `backend/data_access/database_manager.py`

**Instructions:** Update the `add_opportunities` method to save the `is_question` flag.

**Locate the `cursor.execute` statement for inserting new opportunities (the `INSERT INTO opportunities (...) VALUES (...)` block) within `DatabaseManager.add_opportunities`.**

**Inside that SQL string, find the part where columns are listed and add `is_question`:**
```sql
                            "competitor_social_media_tags_json, competitor_page_timing_json, "
                            "social_media_posts_status, search_volume, keyword_difficulty, ai_topic_clusters, is_question" # NEW: Add ai_topic_clusters and is_question
                            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" # Update number of placeholders
```
**Then, in the corresponding tuple of values right after that SQL string, find the end of the list and add `json.dumps(full_data_copy.get("ai_topic_clusters"))` and `opp.get("is_question")`:**
```python
                            competitor_page_timing_json_val,
                            opp.get("social_media_posts_status", "draft"),
                            keyword_info.get("search_volume"),
                            keyword_properties.get("keyword_difficulty"),
                            json.dumps(full_data_copy.get("ai_topic_clusters", [])),
                            opp.get("is_question", False), # NEW: Add is_question
                        ),
                    )```

**Sub-Task 5.6: Update Frontend UI to Display Question Indicator (`OpportunitiesPage.jsx` and `RunDetailsPage.jsx`)**

**File to Modify:** `my-content-app/src/pages/OpportunitiesPage/OpportunitiesPage.jsx`

**Instructions:** Modify the `columns` definition to conditionally display a `QuestionCircleOutlined` icon next to the keyword.

**Locate the `columns` array. Find the `keyword` column definition:**
```javascript
        { title: 'Keyword', dataIndex: 'keyword', key: 'keyword', sorter: true, render: (text, record) => <a onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}}>{text}</a> },
```
**With this:**
```javascript
        {
          title: 'Keyword',
          dataIndex: 'keyword',
          key: 'keyword',
          sorter: true,
          render: (text, record) => (
            <Space>
              <a onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}}>{text}</a>
              {record.is_question && <Tooltip title="Question Keyword"><QuestionCircleOutlined style={{ color: '#1890ff' }} /></Tooltip>}
            </Space>
          )
        },
```

**File to Modify:** `my-content-app/src/pages/DiscoveryPage/components/RunDetailsPage.jsx`

**Instructions:** Modify the `columns` definition to conditionally display a `QuestionCircleOutlined` icon next to the keyword.

**Locate the `columns` array. Find the `keyword` column definition:**
```javascript
    {
      title: 'Keyword',
      dataIndex: 'keyword',
      key: 'keyword',
      sorter: (a, b) => a.keyword.localeCompare(b.keyword),
    },
```
**With this:**
```javascript
    {
      title: 'Keyword',
      dataIndex: 'keyword',
      key: 'keyword',
      sorter: (a, b) => a.keyword.localeCompare(b.keyword),
      render: (text, record) => (
        <Space>
          <Text>{text}</Text>
          {record.is_question && <Tooltip title="Question Keyword"><QuestionCircleOutlined style={{ color: '#1890ff' }} /></Tooltip>}
        </Space>
      ),
    },
```

---

### **Task 6: Develop Context-Aware Disqualification Rules Based on Intent**

**High-Level Goal:** Make the qualification process more intelligent by applying different rules based on the keyword's primary search intent.

| # | Sub-Task | Category | Description |
| :-- | :--- | :--- | :--- |
| 6.1 | **Update `settings.ini` with Intent-Specific Rules** | Config | Adds new, intent-prefixed configuration variables for `max_high_top_of_page_bid` (CPC threshold). |
| 6.2 | **Refactor `ConfigManager` to Load Intent Rules** | Backend Config | Modifies the `ConfigManager` to correctly parse and store the new intent-specific rules. |
| 6.3 | **Update `qualification_settings` Database Table** | Database | Adds new columns to `qualification_settings` to store the intent-specific thresholds in the database. |
| 6.4 | **Update `DatabaseManager` for New Settings Structure** | Backend DB | Modifies `get_qualification_settings` to correctly read from and `update_qualification_settings` to write to the new intent-based rules. |
| 6.5 | **Refactor `disqualification_rules.py` for Intent-Awareness** | Backend Logic | Updates the `apply_disqualification_rules` function to dynamically select thresholds based on the keyword's detected `main_intent`. |
| 6.6 | **Redesign `DiscoverySettingsTab.jsx` for Intent Rules** | Frontend | Implements a UI using Ant Design `Tabs` to allow users to configure rules for each intent type. |

#### **Granular Code Implementation for Task 6**

**Sub-Task 6.1: Update `settings.ini` with Intent-Specific Rules**

**File to Modify:** `backend/app_config/settings.ini`

**Instructions:** Add these lines to the `[DISQUALIFICATION_RULES]` section.

```ini
[DISQUALIFICATION_RULES]
; Tier 1
allowed_intents = informational
negative_keywords = login, sign in, account, free, cheap, porn

; Tier 2
yearly_trend_decline_threshold = -25
quarterly_trend_decline_threshold = 0
search_volume_volatility_threshold = 1.5

; Tier 3
max_paid_competition_score = 0.8
max_high_top_of_page_bid = 15.00 ; General default
informational_max_high_top_of_page_bid = 5.0 ; Stricter for informational
commercial_max_high_top_of_page_bid = 20.0 ; Looser for commercial
transactional_max_high_top_of_page_bid = 30.0 ; Even looser for transactional
max_kd_hard_limit = 70
informational_max_kd_hard_limit = 60 ; Example intent-specific KD
commercial_max_kd_hard_limit = 80
transactional_max_kd_hard_limit = 90
max_referring_main_domains_limit = 100
max_avg_domain_rank_threshold = 500
max_pages_to_domain_ratio = 15

; Tier 4
non_evergreen_year_pattern = 20[12]\d ; e.g., 2010-2029
min_keyword_word_count = 2
max_keyword_word_count = 8
hostile_serp_features = shopping,local_pack,google_flights,google_hotels,popular_products,local_services
crowded_serp_features_threshold = 4
min_serp_stability_days = 14
max_y_pixel_threshold = 800
max_forum_results_in_top_10 = 3
max_ecommerce_results_in_top_10 = 2
disallowed_page_types_in_top_3 = E-commerce,Forum
```

**Sub-Task 6.2: Refactor `ConfigManager` to Load Intent Rules**

**File to Modify:** `backend/app_config/manager.py`

**Instructions:** Update the `_setting_types` dictionary with the new intent-specific settings.

**Inside `_setting_types`, add these lines:**
```python
    _setting_types = {
        # ... existing float types ...
        "informational_max_high_top_of_page_bid": float, # NEW
        "commercial_max_high_top_of_page_bid": float, # NEW
        "transactional_max_high_top_of_page_bid": float, # NEW
        "informational_max_kd_hard_limit": int, # NEW
        "commercial_max_kd_hard_limit": int, # NEW
        "transactional_max_kd_hard_limit": int, # NEW
        # ... rest of _setting_types ...
    }
```
**No direct code change is needed in `_load_and_validate_global` as the generic loop handles `float` and `int` types if defined in `settings.ini`.**

**Sub-Task 6.3: Update `qualification_settings` Database Table**

**File to Modify:** `backend/data_access/migrations/028_add_ai_topic_clusters.sql` (or `029_add_intent_specific_settings.sql` if 028 is applied)

**Instructions:** Add the new columns to the `qualification_settings` table.

```sql
-- backend/data_access/migrations/028_add_ai_topic_clusters.sql (if using this as the next migration)

ALTER TABLE opportunities ADD COLUMN ai_topic_clusters TEXT;
ALTER TABLE opportunities ADD COLUMN is_question BOOLEAN DEFAULT FALSE;

ALTER TABLE qualification_settings ADD COLUMN informational_max_high_top_of_page_bid REAL DEFAULT 5.0;
ALTER TABLE qualification_settings ADD COLUMN commercial_max_high_top_of_page_bid REAL DEFAULT 20.0;
ALTER TABLE qualification_settings ADD COLUMN transactional_max_high_top_of_page_bid REAL DEFAULT 30.0;
ALTER TABLE qualification_settings ADD COLUMN informational_max_kd_hard_limit INTEGER DEFAULT 60;
ALTER TABLE qualification_settings ADD COLUMN commercial_max_kd_hard_limit INTEGER DEFAULT 80;
ALTER TABLE qualification_settings ADD COLUMN transactional_max_kd_hard_limit INTEGER DEFAULT 90;
```

**Sub-Task 6.4: Update `DatabaseManager` for New Settings Structure**

**File to Modify:** `backend/data_access/database_manager.py`

**Instructions:** Modify the `get_qualification_settings` method to correctly retrieve and convert the new intent-specific float and integer types.

**In `DatabaseManager.get_qualification_settings`, within the `if row:` block, add the new keys to `float_keys` and `int_keys` lists.**

**Locate the `float_keys` list definition (from Task 4.7) and add the new intent-specific bid thresholds:**
```python
            float_keys = [
                # ... existing float keys ...
                "informational_max_high_top_of_page_bid", # NEW
                "commercial_max_high_top_of_page_bid", # NEW
                "transactional_max_high_top_of_page_bid", # NEW
            ]
```

**Locate the `int_keys` list definition (from Task 4.7) and add the new intent-specific KD thresholds:**
```python
                int_keys = [
                    # ... existing integer keys ...
                    "informational_max_kd_hard_limit", # NEW
                    "commercial_max_kd_hard_limit", # NEW
                    "transactional_max_kd_hard_limit", # NEW
                ]
```
**No explicit change is needed for `update_qualification_settings` as its logic to update `qualification_settings` already handles arbitrary key-value pairs if the column exists.**

**Sub-Task 6.5: Refactor `disqualification_rules.py` for Intent-Awareness**

**File to Modify:** `backend/pipeline/step_01_discovery/disqualification_rules.py`

**Instructions:** Refactor specific rules (`max_high_top_of_page_bid`, `max_kd_hard_limit`) to be intent-aware.

**Locate the `Rule 9: Prohibitively high CPC bids` logic.**

**Replace this block:**
```python
    if utils.safe_compare(
        keyword_info.get("high_top_of_page_bid"),
        client_cfg.get("max_high_top_of_page_bid", 15.0),
        "gt",
    ):
        return (
            True,
            f"Rule 9: Prohibitively high CPC bids (${client_cfg.get('max_high_top_of_page_bid', 15.00)}).",
            False,
        )
```
**With this code:**
```python
    # Rule 9: Prohibitively high CPC bids (Intent-Aware)
    main_intent = intent_info.get("main_intent", "informational")
    high_bid = keyword_info.get("high_top_of_page_bid", 0.0) or 0.0

    # Get intent-specific threshold, fallback to general if not defined
    intent_specific_bid_threshold_key = f"{main_intent}_max_high_top_of_page_bid"
    bid_threshold = client_cfg.get(intent_specific_bid_threshold_key, client_cfg.get("max_high_top_of_page_bid", 15.0))

    if utils.safe_compare(high_bid, bid_threshold, "gt"):
        return (
            True,
            f"Rule 9: High CPC bid (${high_bid:.2f}) for '{main_intent}' intent exceeds configured limit of ${bid_threshold:.2f}.",
            False,
        )
```

**Now, locate the `Rule 10: Extreme keyword difficulty` logic.**

**Replace this block:**
```python
    if utils.safe_compare(
        keyword_props.get("keyword_difficulty"),
        client_cfg.get("max_kd_hard_limit", 70),
        "gt",
    ):
        return (
            True,
            f"Rule 10: Extreme keyword difficulty (>{client_cfg.get('max_kd_hard_limit', 70)}).",
            False,
        )
```
**With this code:**
```python
    # Rule 10: Extreme keyword difficulty (Intent-Aware)
    main_intent = intent_info.get("main_intent", "informational")
    kd_value = keyword_props.get("keyword_difficulty")

    # Get intent-specific KD threshold, fallback to general if not defined
    intent_specific_kd_threshold_key = f"{main_intent}_max_kd_hard_limit"
    kd_threshold = client_cfg.get(intent_specific_kd_threshold_key, client_cfg.get("max_kd_hard_limit", 70))

    if utils.safe_compare(kd_value, kd_threshold, "gt"):
        return (
            True,
            f"Rule 10: Keyword Difficulty ({kd_value}) for '{main_intent}' intent exceeds configured limit of {kd_threshold}.",
            False,
        )
```
*(The AI agent should understand that this pattern of checking `main_intent` and deriving an intent-specific threshold should be applied to other relevant rules within `disqualification_rules.py` where a one-size-fits-all threshold is inadequate. E.g., `min_search_volume` could also be intent-sensitive).*

**Sub-Task 6.6: Redesign `DiscoverySettingsTab.jsx` for Intent Rules**

**File to Modify:** `my-content-app/src/pages/Settings/tabs/DiscoverySettingsTab.jsx`

**Instructions:** Replace the entire content of `my-content-app/src/pages/Settings/tabs/DiscoverySettingsTab.jsx` with the following code.

```javascript
import React from 'react';
import { Form, Input, InputNumber, Select, Switch, Checkbox, Slider, Typography, Row, Col, Divider, Tooltip, Space, Tabs } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

const DiscoverySettingsTab = ({ settings, form }) => {
  // Define common intent-specific rules
  const commonIntentThresholds = [
    { key: "max_high_top_of_page_bid", label: "Max High Top-of-Page Bid ($)", tooltip: "Maximum average CPC bid for top results. Keywords above this are disqualified. Adjust per intent." },
    { key: "max_kd_hard_limit", label: "Max Keyword Difficulty", tooltip: "Keywords above this difficulty (0-100) are disqualified. Adjust per intent." },
    // Add other intent-specific rules here as they are implemented
  ];

  const renderIntentRules = (intent) => (
    <Row gutter={16}>
      {commonIntentThresholds.map(rule => (
        <Col span={12} key={`${intent}_${rule.key}`}>
          <Form.Item 
            name={`${intent}_${rule.key}`} 
            label={
              <Space>
                {rule.label} ({intent.charAt(0).toUpperCase() + intent.slice(1)} Intent)
                {rule.tooltip && <Tooltip title={rule.tooltip}><InfoCircleOutlined /></Tooltip>}
              </Space>
            }
          >
            <InputNumber 
              min={rule.key.includes("bid") ? 0.0 : 0} 
              max={rule.key.includes("bid") ? 9999.0 : 100} 
              step={rule.key.includes("bid") ? 0.1 : 1} 
              style={{ width: '100%' }} 
            />
          </Form.Item>
        </Col>
      ))}
    </Row>
  );

  return (
    <>
      <Title level={5}>General Discovery Parameters</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="min_search_volume" label="Minimum Search Volume">
            <InputNumber min={0} max={100000} step={10} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_keyword_difficulty" label="Maximum Keyword Difficulty">
            <InputNumber min={0} max={100} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="min_keyword_word_count" label="Minimum Keyword Word Count">
            <InputNumber min={1} max={20} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_keyword_word_count" label="Maximum Keyword Word Count">
            <InputNumber min={1} max={20} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_max_pages" label="Max API Pages to Fetch">
            <InputNumber min={1} max={100} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_related_depth" label="Related Keywords Depth">
            <Slider min={0} max={4} />
          </Form.Item>
        </Col>
        <Col span={24}>
          <Form.Item name="discovery_strategies" label="Discovery Strategies">
            <Checkbox.Group
              options={[
                { label: 'Keyword Ideas (Category-based)', value: 'keyword_ideas' },
                { label: 'Keyword Suggestions (Phrase-based)', value: 'keyword_suggestions' },
                { label: 'Related Keywords (SERP-based)', value: 'related_keywords' },
              ]}
            />
          </Form.Item>
        </Col>
      </Row>

      <Divider />

      <Title level={5}>Advanced Filtering & Ordering</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="closely_variants" label="Search Mode (Keyword Ideas)" valuePropName="checked">
            <Switch checkedChildren="Phrase Match" unCheckedChildren="Broad Match" />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_ignore_synonyms" label="Ignore Synonyms" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_replace_with_core_keyword" label="Replace with Core Keyword" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="min_cpc_filter" label="Minimum CPC ($)">
            <InputNumber min={0.0} step={0.1} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_cpc_filter" label="Maximum CPC ($)">
            <InputNumber min={0.0} step={0.1} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="min_competition" label="Minimum Competition (0-1)">
            <InputNumber min={0.0} max={1.0} step={0.01} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_competition" label="Maximum Competition (0-1)">
            <InputNumber min={0.0} max={1.0} step={0.01} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_competition_level" label="Max Competition Level">
            <Select style={{ width: '100%' }}>
              <Option value="LOW">LOW</Option>
              <Option value="MEDIUM">MEDIUM</Option>
              <Option value="HIGH">HIGH</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_order_by_field" label="Order Results By">
            <Select style={{ width: '100%' }}>
              <Option value="keyword_info.search_volume">Search Volume</Option>
              <Option value="keyword_properties.keyword_difficulty">Keyword Difficulty</Option>
              <Option value="keyword_info.cpc">CPC</Option>
              <Option value="keyword_info.competition">Competition</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_order_by_direction" label="Order Direction">
            <Select style={{ width: '100%' }}>
              <Option value="desc">Descending</Option>
              <Option value="asc">Ascending</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={24}>
          <Form.Item 
            name="search_phrase_regex" 
            label={
              <Space>
                Keyword Regex Filter
                <Tooltip title="Use regular expressions to filter keywords (e.g., ^how to.*$)">
                  <InfoCircleOutlined />
                </Tooltip>
              </Space>
            }
          >
            <Input placeholder="e.g., ^best.*reviews$" />
          </Form.Item>
        </Col>
      </Row>

      <Divider />

      <Title level={5}>Intent & Qualification</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="enforce_intent_filter" label="Enforce Intent Filter" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="allowed_intents" label="Allowed Intents">
            <Select mode="multiple" style={{ width: '100%' }}>
              <Option value="informational">Informational</Option>
              <Option value="commercial">Commercial</Option>
              <Option value="transactional">Transactional</Option>
              <Option value="navigational">Navigational</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="prohibited_intents" label="Prohibited Secondary Intents">
            <Select mode="multiple" style={{ width: '100%' }}>
              <Option value="informational">Informational</Option>
              <Option value="commercial">Commercial</Option>
              <Option value="transactional">Transactional</Option>
              <Option value="navigational">Navigational</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="require_question_keywords" label="Require Question Keywords" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Col>
        <Col span={24}>
          <Form.Item 
            name="negative_keywords" 
            label="Negative Keywords" 
            extra="Comma-separated list of keywords to exclude (e.g., free, login)"
          >
            <Input.TextArea rows={2} />
          </Form.Item>
        </Col>
      </Row>

      <Divider />
      <Title level={5}>Intent-Specific Disqualification Rules (High-CPC / Bids)</Title>
      <Tabs defaultActiveKey="informational">
        <TabPane tab="Informational" key="informational">
          {renderIntentRules('informational')}
        </TabPane>
        <TabPane tab="Commercial" key="commercial">
          {renderIntentRules('commercial')}
        </TabPane>
        <TabPane tab="Transactional" key="transactional">
          {renderIntentRules('transactional')}
        </TabPane>
        {/* Add more tabs for other intents or specific rules if needed */}
      </Tabs>

      <Divider /><br/>
      <Title level={5}>SERP & Competitor Analysis Cost Controls</Title><br/>
      <Row gutter={16}><br/>
        <Col span={12}><br/>
          <Form.Item name="load_async_ai_overview" label="Load Async AI Overview" valuePropName="checked" tooltip="Set to true to obtain AI Overview items in SERPs even if they are loaded asynchronously. Costs $0.002 extra per SERP call."><br/>
            <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" /><br/>
          </Form.Item><br/>
        </Col><br/>
        <Col span={12}><br/>
          <Form.Item name="people_also_ask_click_depth" label="PAA Click Depth"><br/>
            <InputNumber min={0} max={4} style={{ width: '100%' }} tooltip="Specify the depth of clicks (1 to 4) on People Also Ask elements. Costs $0.00015 extra per click per level." /><br/>
          </Form.Item><br/>
        </Col><br/>
        <Col span={12}><br/>
          <Form.Item name="onpage_enable_browser_rendering" label="Enable Browser Rendering (High Cost)" valuePropName="checked" tooltip="If true, emulates a full browser load for Core Web Vitals (LCP/CLS) and loads JavaScript/Resources automatically. Primary cost factor for Analysis."><br/>
            <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" /><br/>
          </Form.Item><br/>
        </Col><br/>
        <Col span={12}><br/>
          <Form.Item name="onpage_enable_custom_js" label="Enable Custom JavaScript" valuePropName="checked" tooltip="Allows execution of custom JavaScript during OnPage crawl. Costs $0.00025 extra per page analyzed."><br/>
            <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" /><br/>
          </Form.Item><br/>
        </Col><br/>
      </Row><br/><br/>
    </>
  );
};

export default DiscoverySettingsTab;
```