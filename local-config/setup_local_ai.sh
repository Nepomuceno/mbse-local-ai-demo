#!/bin/bash
# setup_local_ai.sh - Automated setup script for Local AI with GitHub Copilot

set -e

echo "🚀 Setting up Local AI for GitHub Copilot..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📦 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✅ Ollama is already installed"
fi

# Start Ollama if not running
if ! pgrep -f "ollama serve" > /dev/null; then
    echo "🔄 Starting Ollama..."
    ollama serve &
    sleep 5
fi

# Download recommended models
echo "📥 Downloading recommended AI models..."
echo "This may take a while depending on your internet connection..."

models_to_download=(
    "qwen2.5-coder:7b"
    "codellama:13b"
    "llama3.2:8b"
)

for model in "${models_to_download[@]}"; do
    echo "📥 Downloading $model..."
    ollama pull "$model"
done

# Check if hosts file needs modification
if ! grep -q "127.0.0.1 api.openai.com" /etc/hosts; then
    echo "🔧 Modifying hosts file..."
    echo "127.0.0.1 api.openai.com" | sudo tee -a /etc/hosts
    echo "✅ Hosts file updated"
else
    echo "✅ Hosts file already configured"
fi

# Start LiteLLM service
echo "🔄 Starting LiteLLM service..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Test the setup
echo "🧪 Testing the setup..."

# Test Ollama
echo "Testing Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not responding"
    exit 1
fi

# Test LiteLLM
echo "Testing LiteLLM..."
if curl -s http://localhost:4000/health > /dev/null; then
    echo "✅ LiteLLM is running"
else
    echo "❌ LiteLLM is not responding"
    exit 1
fi

# Test with a simple request
echo "Testing AI inference..."
response=$(curl -s -X POST http://localhost:4000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer test-key" \
    -d '{
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello, world!"}],
        "max_tokens": 50
    }')

if echo "$response" | grep -q "choices"; then
    echo "✅ AI inference is working"
else
    echo "❌ AI inference test failed"
    echo "Response: $response"
fi

echo ""
echo "🎉 Setup complete! Your local AI is now ready for GitHub Copilot."
echo ""
echo "📋 Next steps:"
echo "1. Start Caddy with: sudo caddy run --config Caddyfile"
echo "2. Open VS Code and use GitHub Copilot normally"
echo "3. Your requests will now be handled by your local AI!"
echo ""
echo "🔧 To customize your models, edit litellm_config.yaml"
echo "📚 See README.md for detailed configuration options"
echo ""
echo "💡 Tip: Monitor your setup with:"
echo "   - Ollama: curl http://localhost:11434/api/tags"
echo "   - LiteLLM: curl http://localhost:4000/health"
echo "   - Logs: docker logs litellm"
