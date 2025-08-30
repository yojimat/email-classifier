import ComponentLoader from "./modules/ComponentLoader.js";

// Create global instance
const componentLoader = new ComponentLoader();

// Register all components
componentLoader.register("header", "components/header.html");
componentLoader.register("email-input", "components/email-input.html");
componentLoader.register("ai-analysis", "components/ai-analysis.html");
componentLoader.register("toast", "components/toast.html");

/**
 * Initialize all components when DOM is ready
 */
async function initializeComponents() {
  const componentConfigs = [
    { name: "header", target: "#header-container" },
    { name: "email-input", target: "#email-input-container" },
    { name: "ai-analysis", target: "#ai-analysis-container" },
    { name: "toast", target: "#toast-container" },
  ];

  const success = await componentLoader.loadMultiple(componentConfigs);

  if (success) {
    console.log("🎉 All components loaded successfully!");
  } else {
    console.error("❌ Some components failed to load");
  }
}

export { initializeComponents };
