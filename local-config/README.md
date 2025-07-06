# Local AI Setup for GitHub Copilot

This guide will help you set up a local AI environment that intercepts GitHub Copilot requests and routes them to your local models using LiteLLM and Caddy.

## Overview

GitHub Copilot doesn't natively support OpenAI-compatible APIs yet (this is being tracked in various GitHub issues). This setup creates a workaround by:

1. **Caddy**: Acts as a reverse proxy that intercepts calls to `api.openai.com`
2. **LiteLLM**: Provides OpenAI-compatible API that can route to local models (Ollama) or fallback to Azure OpenAI
3. **Ollama**: Runs local AI models on your machine
4. **Hosts file modification**: Redirects OpenAI API calls to your local setup

## Prerequisites

- Docker and Docker Compose installed
- Administrative access to modify your hosts file
- SSL certificates for `api.openai.com` (provided in this directory)

## Step-by-Step Setup

### 1. Install and Configure Ollama

#### Option A: Install Ollama directly on your system

**On Linux:**
```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Or run manually
ollama serve
```

**On macOS:**
```bash
# Download from https://ollama.com/download/mac
# Or install via Homebrew
brew install ollama

# Start Ollama
ollama serve
```

**On Windows:**
```bash
# Download from https://ollama.com/download/windows
# Follow the installer instructions
```

#### Option B: Run Ollama in Docker

**CPU Only:**
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

**With NVIDIA GPU support:**
```bash
# Install NVIDIA Container Toolkit first
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Run Ollama with GPU support
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

**With AMD GPU support:**
```bash
docker run -d --device /dev/kfd --device /dev/dri -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama:rocm
```

### 2. Download and Configure AI Models

After Ollama is running, download the models you want to use:

```bash
# Download a coding-focused model (recommended for Copilot)
ollama pull codellama:13b

# Or download a general-purpose model
ollama pull llama3.2:8b

# Or download the model specified in the config
ollama pull qwen2.5-coder:7b

# List available models
ollama list
```

### 3. Configure Your Environment

#### Update the LiteLLM configuration
Edit `litellm_config.yaml` to match your chosen model:

```yaml
model_list:
  - model_name: gpt4o-main         # Azure primary (if you have Azure OpenAI)
    litellm_params:
      model: "azure/gpt-4o"
      api_base: os.environ/AZURE_API_BASE
      api_key:  os.environ/AZURE_API_KEY
      api_version: "2025-02-15-preview"
      num_retries: 2

  - model_name: local-coding       # Local model for coding
    litellm_params:
      model: "ollama_chat/codellama:13b"  # Change this to your downloaded model
      api_base: "http://host.docker.internal:11434"  # Or http://localhost:11434 if running locally
      keep_alive: "5m"

router_settings:
  fallbacks:
    - { "gpt4o-main": ["local-coding"] }  # Falls back to local if Azure fails
```

#### Update Docker Compose (if needed)
If you don't have Azure OpenAI, you can remove the Azure environment variables from `docker-compose.yaml`:

```yaml
version: "3.9"
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-stable
    ports: [ "4000:4000" ]
    volumes:
      - ./litellm_config.yaml:/app/config.yaml:ro
    command: [ "--config", "/app/config.yaml", "--port", "4000" ]
```

### 4. Modify Your Hosts File

You need to redirect `api.openai.com` to your local machine:

**On Linux/macOS:**
```bash
sudo nano /etc/hosts
```

**On Windows:**
```cmd
# Run as Administrator
notepad C:\Windows\System32\drivers\etc\hosts
```

Add this line:
```
127.0.0.1 api.openai.com
```

### 5. Install Caddy (if not using Docker)

**On Linux:**
```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

**On macOS:**
```bash
brew install caddy
```

### 6. Start the Services

1. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

2. **Start LiteLLM**:
   ```bash
   cd /workspaces/mbse-local-ai/local-config
   docker-compose up -d
   ```

3. **Start Caddy**:
   ```bash
   cd /workspaces/mbse-local-ai/local-config
   sudo caddy run --config Caddyfile
   ```

### 7. Test Your Setup

1. **Test Ollama directly**:
   ```bash
   curl http://localhost:11434/api/generate -d '{
     "model": "codellama:13b",
     "prompt": "Write a Python hello world function",
     "stream": false
   }'
   ```

2. **Test LiteLLM**:
   ```bash
   curl http://localhost:4000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer test-key" \
     -d '{
       "model": "local-coding",
       "messages": [{"role": "user", "content": "Hello, world!"}]
     }'
   ```

3. **Test the full chain**:
   ```bash
   curl https://api.openai.com/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer test-key" \
     -d '{
       "model": "gpt-3.5-turbo",
       "messages": [{"role": "user", "content": "Hello from local AI!"}]
     }' \
     --insecure
   ```

### 8. Configure GitHub Copilot

1. **In VS Code**, ensure GitHub Copilot is installed and logged in
2. **The setup should now work automatically** - Copilot requests will be intercepted and routed to your local AI

## Configuration Details

### LiteLLM Configuration Options

The `litellm_config.yaml` file supports various model configurations:

```yaml
model_list:
  # Local Ollama models
  - model_name: coding-assistant
    litellm_params:
      model: "ollama_chat/codellama:13b"
      api_base: "http://localhost:11434"
      
  # OpenAI-compatible models
  - model_name: local-openai
    litellm_params:
      model: "openai/gpt-3.5-turbo"
      api_base: "http://localhost:8080/v1"
      api_key: "your-api-key"
      
  # Azure OpenAI
  - model_name: azure-gpt4
    litellm_params:
      model: "azure/gpt-4"
      api_base: "https://your-resource.openai.azure.com/"
      api_key: "your-azure-key"
      api_version: "2023-12-01-preview"
```

### Caddy Configuration

The `Caddyfile` configuration:
- Terminates SSL for `api.openai.com`
- Uses the provided SSL certificates
- Proxies all requests to LiteLLM on port 4000

### Model Recommendations

For GitHub Copilot usage, consider these models:

1. **Code Llama 13B** - Excellent for code completion
2. **Qwen2.5-Coder** - Good balance of speed and quality
3. **DeepSeek-Coder** - Very good at code understanding
4. **Codestral** - Mistral's coding model

## Troubleshooting

### Common Issues

1. **"Connection refused" errors**:
   - Ensure Ollama is running: `ollama serve`
   - Check if the port is accessible: `netstat -tlnp | grep 11434`

2. **SSL certificate errors**:
   - Verify the certificates are in the right location
   - Check Caddy logs: `sudo caddy logs`

3. **Model not found**:
   - Verify the model is downloaded: `ollama list`
   - Check the model name in `litellm_config.yaml`

4. **GitHub Copilot not working**:
   - Check if the hosts file modification is active: `ping api.openai.com`
   - Verify LiteLLM is responding: `curl http://localhost:4000/health`

### Checking Logs

```bash
# LiteLLM logs
docker logs litellm

# Caddy logs
sudo caddy logs

# Ollama logs
journalctl -u ollama -f
```

## Future Improvements

This setup is a workaround until GitHub Copilot officially supports OpenAI-compatible APIs. Once that feature is available, you'll be able to:

1. Remove the Caddy proxy
2. Remove the hosts file modification
3. Configure Copilot to use your local LiteLLM endpoint directly

## Security Considerations

- The SSL certificates are self-signed for `api.openai.com`
- All traffic is redirected to your local machine
- Consider the security implications of intercepting API calls
- Use this setup only in development environments

## Contributing

If you improve this setup or find issues, please update this documentation and share your changes with the team.
