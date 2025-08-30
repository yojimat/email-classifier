/**
 * ===================================
 * FILE HANDLER MODULE
 * ===================================
 * Manages file upload, drag-and-drop functionality, and file processing
 */

export class FileHandler {
  constructor(notificationService) {
    this.notificationService = notificationService;
    this.uploadArea = null;
    this.fileInput = null;
    this.fileInfo = null;
    this.fileName = null;
    this.emailText = null;

    // Supported file types
    this.supportedTypes = ["text/plain", "application/pdf"];
    this.supportedExtensions = [".txt", ".pdf"];

    // Event handlers bound to this instance
    this.boundHandlers = {
      handleClick: this.handleClick.bind(this),
      handleDragOver: this.handleDragOver.bind(this),
      handleDragLeave: this.handleDragLeave.bind(this),
      handleDrop: this.handleDrop.bind(this),
      handleFileSelect: this.handleFileSelect.bind(this),
    };
  }

  /**
   * Initialize the file handler with DOM elements
   * @param {Object} elements - Object containing DOM element selectors
   */
  init(elements = {}) {
    const {
      uploadArea = "#uploadArea",
      fileInput = "#fileInput",
      fileInfo = "#fileInfo",
      fileName = "#fileName",
      emailText = "#emailText",
    } = elements;

    try {
      this.uploadArea = document.querySelector(uploadArea);
      this.fileInput = document.querySelector(fileInput);
      this.fileInfo = document.querySelector(fileInfo);
      this.fileName = document.querySelector(fileName);
      this.emailText = document.querySelector(emailText);

      this.validateElements();
      this.attachEventListeners();

      console.log("✅ FileHandler initialized successfully");
    } catch (error) {
      console.error("❌ Error initializing FileHandler:", error);
      this.notificationService?.error(
        "Erro ao inicializar o sistema de arquivos"
      );
    }
  }

  /**
   * Validate that all required DOM elements are present
   */
  validateElements() {
    const requiredElements = {
      uploadArea: this.uploadArea,
      fileInput: this.fileInput,
      emailText: this.emailText,
    };

    for (const [name, element] of Object.entries(requiredElements)) {
      if (!element) {
        throw new Error(`Required element '${name}' not found`);
      }
    }
  }

  /**
   * Attach event listeners to DOM elements
   */
  attachEventListeners() {
    if (this.uploadArea) {
      this.uploadArea.addEventListener("click", this.boundHandlers.handleClick);
      this.uploadArea.addEventListener(
        "dragover",
        this.boundHandlers.handleDragOver
      );
      this.uploadArea.addEventListener(
        "dragleave",
        this.boundHandlers.handleDragLeave
      );
      this.uploadArea.addEventListener("drop", this.boundHandlers.handleDrop);
    }

    if (this.fileInput) {
      this.fileInput.addEventListener(
        "change",
        this.boundHandlers.handleFileSelect
      );
    }
  }

  destroy() {
    if (this.uploadArea) {
      this.uploadArea.removeEventListener(
        "click",
        this.boundHandlers.handleClick
      );
      this.uploadArea.removeEventListener(
        "dragover",
        this.boundHandlers.handleDragOver
      );
      this.uploadArea.removeEventListener(
        "dragleave",
        this.boundHandlers.handleDragLeave
      );
      this.uploadArea.removeEventListener(
        "drop",
        this.boundHandlers.handleDrop
      );
    }

    if (this.fileInput) {
      this.fileInput.removeEventListener(
        "change",
        this.boundHandlers.handleFileSelect
      );
    }
  }

  /**
   * Handle click on upload area
   */
  handleClick() {
    if (this.fileInput) {
      this.fileInput.click();
    }
  }

  /**
   * Handle drag over event
   * @param {DragEvent} event - Drag event
   */
  handleDragOver(event) {
    event.preventDefault();
    this.uploadArea?.classList.add("active");
  }

  /**
   * Handle drag leave event
   */
  handleDragLeave() {
    this.uploadArea?.classList.remove("active");
  }

  /**
   * Handle file drop event
   * @param {DragEvent} event - Drop event
   */
  handleDrop(event) {
    event.preventDefault();
    this.uploadArea?.classList.remove("active");

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.processFile(files[0]);
    }
  }

  /**
   * Handle file selection from input
   * @param {Event} event - Change event
   */
  handleFileSelect(event) {
    const files = event.target?.files;
    if (files && files.length > 0) {
      this.processFile(files[0]);
    }
  }

  /**
   * Process the selected file
   * @param {File} file - File object to process
   */
  async processFile(file) {
    try {
      // Validate file type
      if (!this.isValidFileType(file)) {
        this.notificationService?.error(
          `Por favor, selecione um arquivo ${this.supportedExtensions.join(
            " ou "
          )}`
        );
        return;
      }

      // Update UI with file info
      this.updateFileInfo(file);

      // Process file content if it's a text file
      if (file.type === "text/plain") {
        await this.readTextFile(file);
      } else {
        this.notificationService?.info(
          "Arquivo PDF carregado. Processamento manual necessário."
        );
      }

      console.log(`📄 File processed: ${file.name}`);
    } catch (error) {
      console.error("Error processing file:", error);
      this.notificationService?.error("Erro ao processar o arquivo");
    }
  }

  /**
   * Validate file type
   * @param {File} file - File to validate
   * @returns {boolean} - Whether file type is supported
   */
  isValidFileType(file) {
    return this.supportedTypes.includes(file.type);
  }

  /**
   * Update file info display
   * @param {File} file - File object
   */
  updateFileInfo(file) {
    if (this.fileName) {
      this.fileName.textContent = `📄 ${file.name}`;
    }

    if (this.fileInfo) {
      this.fileInfo.style.display = "block";
    }
  }

  /**
   * Read text file content
   * @param {File} file - Text file to read
   * @returns {Promise<string>} - File content
   */
  readTextFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = (event) => {
        const content = event.target?.result;
        if (this.emailText && content) {
          this.emailText.value = content;
        }
        resolve(content);
      };

      reader.onerror = () => {
        reject(new Error("Erro ao ler o arquivo"));
      };

      reader.readAsText(file);
    });
  }

  /**
   * Clear file selection and reset UI
   */
  clearFile() {
    if (this.fileInput) {
      this.fileInput.value = "";
    }

    if (this.fileInfo) {
      this.fileInfo.style.display = "none";
    }

    if (this.fileName) {
      this.fileName.textContent = "";
    }
  }

  /**
   * Get current file input element
   * @returns {HTMLInputElement|null} - File input element
   */
  getFileInput() {
    return this.fileInput;
  }
}
