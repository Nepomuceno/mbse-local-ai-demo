# LiteLLM Configuration Examples

This directory contains example configurations for different local AI setups.

## Available Configurations

### 1. `litellm_config.yaml` - Current Configuration
The main configuration file with Azure OpenAI primary and local Ollama fallback.

### 2. `litellm_config_local_only.yaml` - Local Only
Configuration using only local Ollama models without external API dependencies.

### 3. `litellm_config_coding_focused.yaml` - Coding Optimized
Configuration optimized for coding tasks with multiple coding-focused models.

## Model Recommendations

### For GitHub Copilot / Code Completion
- **CodeLlama 13B**: `ollama pull codellama:13b`
- **Qwen2.5-Coder 7B**: `ollama pull qwen2.5-coder:7b`
- **DeepSeek-Coder**: `ollama pull deepseek-coder:6.7b`

### For General Purpose
- **Llama 3.2 8B**: `ollama pull llama3.2:8b`
- **Qwen2.5 14B**: `ollama pull qwen2.5:14b`
- **Mistral 7B**: `ollama pull mistral:7b`

## Usage

1. Choose the configuration that best fits your needs
2. Copy it to `litellm_config.yaml`
3. Adjust model names to match your downloaded models
4. Restart the LiteLLM service: `docker-compose restart litellm`
