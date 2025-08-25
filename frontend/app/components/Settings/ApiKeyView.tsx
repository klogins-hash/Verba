"use client";

import React, { useState, useEffect } from "react";
import { FaKey, FaEye, FaEyeSlash, FaSave } from "react-icons/fa";
import VerbaButton from "../Navigation/VerbaButton";
import { Credentials } from "@/app/types";

interface ApiKeyViewProps {
  credentials: Credentials;
  addStatusMessage: (
    message: string,
    type: "INFO" | "WARNING" | "SUCCESS" | "ERROR"
  ) => void;
}

interface ApiKey {
  name: string;
  key: string;
  description: string;
  required: boolean;
}

const ApiKeyView: React.FC<ApiKeyViewProps> = ({
  credentials,
  addStatusMessage,
}) => {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [showKeys, setShowKeys] = useState<{ [key: string]: boolean }>({});
  const [loading, setLoading] = useState(false);

  // Common API keys used in Verba
  const defaultApiKeys: ApiKey[] = [
    {
      name: "OPENAI_API_KEY",
      key: "",
      description: "OpenAI API key for GPT models and embeddings",
      required: false,
    },
    {
      name: "ANTHROPIC_API_KEY",
      key: "",
      description: "Anthropic API key for Claude models",
      required: false,
    },
    {
      name: "COHERE_API_KEY",
      key: "",
      description: "Cohere API key for embeddings and generation",
      required: false,
    },
    {
      name: "FIRECRAWL_API_KEY",
      key: "",
      description: "Firecrawl API key for web scraping",
      required: false,
    },
    {
      name: "GROQ_API_KEY",
      key: "",
      description: "Groq API key for fast inference",
      required: false,
    },
    {
      name: "VOYAGE_API_KEY",
      key: "",
      description: "VoyageAI API key for embeddings",
      required: false,
    },
    {
      name: "UPSTAGE_API_KEY",
      key: "",
      description: "Upstage API key for document parsing and embeddings",
      required: false,
    },
  ];

  useEffect(() => {
    loadApiKeys();
  }, []);

  const loadApiKeys = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/get_api_keys", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ credentials }),
      });

      if (response.ok) {
        const data = await response.json();
        setApiKeys(data.api_keys || defaultApiKeys);
      } else {
        // If endpoint doesn't exist, use default keys
        setApiKeys(defaultApiKeys);
      }
    } catch (error) {
      console.warn("Could not load API keys, using defaults");
      setApiKeys(defaultApiKeys);
    }
    setLoading(false);
  };

  const handleKeyChange = (name: string, value: string) => {
    setApiKeys((prev) =>
      prev.map((key) => (key.name === name ? { ...key, key: value } : key))
    );
  };

  const toggleShowKey = (name: string) => {
    setShowKeys((prev) => ({ ...prev, [name]: !prev[name] }));
  };

  const saveApiKeys = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/set_api_keys", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          credentials,
          api_keys: apiKeys,
        }),
      });

      if (response.ok) {
        addStatusMessage("API keys saved successfully", "SUCCESS");
      } else {
        addStatusMessage("Failed to save API keys", "ERROR");
      }
    } catch (error) {
      addStatusMessage("Error saving API keys", "ERROR");
    }
    setLoading(false);
  };

  const maskKey = (key: string) => {
    if (!key) return "";
    if (key.length <= 8) return "*".repeat(key.length);
    return key.substring(0, 4) + "*".repeat(key.length - 8) + key.substring(key.length - 4);
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center gap-2 mb-4">
        <FaKey className="text-primary-verba" />
        <h2 className="text-xl font-bold text-text-verba">API Key Management</h2>
      </div>

      <div className="text-text-alt-verba text-sm mb-4">
        Configure your API keys for various services. Keys are stored securely and used for authentication with external services.
      </div>

      {loading && (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-verba"></div>
        </div>
      )}

      <div className="space-y-4">
        {apiKeys.map((apiKey) => (
          <div
            key={apiKey.name}
            className="bg-bg-verba rounded-lg p-4 border border-text-alt-verba/20"
          >
            <div className="flex items-center justify-between mb-2">
              <div>
                <h3 className="font-semibold text-text-verba">{apiKey.name}</h3>
                <p className="text-sm text-text-alt-verba">{apiKey.description}</p>
              </div>
              {apiKey.required && (
                <span className="text-xs bg-warning-verba text-white px-2 py-1 rounded">
                  Required
                </span>
              )}
            </div>

            <div className="flex items-center gap-2">
              <div className="flex-1 relative">
                <input
                  type={showKeys[apiKey.name] ? "text" : "password"}
                  value={apiKey.key}
                  onChange={(e) => handleKeyChange(apiKey.name, e.target.value)}
                  placeholder={`Enter your ${apiKey.name}`}
                  className="w-full px-3 py-2 bg-bg-alt-verba border border-text-alt-verba/30 rounded-md text-text-verba placeholder-text-alt-verba focus:outline-none focus:border-primary-verba"
                />
              </div>
              <button
                onClick={() => toggleShowKey(apiKey.name)}
                className="p-2 text-text-alt-verba hover:text-primary-verba transition-colors"
                title={showKeys[apiKey.name] ? "Hide key" : "Show key"}
              >
                {showKeys[apiKey.name] ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>

            {apiKey.key && !showKeys[apiKey.name] && (
              <div className="text-xs text-text-alt-verba mt-1">
                Current: {maskKey(apiKey.key)}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="flex justify-end mt-6">
        <VerbaButton
          title="Save API Keys"
          onClick={saveApiKeys}
          disabled={loading}
          Icon={FaSave}
        />
      </div>

      <div className="text-xs text-text-alt-verba mt-4 p-3 bg-bg-alt-verba rounded-lg">
        <strong>Note:</strong> API keys are stored in your environment configuration. 
        For production deployments, consider using environment variables or secure key management systems.
      </div>
    </div>
  );
};

export default ApiKeyView;
