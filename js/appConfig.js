/**
 * Application configuration
 */
export const APP_CONFIG = {
  // API Configuration
  apiEndpoint: "http://localhost:5000/api/classify",
  requestTimeout: 30000, // 30 seconds

  // UI Element Selectors
  uiElements: {
    emailText: "#emailText",
    processBtn: "#processBtn",
    loading: "#loading",
    results: "#results",
    categoryBadge: "#categoryBadge",
    confidence: "#confidence",
    suggestedResponse: "#suggestedResponse",
    wordCount: "#wordCount",
    processingTime: "#processingTime",
    accuracyScore: "#accuracyScore",
    fileInfo: "#fileInfo",
    clearBtn: "#clearBtn",
    emptyResult: "#emptyResult",
  },

  // File Handler Element Selectors
  fileElements: {
    uploadArea: "#uploadArea",
    fileInput: "#fileInput",
    fileInfo: "#fileInfo",
    fileName: "#fileName",
    emailText: "#emailText",
  },

  // Toast Notification Selector
  toastSelector: "#toast",
};
