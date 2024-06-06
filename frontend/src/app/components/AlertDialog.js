import PropTypes from "prop-types";
import * as React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";

const AlertDialog = (props) => {
  const {
    open,
    dialogue,
    title,
    cancelText,
    handleCancel,
    confirmText,
    handleConfirm,
  } = props;

  if (!open) {
    return null;
  }
  return (
    <div>
      <Dialog
        open={true}
        onClose={() => {
          handleCancel();
        }}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{title}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {dialogue}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => {
              handleCancel();
            }}
          >
            {cancelText}
          </Button>
          <Button
            onClick={() => {
              handleConfirm();
            }}
            autoFocus
          >
            {confirmText}
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

AlertDialog.defaultProps = {
  dialogue: "",
  title: "",
};
AlertDialog.propTypes = {
  open: PropTypes.bool.isRequired,
  title: PropTypes.string,
  dialogue: PropTypes.string,
  cancelText: PropTypes.string.isRequired,
  handleCancel: PropTypes.func.isRequired,
  confirmText: PropTypes.string.isRequired,
  handleConfirm: PropTypes.func.isRequired,
};

export default AlertDialog;
