/**
 * ===================================
 * UI MANAGER MODULE
 * ===================================
 * Manages UI state, interactions, and result display
 */

export class UIManager {
  constructor(notificationService) {
    this.notificationService = notificationService;
    this.elements = {};
    this.isProcessing = false;
  }

  /**
   * @param {Object} elementSelectors - Object containing CSS selectors for UI elements
   */
  init(elementSelectors = {}) {
    const selectors = { ...elementSelectors };
    for (const [key, selector] of Object.entries(selectors)) {
      this.elements[key] = document.querySelector(selector);
    }

    this.validateCriticalElements();
  }

  validateCriticalElements() {
    const criticalElements = ["emailText", "processBtn"];

    for (const elementKey of criticalElements) {
      if (!this.elements[elementKey]) {
        throw new Error(`Critical UI element '${elementKey}' not found`);
      }
    }
  }

  /**
   * @returns {string} - Email content
   */
  getEmailContent() {
    return this.elements.emailText?.value?.trim() || "";
  }

  /**
   * @param {string} content - Email content to set
   */
  setEmailContent(content) {
    if (this.elements.emailText && typeof content === "string") {
      this.elements.emailText.value = content;
    }
  }

  clearEmailContent() {
    this.setEmailContent("");
  }

  /**
   * Set processing state
   * @param {boolean} processing - Whether processing is active
   */
  setProcessingState(processing) {
    this.isProcessing = processing;

    if (this.elements.processBtn) {
      this.elements.processBtn.disabled = processing;
      this.elements.processBtn.children[1].textContent = processing
        ? "Processando..."
        : "Processar Email";
    }

    if (this.elements.clearBtn) {
      this.elements.clearBtn.disabled = processing;
    }

    if (this.elements.loading) {
      this.elements.loading.style.display = processing ? "block" : "none";
    }

    if (processing && this.elements.results) {
      this.elements.results.style.display = "none";
    }

    if (this.elements.emptyResult) {
      this.elements.emptyResult.style.display =
        this.elements.results.style.display === "none" && !processing
          ? "block"
          : "none";
    }
  }

  /**
   * Display processing results
   * @param {Object} data - Processing results data
   */
  displayResults(data) {
    try {
      if (!data || typeof data !== "object") {
        throw new Error("Invalid results data");
      }

      if (this.elements.results) {
        this.elements.results.style.display = "block";
      }

      this.updateCategoryBadge(data.category);
      this.updateConfidence(data.confidence);
      this.updateSuggestedResponse(data.response);
      this.updateStatistics(data);

      console.log("✅ Results displayed successfully");
    } catch (error) {
      console.error("Error displaying results:", error);
      this.notificationService?.error("Não foi possível exibir os resultados.");
      throw error;
    }
  }

  /**
   * @param {string} category - Email category
   */
  updateCategoryBadge(category) {
    if (!this.elements.categoryBadge) return;

    const isProductive = category === "productive";

    this.elements.categoryBadge.className = `category-badge ${
      isProductive ? "productive" : "unproductive"
    }`;

    this.elements.categoryBadge.textContent = isProductive
      ? "✅ Produtivo"
      : "⚠️ Improdutivo";
  }

  /**
   * @param {number} confidence - Confidence score
   */
  updateConfidence(confidence) {
    if (this.elements.confidence) {
      const validConfidence = this.validateConfidence(confidence);
      this.elements.confidence.textContent = `Confiança: ${validConfidence}%`;
    }
  }

  /**
   * @param {string} response - Suggested response text
   */
  updateSuggestedResponse(response) {
    if (this.elements.suggestedResponse) {
      this.elements.suggestedResponse.innerHTML =
        response || "Resposta não disponível";
    }
  }

  /**
   * @param {Object} data - Results data containing statistics
   */
  updateStatistics(data) {
    if (this.elements.wordCount) {
      const wordCount =
        data.word_count || this.countWords(this.getEmailContent());
      this.elements.wordCount.textContent = wordCount;
    }

    if (this.elements.processingTime && data.processingTime !== undefined) {
      const secsWithOneDecimal = data.processingTime.toFixed(1);
      this.elements.processingTime.textContent = `${secsWithOneDecimal}s`;
    }

    if (this.elements.accuracyScore) {
      const confidence = this.validateConfidence(data.confidence);
      this.elements.accuracyScore.textContent = `${confidence}%`;
    }
  }

  clearForm() {
    this.clearEmailContent();

    if (this.elements.fileInfo) {
      this.elements.fileInfo.style.display = "none";
    }

    if (this.elements.results) {
      this.elements.results.style.display = "none";
    }

    this.setProcessingState(false);
  }

  async copyResponse() {
    try {
      if (!this.elements.suggestedResponse) {
        throw new Error("Elemento de resposta não encontrado");
      }

      const responseText = this.elements.suggestedResponse.innerText;

      if (!responseText || responseText.trim() === "") {
        return;
      }

      await navigator.clipboard.writeText(responseText);
      this.notificationService?.success("Resposta copiada com sucesso!");
    } catch (error) {
      console.error("Error copying response:", error);
      this.notificationService?.error("Não foi possível copiar a resposta.");
    }
  }

  /**
   * @param {number} confidence - Confidence score
   * @returns {number} - Normalized confidence (0-100)
   */
  validateConfidence(confidence) {
    const numConfidence = Number(confidence);

    if (isNaN(numConfidence)) {
      throw new Error("Confiança inválida");
    }

    return Math.max(0, Math.min(100, Math.round(numConfidence)));
  }

  /**
   * @param {string} text - Text to count words in
   * @returns {number} - Word count
   */
  countWords(text) {
    if (!text || typeof text !== "string") {
      return 0;
    }

    return text
      .trim()
      .split(/\s+/)
      .filter((word) => word.length > 0).length;
  }
}
