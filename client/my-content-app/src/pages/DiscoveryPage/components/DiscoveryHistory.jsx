import React, { useState, useMemo } from 'react';
import { Table, Tag, Tooltip, Button, Modal, Progress, Empty, Typography, Input, Row, Col, DatePicker, Alert } from 'antd';
import { ReloadOutlined, ProfileOutlined, ClockCircleOutlined, CheckCircleOutlined, CloseCircleOutlined, LoadingOutlined, EyeOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import RunDetailsModal from './RunDetailsModal';
import DiscoveryStatsBreakdown from './DiscoveryStatsBreakdown'; // NEW: For expandable row

const { Title, Text } = Typography;
const { Search } = Input;
const { RangePicker } = DatePicker;

const STATUS_CONFIG = {
  running: { color: 'processing', text: 'Running', icon: <LoadingOutlined spin /> },
  completed: { color: 'success', text: 'Completed', icon: <CheckCircleOutlined /> },
  failed: { color: 'error', text: 'Failed', icon: <CloseCircleOutlined /> },
  pending: { color: 'default', text: 'Pending', icon: <ClockCircleOutlined /> },
};

const DiscoveryHistory = ({
  runs, totalRuns, page, setPage, isLoading, onRerun, isRerunning,
  searchQuery, setSearchQuery, setDateRange
}) => {
  const navigate = useNavigate();
  // Local state for filters is removed, now using props
  const [errorModal, setErrorModal] = useState({ open: false, content: '' });
  const [detailsModal, setDetailsModal] = useState({ open: false, run: null });

  const handleShowError = (errorMsg) => {
    setErrorModal({ open: true, content: errorMsg || 'No error details provided.' });
  };

  const handleShowDetails = (run) => {
    setDetailsModal({ open: true, run: run });
  };



  const expandedRowRender = (record) => {
    if (!record.results_summary) {
      return <Text type="secondary">No detailed summary available for this run.</Text>;
    }
    return <DiscoveryStatsBreakdown summary={record.results_summary} runId={record.id} />;
  };

  const columns = [
    {
      title: 'Start Time',
      dataIndex: 'start_time',
      key: 'start_time',
      render: (text) => text ? `${formatDistanceToNow(new Date(text))} ago` : 'N/A',
      sorter: (a, b) => new Date(a.start_time) - new Date(b.start_time),
      defaultSortOrder: 'descend',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status, record) => {
        const config = STATUS_CONFIG[status] || STATUS_CONFIG.pending;
        const progress = record.results_summary?.progress || (status === 'running' ? record.progress || 0 : 0);
        const stepMessage = record.results_summary?.step || (status === 'running' ? 'Initializing...' : null);

        return (
          <div style={{ display: 'flex', alignItems: 'center', flexDirection: 'column', gap: '4px' }}>
            <Tag icon={config.icon} color={config.color} onClick={() => status === 'failed' && handleShowError(record.error_message)} style={{ cursor: status === 'failed' ? 'pointer' : 'default' }}>
              {config.text}
            </Tag>
            {status === 'running' && (
              <>
                <Text type="secondary" style={{ fontSize: '12px', fontStyle: 'italic' }}>{stepMessage}</Text>
                <Progress percent={progress} size="small" status="active" showInfo={false} style={{ width: 100, margin: 0 }} />
              </>
            )}
          </div>
        );
      },
      sorter: (a, b) => a.status.localeCompare(b.status),
    },
    {
      title: 'Seed Keywords',
      dataIndex: 'parameters',
      key: 'seed_keywords',
      responsive: ['md'],
      render: (params) => {
        const keywords = params?.seed_keywords || [];
        if (keywords.length === 0) return <Text type="secondary">N/A</Text>;
        const displayedKeywords = keywords.slice(0, 3);
        const remainingCount = keywords.length - displayedKeywords.length;
        return (
          <>
            {displayedKeywords.map(kw => <Tag key={kw}>{kw}</Tag>)}
            {remainingCount > 0 && <Tooltip title={keywords.slice(3).join(', ')}><Tag>+{remainingCount} more</Tag></Tooltip>}
          </>
        );
      },
    },
    {
      title: 'New Keywords',
      dataIndex: 'results_summary',
      key: 'new_keywords',
      responsive: ['lg'],
      render: (summary) => summary ? <Tag color="blue">{summary.final_added_to_db || 0}</Tag> : 'N/A',
    },
    {
      title: 'Qualified',
      dataIndex: 'results_summary',
      key: 'qualified',
      responsive: ['lg'],
      render: (summary) => summary ? <Tag color="green">{summary.final_qualified_count || 0}</Tag> : 'N/A',
    },
    {
      title: 'Disqualified',
      dataIndex: 'results_summary',
      key: 'disqualified',
      responsive: ['lg'],
      render: (summary) => summary ? <Tag color="red">{summary.disqualified_count || 0}</Tag> : 'N/A',
    },
    {
      title: 'Cost',
      dataIndex: 'results_summary',
      key: 'cost',
      responsive: ['lg'],
      render: (summary) => summary ? `$${(summary.total_cost || 0).toFixed(2)}` : 'N/A',
    },
    {
      title: 'Actions',
      key: 'actions',
      align: 'right',
      fixed: 'right',
      render: (_, record) => (
        <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
          {record.status === 'completed' && (
            <>
              <Tooltip title="View Run Details">
                <Button type="default" icon={<EyeOutlined />} onClick={() => handleShowDetails(record)} />
              </Tooltip>
              <Tooltip title="View Keywords">
                <Button type="primary" icon={<ProfileOutlined />} onClick={() => navigate(`/discovery-run/${record.id}`)} />
              </Tooltip>
            </>
          )}
        </div>
      ),
    },
  ];

  return (
    <div style={{ marginTop: '32px' }}>
        <Row justify="space-between" align="middle" style={{ marginBottom: '16px' }} gutter={[16, 16]}>
            <Col><Title level={3} style={{margin: 0}}>Discovery History</Title></Col>
            <Col flex="auto" style={{textAlign: 'right'}}>
              <Search 
                placeholder="Filter by keyword or status..." 
                allowClear 
                value={searchQuery} 
                onChange={e => setSearchQuery(e.target.value)} 
                style={{ width: 250, marginRight: '8px' }} 
              />
              <RangePicker onChange={(dates) => {
                const dateStrings = dates ? [dates[0].toISOString(), dates[1].toISOString()] : null;
                setDateRange(dateStrings);
              }} />
            </Col>
        </Row>
      <Table
        loading={isLoading}
        columns={columns}
        dataSource={runs}
        rowKey="id"
        scroll={{ x: 800 }}
        locale={{ emptyText: <Empty description="No discovery runs found. Start one above to see your history." /> }}
        pagination={{
          current: page,
          pageSize: 10,
          total: totalRuns,
          onChange: setPage,
        }}
        expandable={{ expandedRowRender }} // NEW: Enable expandable rows
      />
      <Modal title="Run Failed" open={errorModal.open} onOk={() => setErrorModal({ open: false, content: '' })} onCancel={() => setErrorModal({ open: false, content: '' })} footer={[<Button key="back" onClick={() => setErrorModal({ open: false, content: '' })}>Close</Button>]}>
<Text strong>Error Message:</Text>
<pre style={{ marginTop: '8px', background: '#f5f5f5', padding: '12px', borderRadius: '4px', overflowX: 'auto', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>{errorModal.content}</pre>
</Modal>
      
      <RunDetailsModal 
        run={detailsModal.run}
        open={detailsModal.open}
        onCancel={() => setDetailsModal({ open: false, run: null })}
      />
    </div>
  );
};

export default DiscoveryHistory;
