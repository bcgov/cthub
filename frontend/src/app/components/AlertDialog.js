import PropTypes from "prop-types";
import * as React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";

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
        <DialogTitle id="alert-dialog-title">
          <InfoOutlinedIcon className="error" /> {title}
        </DialogTitle>
        <DialogContent>
          <DialogContent id="alert-dialog-description">
            {dialogue}
          </DialogContent>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => {
              handleCancel();
            }}
          >
            {cancelText}
          </Button>
          {confirmText && (
            <Button
              onClick={() => {
                handleConfirm();
              }}
              autoFocus
            >
              {confirmText}
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </div>
  );
};

AlertDialog.defaultProps = {
  dialogue: "",
  title: "",
  cancelText: "cancel",
  confirmText: "",
};
AlertDialog.propTypes = {
  open: PropTypes.bool.isRequired,
  title: PropTypes.string,
  dialogue: PropTypes.oneOfType([PropTypes.string, PropTypes.object])
    .isRequired,
  cancelText: PropTypes.string,
  handleCancel: PropTypes.func.isRequired,
  confirmText: PropTypes.string,
  handleConfirm: PropTypes.func.isRequired,
};

export default AlertDialog;
