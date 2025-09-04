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

    this.supportedTypes = ["text/plain", "application/pdf"];
    this.supportedExtensions = [".txt", ".pdf"];

    this.boundHandlers = {
      handleClick: this.handleClick.bind(this),
      handleDragOver: this.handleDragOver.bind(this),
      handleDragLeave: this.handleDragLeave.bind(this),
      handleDrop: this.handleDrop.bind(this),
      handleFileSelect: this.handleFileSelect.bind(this),
    };
  }

  /**
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

  handleClick() {
    if (this.fileInput) {
      this.fileInput.click();
    }
  }

  /**
   * @param {DragEvent} event - Drag event
   */
  handleDragOver(event) {
    event.preventDefault();
    this.uploadArea?.classList.add("active");
  }

  handleDragLeave() {
    this.uploadArea?.classList.remove("active");
  }

  /**
   * @param {DragEvent} event - Drop event
   */
  handleDrop(event) {
    event.preventDefault();
    this.uploadArea?.classList.remove("active");

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.loadFile(files[0]);
    }
  }

  /**
   * @param {Event} event - Change event
   */
  handleFileSelect(event) {
    const files = event.target?.files;
    if (files && files.length > 0) {
      this.loadFile(files[0]);
    }
  }

  /**
   * @param {File} file - File object to process
   */
  async loadFile(file) {
    try {
      if (!this.isValidFileType(file)) {
        this.notificationService?.error(
          `Por favor, selecione um arquivo ${this.supportedExtensions.join(
            " ou "
          )}`
        );
        return;
      }

      this.updateFileInfo(file);

      if (file.type === "text/plain") {
        await this.readTextFile(file);
      } else {
        this.emailText.value = "";
      }

      console.log(`📄 File loaded: ${file.name}`);
    } catch (error) {
      console.error("Error loading file:", error);
      this.notificationService?.error("Não foi possível carregar o arquivo.");
    }
  }

  /**
   * @param {File} file - File to validate
   * @returns {boolean} - Whether file type is supported
   */
  isValidFileType(file) {
    return this.supportedTypes.includes(file.type);
  }

  /**
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
   * @param {File} file - Text file to read
   * @returns {Promise<string>} - File content
   */
  readTextFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = (event) => {
        const content = event.target?.result;
        if (this.emailText && content) {
          this.clearFile();
          this.emailText.value = content;
        }
        resolve(content);
      };

      reader.onerror = () => {
        reject(new Error("Erro ao ler o arquivo"));
      };

      reader.readAsText(file, "UTF-8");
    });
  }

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

  getFile() {
    return this.fileInput?.files?.[0] || null;
  }
}
