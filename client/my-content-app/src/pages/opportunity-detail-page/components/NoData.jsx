import React from 'react';
import { Empty } from 'antd';

const NoData = ({ description }) => {
  return (
    <Empty
      image={Empty.PRESENTED_IMAGE_SIMPLE}
      description={
        <span>
          {description || 'No data available at this stage.'}
        </span>
      }
    />
  );
};

export default NoData;