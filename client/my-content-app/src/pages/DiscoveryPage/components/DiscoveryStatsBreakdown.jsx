import React, { useState } from 'react';
import { Row, Col, Typography, Empty, Modal, Table } from 'antd';
import PieChartCard from './PieChartCard';
import FunnelChart from './FunnelChart'; // NEW: From Task 35
import { getDisqualifiedKeywords } from '../../../services/discoveryService';

const { Title, Text } = Typography;

const DiscoveryStatsBreakdown = ({ summary, runId }) => {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalTitle, setModalTitle] = useState('');
  const [modalData, setModalData] = useState([]);
  const [modalLoading, setModalLoading] = useState(false);

  if (!summary) {
    return <Empty description="No summary data available for this run." />;
  }

  const handleReasonClick = async (reason) => {
    setModalTitle(`Disqualified Keywords: ${reason}`);
    setModalVisible(true);
    setModalLoading(true);
    try {
      const data = await getDisqualifiedKeywords(runId, reason);
      setModalData(data);
    } catch (error) {
      console.error('Failed to fetch disqualified keywords:', error);
    } finally {
      setModalLoading(false);
    }
  };

  // Destructure with defaults to prevent errors if fields are missing
  const {
    source_counts = {},
    disqualification_reasons = {},
    total_raw_count = 0,
    total_unique_count = 0,
    disqualified_count = 0,
    final_added_to_db = 0,
    final_qualified_count = 0
  } = summary;

  const modalColumns = [
    {
      title: 'Keyword',
      dataIndex: 'keyword',
      key: 'keyword',
    },
    {
      title: 'Search Volume',
      dataIndex: ['keyword_info', 'search_volume'],
      key: 'search_volume',
    },
  ];

  return (
    <div style={{ padding: '16px', backgroundColor: '#fafafa' }}>
      <Row gutter={[32, 32]}>
        {/* Section 1: Keyword Sources */}
        <Col xs={24} md={12} lg={8}>
          <PieChartCard title="Keyword Sources" data={source_counts} />
        </Col>

        {/* Section 2: Processing Funnel (Visualized) */}
        <Col xs={24} lg={16}>
            <FunnelChart 
                totalRaw={total_raw_count}
                unique={total_unique_count}
                qualified={final_qualified_count}
                disqualified={disqualified_count}
                addedToDB={final_added_to_db}
            />
        </Col>

        {/* Section 3: Disqualification Reasons */}
        <Col xs={24} md={12} lg={8}>
          <PieChartCard title="Disqualification Reasons" data={disqualification_reasons} onSliceClick={handleReasonClick} />
        </Col>
      </Row>
      <Modal
        title={modalTitle}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={800}
      >
        <Table
          loading={modalLoading}
          dataSource={modalData}
          columns={modalColumns}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Modal>
    </div>
  );
};

export default DiscoveryStatsBreakdown;
