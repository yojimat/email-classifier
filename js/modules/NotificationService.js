/**
 * ===================================
 * NOTIFICATION SERVICE MODULE
 * ===================================
 * Handles toast notifications and user feedback
 */

export class NotificationService {
  constructor() {
    this.toastElement = null;
    this.defaultDuration = 4000;
  }

  /**
   * Initialize the notification service
   * @param {string} toastSelector - CSS selector for toast element
   */
  init(toastSelector = "#toast") {
    this.toastElement = document.querySelector(toastSelector);
    if (!this.toastElement) {
      console.warn(
        "Toast element not found. Notifications may not work properly."
      );
    }
  }

  /**
   * Show a toast notification
   * @param {string} message - Message to display
   * @param {string} type - Type of notification ('success', 'error', 'warning', 'info')
   * @param {number} duration - Duration in milliseconds (optional)
   */
  show(message, type = "success", duration = this.defaultDuration) {
    if (!this.toastElement) {
      console.error("Toast element not initialized");
      return;
    }

    if (!message || typeof message !== "string") {
      console.error("Invalid message provided to notification service");
      return;
    }

    const validTypes = ["success", "error", "warning", "info"];
    if (!validTypes.includes(type)) {
      console.warn(`Invalid notification type: ${type}. Using 'info' instead.`);
      type = "info";
    }

    this.toastElement.textContent = message;
    this.toastElement.className = `toast ${type}`;
    this.toastElement.style.display = "block";

    setTimeout(() => {
      this.hide();
    }, duration);

    console.log(`📢 Notification shown: ${type} - ${message}`);
  }

  hide() {
    if (this.toastElement) {
      this.toastElement.style.display = "none";
    }
  }

  /**
   * Show success notification
   * @param {string} message - Success message
   * @param {number} duration - Duration in milliseconds (optional)
   */
  success(message, duration) {
    this.show(message, "success", duration);
  }

  /**
   * Show error notification
   * @param {string} message - Error message
   * @param {number} duration - Duration in milliseconds (optional)
   */
  error(message, duration) {
    this.show(message, "error", duration);
  }

  /**
   * Show warning notification
   * @param {string} message - Warning message
   * @param {number} duration - Duration in milliseconds (optional)
   */
  warning(message, duration) {
    this.show(message, "warning", duration);
  }

  /**
   * Show info notification
   * @param {string} message - Info message
   * @param {number} duration - Duration in milliseconds (optional)
   */
  info(message, duration) {
    this.show(message, "info", duration);
  }
}
