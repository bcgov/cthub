import React from 'react';
import { CircularProgress } from '@mui/material';

const Loading = ({ color = 'inherit' }) => {
  return (
    <CircularProgress sx={{ color: color }} />
  );
};

export default Loading;
