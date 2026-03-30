/// <reference types="vite/client" />

interface Window {
  AgentAPI?: {
    getOllamaResponse: (message: string) => Promise<string>;
  };
}

declare module "*.css";
