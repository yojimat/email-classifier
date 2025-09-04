/**
 * ===================================
 * EMAIL PROCESSOR MODULE
 * ===================================
 * Handles email processing, API communication, and response generation
 */

export class EmailProcessor {
  constructor(notificationService) {
    this.notificationService = notificationService;
    this.apiEndpoint = "http://localhost:5000/api/classify";
    this.apiEndpointFile = "http://localhost:5000/api/classify-file";
    this.requestTimeout = 30000; // 30 seconds
  }

  /**
   * @param {string} content - Email content to process
   * @returns {Promise<Object>} - Processing results
   */
  async processEmail(content) {
    try {
      this.validateEmailContent(content);

      const startTime = Date.now();
      const result = await this.callClassificationAPI(content);
      result.processingTime = this.calculateProcessingTime(startTime);

      return result;
    } catch (error) {
      console.error("Error processing email:", error);
      throw error;
    }
  }

  async processEmailFile(file) {
    try {
      const startTime = Date.now();

      const result = await this.callClassificationFileAPI(file);
      result.processingTime = this.calculateProcessingTime(startTime);

      return result;
    } catch (error) {
      console.error("Error processing email file:", error);
      throw error;
    }
  }

  /**
   * @param {string} content - Email content to validate
   */
  validateEmailContent(content) {
    if (!content || typeof content !== "string") {
      this.notificationService?.warning(
        "Por favor, insira o conteúdo do email"
      );
      throw new Error("Conteúdo do email é obrigatório");
    }

    const trimmedContent = content.trim();
    if (trimmedContent.length === 0) {
      this.notificationService?.warning(
        "Por favor, insira o conteúdo do email"
      );
      throw new Error("Por favor, insira o conteúdo do email");
    }

    if (trimmedContent.length < 10) {
      this.notificationService?.warning(
        "Conteúdo do email muito curto (mínimo 10 caracteres)"
      );
      throw new Error("Conteúdo do email muito curto (mínimo 10 caracteres)");
    }

    if (trimmedContent.length > 10000) {
      this.notificationService?.warning(
        "Conteúdo do email muito longo (máximo 10.000 caracteres)"
      );
      throw new Error(
        "Conteúdo do email muito longo (máximo 10.000 caracteres)"
      );
    }
  }

  /**
   * @param {string} content - Email content
   * @returns {Promise<Object>} - API response
   */
  async callClassificationAPI(content) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.requestTimeout);

    try {
      const response = await fetch(this.apiEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email_content: content.trim(),
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(
          `Erro do servidor: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      return this.validateAPIResponse(data);
    } catch (error) {
      clearTimeout(timeoutId);

      this.notificationService?.error(
        "Não foi possível processar o email, tente novamente."
      );

      if (error.name === "AbortError") {
        throw new Error("Timeout na requisição para o servidor");
      }

      throw error;
    }
  }

  async callClassificationFileAPI(file) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.requestTimeout);
    const form = new FormData();
    form.append("file", file);

    try {
      const response = await fetch(this.apiEndpointFile, {
        method: "POST",
        body: form,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(
          `Erro do servidor: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      return this.validateAPIResponse(data);
    } catch (error) {
      clearTimeout(timeoutId);

      this.notificationService?.error(
        "Não foi possível processar o email, tente novamente."
      );

      if (error.name === "AbortError") {
        throw new Error("Timeout na requisição para o servidor");
      }

      throw error;
    }
  }

  /**
   * @param {Object} data - API response data
   * @returns {Object} - Validated response
   */
  validateAPIResponse(data) {
    if (!data || typeof data !== "object") {
      throw new Error("Resposta inválida da API");
    }

    return {
      category: data.category || "unknown",
      confidence: this.validateConfidence(data.confidence),
      response: data.response || "Resposta não disponível",
      word_count: data.word_count || 0,
      metadata: data.metadata || {},
    };
  }

  /**
   * Validate and normalize confidence score
   * @param {number} confidence - Confidence score
   * @returns {number} - Normalized confidence (0-100)
   */
  validateConfidence(confidence) {
    const numConfidence = Number(confidence);

    if (isNaN(numConfidence)) {
      return 85; // Default confidence
    }

    // Ensure confidence is between 0 and 100
    return Math.max(0, Math.min(100, Math.round(numConfidence)));
  }

  /**
   * Count words in content
   * @param {string} content - Text content
   * @returns {number} - Word count
   */
  countWords(content) {
    return content
      .trim()
      .split(/\s+/)
      .filter((word) => word.length > 0).length;
  }

  /**
   * Generate mock confidence score
   * @returns {number} - Confidence percentage
   */
  generateMockConfidence() {
    return Math.floor(Math.random() * 20) + 80; // 80-99%
  }

  /**
   * @param {number} startTime - Start timestamp
   * @returns {number} - Processing time in seconds
   */
  calculateProcessingTime(startTime) {
    return (Date.now() - startTime) / 1000;
  }

  /**
   * @param {string} endpoint - New API endpoint URL
   */
  setAPIEndpoint(endpoint) {
    if (typeof endpoint === "string" && endpoint.trim()) {
      this.apiEndpoint = endpoint.trim();
    }
  }

  /**
   * @param {string} endpoint - New API endpoint URL
   */
  setAPIEndpointFile(endpoint) {
    if (typeof endpoint === "string" && endpoint.trim()) {
      this.apiEndpointFile = endpoint.trim();
    }
  }

  /**
   * @param {number} timeout - Timeout in milliseconds
   */
  setTimeout(timeout) {
    if (typeof timeout === "number" && timeout > 0) {
      this.requestTimeout = timeout;
    }
  }
}
