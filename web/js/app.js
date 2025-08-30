/**
 * ===================================
 * APPLICATION ENTRY POINT
 * ===================================
 * Initializes and starts the Email Classifier application
 */

import { EmailClassifierApp } from "./modules/EmailClassifierApp.js";
import { initializeComponents } from "./componentsInit.js";
import { APP_CONFIG } from "./appConfig.js";

/**
 * Global application instance
 */
let emailClassifierApp = null;

async function initializeApp() {
  try {
    console.log("🌟 Starting Email Classifier Application...");

    emailClassifierApp = new EmailClassifierApp();

    await emailClassifierApp.init(APP_CONFIG);

    // Make app instance globally available for debugging
    if (typeof window !== "undefined") {
      window.emailClassifierApp = emailClassifierApp;
    }

    console.log("🎉 Application started successfully!");
  } catch (error) {
    console.error("💥 Failed to initialize application:", error);

    const errorMessage =
      "Erro ao inicializar a aplicação. Verifique a conexão com a internet e tente novamente.";

    // Try to show error in a toast if possible, otherwise use alert
    if (typeof showToast === "function") {
      showToast(errorMessage, "error");
    } else {
      alert(errorMessage);
    }
  }
}

/**
 * Handle application cleanup on page unload
 */
function handlePageUnload() {
  if (emailClassifierApp) {
    emailClassifierApp.destroy();
    emailClassifierApp = null;
  }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
  window.addEventListener("beforeunload", handlePageUnload);

  window.addEventListener("online", () => {
    console.log("🌐 Application is online");
    if (emailClassifierApp?.notificationService) {
      emailClassifierApp.notificationService.success("Conexão restaurada");
    }
  });

  window.addEventListener("offline", () => {
    console.log("📴 Application is offline");
    if (emailClassifierApp?.notificationService) {
      emailClassifierApp.notificationService.warning(
        "Sem conexão com a internet"
      );
    }
  });
}

async function startApplication() {
  setupEventListeners();
  await initializeComponents();
  await initializeApp();
}

/**
 * Auto-start when DOM is ready
 */
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", startApplication);
} else {
  startApplication();
}
