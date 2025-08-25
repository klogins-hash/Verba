# Railway Deployment Guide for Verba

This guide explains how to deploy Verba on Railway with optimized configurations.

## Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/verba)

## Manual Deployment

### 1. Prerequisites

- Railway account
- GitHub repository with this Verba code
- API keys for your chosen LLM providers

### 2. Railway Configuration Files

This repository includes Railway-optimized files:

- `railway.json` - Railway service configuration
- `Dockerfile.railway` - Railway-specific Dockerfile
- `nixpacks.toml` - Alternative Nixpacks configuration
- `.env.railway` - Environment variables template

### 3. Environment Variables

Set these in your Railway project dashboard:

#### Required
```
PORT=8000
DEFAULT_DEPLOYMENT=Local
```

#### LLM Providers (choose one or more)
```
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
COHERE_API_KEY=your-cohere-api-key
GROQ_API_KEY=your-groq-api-key
```

#### Optional Services
```
WEAVIATE_URL_VERBA=your-weaviate-url
WEAVIATE_API_KEY_VERBA=your-weaviate-api-key
UNSTRUCTURED_API_KEY=your-unstructured-api-key
ASSEMBLYAI_API_KEY=your-assemblyai-api-key
```

### 4. Deployment Steps

1. **Fork this repository** to your GitHub account
2. **Connect to Railway**:
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository
3. **Configure Environment Variables**:
   - Go to your project settings
   - Add the environment variables from the template above
4. **Deploy**:
   - Railway will automatically build and deploy using the Dockerfile
   - The service will be available at your Railway-provided URL

### 5. Custom Domain (Optional)

1. Go to your Railway project settings
2. Click "Domains" 
3. Add your custom domain
4. Update DNS records as instructed

## Architecture

### Railway Optimizations

- **Multi-stage Docker build** for smaller image size
- **Health checks** for better reliability  
- **Environment variable support** for Railway's dynamic PORT
- **Persistent data storage** using Railway volumes
- **Resource optimization** for Railway's infrastructure

### Deployment Options

1. **Dockerfile** (recommended) - Uses optimized Docker build
2. **Nixpacks** - Alternative build system, faster for simple deployments

## Troubleshooting

### Common Issues

1. **Port binding errors**: Ensure you're using `${PORT}` environment variable
2. **Memory issues**: Upgrade Railway plan if needed
3. **Build timeouts**: Use multi-stage Docker build (already configured)
4. **API key errors**: Verify environment variables are set correctly

### Logs and Monitoring

- View logs in Railway dashboard
- Monitor resource usage in the metrics tab
- Set up alerts for service health

### Performance Tips

1. **Use Railway Pro** for better performance and resources
2. **Enable persistent storage** for document uploads
3. **Configure proper health checks** (already included)
4. **Use CDN** for static assets if needed

## Cost Optimization

- Railway charges based on usage
- Use sleep mode for development environments
- Monitor resource consumption in dashboard
- Consider using external Weaviate instance for production

## Support

- Railway Documentation: https://docs.railway.app/
- Verba Issues: https://github.com/weaviate/Verba/issues
- Railway Community: https://railway.app/discord
