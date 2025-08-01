# Streamlit Cloud Deployment Guide

This guide will help you deploy your Streaming Platform ETL + Dashboard to Streamlit Cloud.

## 🚀 Quick Deployment Steps

### 1. Prepare Your Repository

Make sure your repository has the following files:
- `streamlit_app.py` (main app file)
- `requirements.txt` (dependencies)
- `.streamlit/config.toml` (configuration)

### 2. Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Fill in the details:**
   - **Repository**: `your-username/MediaStreamETL`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: `streaming-platform-analytics` (optional)
5. **Click "Deploy!"**

## 📁 Required Files

### `streamlit_app.py`
This is the main application file that Streamlit Cloud will run. It includes:
- Complete dashboard functionality
- Demo data generation for cloud deployment
- All visualizations and metrics
- Responsive design

### `requirements.txt`
Contains all necessary Python dependencies:
```
streamlit==1.28.1
pandas==2.1.3
plotly==5.17.0
numpy==1.25.2
python-dateutil==2.8.2
pytz==2023.3
```

### `.streamlit/config.toml`
Streamlit configuration file with:
- Production settings
- Custom theme
- Security configurations

## 🌐 Deployment Options

### Option 1: Direct GitHub Integration (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Streamlit Cloud deployment files"
   git push origin main
   ```

2. **Deploy via Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Deploy

### Option 2: Manual Upload

1. **Create a new app on Streamlit Cloud**
2. **Upload your files manually**
3. **Configure the deployment**

## ⚙️ Configuration

### Environment Variables

You can set environment variables in Streamlit Cloud:

1. **Go to your app settings**
2. **Navigate to "Secrets"**
3. **Add your configuration:**

```toml
[general]
# Your secrets here
DATABASE_URL = "your-database-url"
API_KEY = "your-api-key"
```

### Custom Domain (Optional)

1. **In your app settings, go to "Custom domain"**
2. **Add your domain**
3. **Update DNS records as instructed**

## 🔧 Advanced Configuration

### Performance Optimization

```toml
[server]
maxUploadSize = 200
enableXsrfProtection = false
enableCORS = false

[browser]
gatherUsageStats = false
```

### Custom Theme

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

## 📊 Features Available in Cloud Deployment

### ✅ Included Features
- **Real-time dashboard** with auto-refresh
- **Interactive charts** using Plotly
- **Key metrics cards** with live data
- **Top titles analysis** with rankings
- **Error analysis** with distribution charts
- **Geographic distribution** visualization
- **Device & platform statistics**
- **Performance metrics** with histograms
- **Recent activity logs** table

### 🎯 Demo Data
The cloud version includes realistic demo data:
- 1000+ streaming events
- Multiple content titles
- Various device types and platforms
- Geographic distribution
- Error scenarios
- Performance metrics

## 🔄 Updates and Maintenance

### Updating Your App

1. **Make changes to your code**
2. **Push to GitHub**
3. **Streamlit Cloud automatically redeploys**

### Monitoring

- **View logs** in the Streamlit Cloud dashboard
- **Check performance** metrics
- **Monitor usage** statistics

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   - Make sure all dependencies are in `requirements.txt`
   - Check for missing modules

2. **Data Loading Issues**
   - The app includes fallback demo data
   - Check your data source configuration

3. **Performance Issues**
   - Optimize your data processing
   - Use caching where appropriate

### Debug Mode

Add this to your app for debugging:
```python
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
```

## 📈 Scaling Considerations

### Free Tier Limits
- **1 app per repository**
- **Basic performance**
- **Limited resources**

### Pro Features
- **Multiple apps**
- **Better performance**
- **Custom domains**
- **Advanced analytics**

## 🔒 Security Best Practices

1. **Never commit secrets** to your repository
2. **Use environment variables** for sensitive data
3. **Validate user inputs**
4. **Implement proper authentication** if needed

## 📞 Support

### Streamlit Cloud Support
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Community Forum](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

### App-Specific Issues
- Check the troubleshooting section above
- Review the demo data generation
- Verify all dependencies are included

## 🎉 Success!

Once deployed, your app will be available at:
```
https://your-app-name.streamlit.app
```

Your Streaming Platform ETL + Dashboard is now live and accessible to anyone with the link! 