import PropTypes from 'prop-types';
import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export default function AlertDialog(props) {
  const {
    open, setOpen, rightButtonText, dialogue, leftButtonText, setReplaceData, title
  } = props;
  const handleClose = (trueFalse) => {
    setReplaceData(trueFalse);
    setOpen(false);
  };

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {title}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {dialogue}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            handleClose(false);
          }}
          >
            {leftButtonText}

          </Button>
          <Button
            onClick={() => {
              handleClose(true);
            }}
            autoFocus
          >
            {rightButtonText}
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
AlertDialog.defaultProps = {
  rightButtonText: '',
  dialogue: '',
  leftButtonText: '',
  setReplaceData: '',
};
AlertDialog.propTypes = {
  open: PropTypes.bool.isRequired,
  setOpen: PropTypes.func.isRequired,
  rightButtonText: PropTypes.string,
  dialogue: PropTypes.string,
  leftButtonText: PropTypes.string,
  setReplaceData: PropTypes.func,
};
