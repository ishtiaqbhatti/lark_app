// This is a new file. Create it with the following content:
// You'll need to install react-diff-viewer: npm install react-diff-viewer
import React from 'react';
import DiffViewer from 'react-diff-viewer';
import { Typography } from 'antd';

const { Text } = Typography;

const ContentDiffViewer = ({ oldValue, newValue, oldTitle = "Previous Version", newTitle = "Current Version" }) => {
  if (!oldValue && !newValue) {
    return <Text type="secondary">No content to compare.</Text>;
  }
  if (oldValue === newValue) {
    return <Text type="success">Content is identical.</Text>;
  }

  return (
    <DiffViewer
      oldValue={oldValue || ''}
      newValue={newValue || ''}
      splitView={true}
      leftTitle={oldTitle}
      rightTitle={newTitle}
      showDiffOnly={false} // Show entire file with diffs highlighted
      use={true} // Enable styling
      styles={{
        variables: {
          dark: {
            diffViewerBackground: '#262626',
            diffViewerColor: '#f0f2f5',
            addedBackground: '#003a29',
            removedBackground: '#320a0b',
            wordAddedBackground: '#006d3d',
            wordRemovedBackground: '#9e2b2f',
          },
        },
        diffContainer: {
          fontSize: '12px',
          fontFamily: 'monospace',
        },
        line: {
          wordBreak: 'break-word',
        }
      }}
    />
  );
};

export default ContentDiffViewer;