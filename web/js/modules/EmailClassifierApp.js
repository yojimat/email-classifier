/**
 * ===================================
 * EMAIL CLASSIFIER APP MODULE
 * ===================================
 * Main application controller that coordinates all modules
 */

import { NotificationService } from "./NotificationService.js";
import { FileHandler } from "./FileHandler.js";
import { EmailProcessor } from "./EmailProcessor.js";
import { UIManager } from "./UIManager.js";

export class EmailClassifierApp {
  constructor() {
    this.notificationService = null;
    this.fileHandler = null;
    this.emailProcessor = null;
    this.uiManager = null;
    this.isInitialized = false;
  }

  /**
   * @param {Object} config - Configuration options
   */
  async init(config = {}) {
    try {
      console.log("🚀 Initializing Email Classifier App...");

      await this.initializeServices(config);
      this.attachGlobalEventHandlers();

      this.isInitialized = true;
      console.log("✅ Email Classifier App initialized successfully");
    } catch (error) {
      console.error("❌ Error initializing Email Classifier App:", error);
      this.handleInitializationError(error);
    }
  }

  /**
   * @param {Object} config - Configuration options
   */
  async initializeServices(config) {
    // Initialize notification service first (other services depend on it)
    this.notificationService = new NotificationService();
    this.notificationService.init(config.toastSelector);

    this.uiManager = new UIManager(this.notificationService);
    this.uiManager.init(config.uiElements);

    this.fileHandler = new FileHandler(this.notificationService);
    this.fileHandler.init(config.fileElements);

    this.emailProcessor = new EmailProcessor(this.notificationService);

    if (config.apiEndpoint) {
      this.emailProcessor.setAPIEndpoint(config.apiEndpoint);
    }

    if (config.requestTimeout) {
      this.emailProcessor.setTimeout(config.requestTimeout);
    }
  }

  attachGlobalEventHandlers() {
    window.addEventListener("unhandledrejection", (event) => {
      console.error("Unhandled promise rejection:", event.reason);
      this.notificationService?.error("Erro inesperado no sistema");
      event.preventDefault();
    });

    window.addEventListener("error", (event) => {
      console.error("Global error:", event.error);
      this.notificationService?.error("Erro inesperado no sistema");
    });

    this.attachButtonEventListeners();
  }

  attachButtonEventListeners() {
    const processBtn = document.getElementById("processBtn");
    if (processBtn) {
      processBtn.addEventListener("click", this.processEmail.bind(this));
    }

    const clearBtn = document.getElementById("clearBtn");
    if (clearBtn) {
      clearBtn.addEventListener("click", this.clearForm.bind(this));
    }

    const copyResponseBtn = document.getElementById("copyResponseBtn");
    if (copyResponseBtn) {
      copyResponseBtn.addEventListener("click", this.copyResponse.bind(this));
    }
  }

  /**
   * Main function called when user clicks "Processar Email"
   */
  async processEmail() {
    if (!this.isInitialized) {
      this.notificationService?.error("Sistema não inicializado");
      return;
    }

    try {
      const content = this.uiManager.getEmailContent();

      if (!content) {
        this.notificationService.warning(
          "Por favor, insira o conteúdo do email"
        );
        return;
      }

      this.uiManager.setProcessingState(true);

      console.log("📧 Processing email...");

      const results = await this.emailProcessor.processEmail(content);

      this.uiManager.displayResults(results);

      console.log("✅ Email processed successfully");
      this.notificationService.success("Email processado com sucesso!");
    } catch (error) {
      console.error("Error processing email:", error);
    } finally {
      this.uiManager.setProcessingState(false);
    }
  }

  clearForm() {
    if (!this.isInitialized) {
      return;
    }

    this.uiManager.clearForm();
    this.fileHandler.clearFile();

    console.log("🧹 Form cleared");
    this.notificationService.success("Formulário limpo com sucesso!");
  }

  async copyResponse() {
    if (!this.isInitialized) {
      return;
    }

    await this.uiManager.copyResponse();
  }

  /**
   * @param {Error} error - Initialization error
   */
  handleInitializationError(error) {
    // Try to show error through notification service if available
    if (this.notificationService) {
      this.notificationService.error("Erro ao inicializar o sistema");
    } else {
      // Fallback to alert if notification service is not available
      alert(
        "Erro ao inicializar o sistema. Verifique o console para mais detalhes."
      );
    }
  }

  destroy() {
    if (this.fileHandler) {
      this.fileHandler.destroy();
    }

    // Reset state
    this.isInitialized = false;
    this.notificationService = null;
    this.fileHandler = null;
    this.emailProcessor = null;
    this.uiManager = null;

    console.log("🧹 Email Classifier App destroyed");
  }
}
