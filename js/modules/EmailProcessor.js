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

      // const result = await this.callClassificationAPI(content);
      // result.processingTime = this.calculateProcessingTime(startTime);

      const mockResult = this.generateMockData(content);
      mockResult.processingTime = this.calculateProcessingTime(startTime);

      return mockResult;
    } catch (error) {
      console.error("Error processing email:", error);
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
          timestamp: new Date().toISOString(),
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
   * Generate mock data for demonstration purposes
   * @param {string} content - Email content
   * @returns {Object} - Mock classification data
   */
  generateMockData(content) {
    const wordCount = this.countWords(content);
    const isProductive = this.determineMockProductivity(content, wordCount);

    return {
      category: isProductive ? "productive" : "unproductive",
      confidence: this.generateMockConfidence(),
      response: this.generateMockResponse(content, isProductive),
      word_count: wordCount,
      metadata: {
        source: "mock",
        analysis_date: new Date().toISOString(),
      },
    };
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
   * Determine mock productivity based on content analysis
   * @param {string} content - Email content
   * @param {number} wordCount - Word count
   * @returns {boolean} - Whether email is considered productive
   */
  determineMockProductivity(content, wordCount) {
    const productiveKeywords = [
      "projeto",
      "reunião",
      "prazo",
      "entrega",
      "desenvolvimento",
      "análise",
      "proposta",
      "orçamento",
      "contrato",
      "acordo",
    ];

    const unproductiveKeywords = [
      "spam",
      "promoção",
      "desconto",
      "oferta",
      "grátis",
      "clique aqui",
      "urgente",
      "limitado",
    ];

    const lowerContent = content.toLowerCase();

    const productiveScore = productiveKeywords.reduce((score, keyword) => {
      return score + (lowerContent.includes(keyword) ? 1 : 0);
    }, 0);

    const unproductiveScore = unproductiveKeywords.reduce((score, keyword) => {
      return score + (lowerContent.includes(keyword) ? 1 : 0);
    }, 0);

    // Consider length and keyword analysis
    const lengthFactor = wordCount > 50 ? 1 : 0;

    return productiveScore + lengthFactor > unproductiveScore;
  }

  /**
   * Generate mock confidence score
   * @returns {number} - Confidence percentage
   */
  generateMockConfidence() {
    return Math.floor(Math.random() * 20) + 80; // 80-99%
  }

  /**
   * Generate mock response based on content analysis
   * @param {string} content - Email content
   * @param {boolean} isProductive - Whether email is productive
   * @returns {string} - Generated response
   */
  generateMockResponse(content, isProductive) {
    if (isProductive) {
      return `Prezado(a),<br><br>
              Agradeço pelo seu email. Analisei atentamente os pontos apresentados e 
              gostaria de contribuir com algumas considerações.<br><br>
              [Pontos específicos baseados no conteúdo]<br><br>
              Fico à disposição para discutirmos este assunto em maior detalhe.<br><br>
              Atenciosamente`;
    } else {
      return `Olá,<br><br>
              Obrigado pelo contato. Recebi sua mensagem e entrarei em contato 
              assim que possível para darmos continuidade.<br><br>
              Atenciosamente`;
    }
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
   * @param {number} timeout - Timeout in milliseconds
   */
  setTimeout(timeout) {
    if (typeof timeout === "number" && timeout > 0) {
      this.requestTimeout = timeout;
    }
  }
}
