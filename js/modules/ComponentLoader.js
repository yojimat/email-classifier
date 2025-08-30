/**
 * ===================================
 * COMPONENT LOADER MODULE
 * ===================================
 * Handles dynamic loading of HTML components
 */

export default class ComponentLoader {
  constructor() {
    this.components = new Map();
    this.loadedComponents = new Set();
  }

  /**
   * Register a component with its path
   * @param {string} name - Component name
   * @param {string} path - Path to component HTML file
   */
  register(name, path) {
    this.components.set(name, path);
  }

  /**
   * Load a component and inject it into a target element
   * @param {string} componentName - Name of the component to load
   * @param {string} targetSelector - CSS selector for target element
   * @returns {Promise<boolean>} - Success status
   */
  async load(componentName, targetSelector) {
    try {
      const path = this.components.get(componentName);
      if (!path) {
        throw new Error(`Component '${componentName}' not registered`);
      }

      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`Failed to load component: ${response.status}`);
      }

      const html = await response.text();
      const targetElement = document.querySelector(targetSelector);

      if (!targetElement) {
        throw new Error(`Target element '${targetSelector}' not found`);
      }

      targetElement.innerHTML = html;
      this.loadedComponents.add(componentName);

      console.log(`✅ Component '${componentName}' loaded successfully`);
      return true;
    } catch (error) {
      console.error(`❌ Error loading component '${componentName}':`, error);
      return false;
    }
  }

  /**
   * Load multiple components
   * @param {Array} componentConfigs - Array of {name, target} objects
   * @returns {Promise<boolean>} - Success status for all components
   */
  async loadMultiple(componentConfigs) {
    const promises = componentConfigs.map((config) =>
      this.load(config.name, config.target)
    );

    const results = await Promise.all(promises);
    return results.every((result) => result === true);
  }
}
