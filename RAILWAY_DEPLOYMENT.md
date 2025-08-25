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

**IMPORTANT**: All API keys should be configured in Railway Environment Variables, not in code files. This ensures security and proper environment separation.

#### Required Variables
- `PORT`: Set to `8000` (Railway will provide this automatically)
- `DEFAULT_DEPLOYMENT`: Set to `Local`

#### API Keys Configuration
Configure these in Railway's Environment Variables section (not in code):

##### LLM Providers
- `OPENAI_API_KEY`: Your OpenAI API key for GPT models
- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude models  
- `COHERE_API_KEY`: Your Cohere API key for embeddings/generation
- `GROQ_API_KEY`: Your Groq API key for fast inference

##### Embedding Services
- `VOYAGE_API_KEY`: Your VoyageAI API key for embeddings
- `UPSTAGE_API_KEY`: Your Upstage API key for document parsing

##### Data Ingestion
- `FIRECRAWL_API_KEY`: Your Firecrawl API key for web scraping
- `UNSTRUCTURED_API_KEY`: Your Unstructured API key for document parsing
- `ASSEMBLYAI_API_KEY`: Your AssemblyAI API key for audio processing

### How to Set Environment Variables in Railway
1. Go to your Railway project dashboard
2. Click on your service
3. Navigate to the "Variables" tab
4. Add each API key as a new variable
5. Deploy your changes

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
