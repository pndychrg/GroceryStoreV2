import { useToast } from "vue-toastification";

const toast = useToast();
const options = {
  position: "top-right",
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: false,
  pauseOnHover: false,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: true,
  closeButton: "button",
  icon: true,
  rtl: false,
};
export function showSuccessToast(message) {
  toast.success(message, options);
}

export function showErrorToast(message) {
  toast.error(message, options);
}

export function showInfoToast(message) {
  toast.info(message, options);
}

export function showWarningToast(message) {
  toast.warning(message, options);
}
