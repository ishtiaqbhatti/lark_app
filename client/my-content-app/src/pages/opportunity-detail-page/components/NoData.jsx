import React from 'react';
import { Empty } from 'antd';

const NoData = ({ description }) => {
  return (
    <div style={{ padding: '24px', textAlign: 'center' }}>
      <Empty
        image={Empty.PRESENTED_IMAGE_SIMPLE}
        description={description || 'No data available for this section.'}
      />
    </div>
  );
};

export default NoData;
