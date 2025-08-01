# 📊 Streaming Platform Analytics Dashboard

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**Real-time analytics dashboard for streaming platforms with interactive visualizations and live data insights**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-blue?style=for-the-badge&logo=streamlit)](https://streaming-analytics-dashboard.streamlit.app/)
[![GitHub Stars](https://img.shields.io/github/stars/ishabanya/streaming-analytics-dashboard?style=for-the-badge&logo=github)](https://github.com/ishabanya/streaming-analytics-dashboard/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ishabanya/streaming-analytics-dashboard?style=for-the-badge&logo=github)](https://github.com/ishabanya/streaming-analytics-dashboard/network/members)

</div>

---

## 🚀 Live Demo

**Experience the dashboard in action:** [https://streaming-analytics-dashboard.streamlit.app/](https://streaming-analytics-dashboard.streamlit.app/)

<div align="center">
  <img src="https://via.placeholder.com/800x400/1f77b4/ffffff?text=Streaming+Analytics+Dashboard" alt="Dashboard Preview" width="800"/>
</div>

---

## 🎯 Project Overview

A comprehensive real-time analytics dashboard designed for streaming platforms, providing deep insights into user behavior, content performance, and system health. Built with modern web technologies and optimized for cloud deployment.

### ✨ Key Features

- 📈 **Real-time Analytics** - Live data visualization with auto-refresh
- 🏆 **Content Performance** - Top titles analysis and rankings
- 🌍 **Geographic Insights** - Global user distribution analytics
- 📱 **Device Analytics** - Cross-platform performance metrics
- ⚡ **Performance Monitoring** - Response time and error tracking
- 🎨 **Interactive Visualizations** - Beautiful charts with Plotly
- 📊 **Comprehensive Metrics** - 6 detailed analytics sections

---

## 🛠️ Technology Stack

<div align="center">

| Technology | Purpose | Version |
|------------|---------|---------|
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) | Web Framework | >=1.28.0 |
| ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) | Data Processing | >=2.0.0 |
| ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white) | Data Visualization | >=5.15.0 |
| ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) | Numerical Computing | >=1.24.0 |

</div>

---

## 📊 Dashboard Sections

### 🎯 Key Metrics Dashboard
<div align="center">
  <img src="https://via.placeholder.com/400x200/4CAF50/ffffff?text=Key+Metrics" alt="Key Metrics" width="400"/>
</div>

- **Plays per Minute** - Real-time streaming activity tracking
- **Error Rate** - System health monitoring with percentage breakdown
- **Active Users** - Current user engagement metrics
- **Avg Response Time** - Performance monitoring in milliseconds

### 📈 Plays Over Time
- Interactive line charts showing temporal patterns
- Configurable time ranges (5 min to 6 hours)
- Real-time data updates with auto-refresh

### 🏆 Top Streaming Titles
- Horizontal bar charts of most popular content
- Play count and percentage breakdowns
- Detailed rankings table with metrics

### ⚠️ Error Analysis
- Error type distribution (pie charts)
- Error trends over time (line charts)
- Detailed error categorization and monitoring

### 🌍 Geographic Distribution
- User distribution by country
- Regional performance insights
- Global analytics visualization

### 📱 Device & Platform Statistics
- Device type distribution (mobile, desktop, tablet, smart TV)
- Platform usage statistics (web, iOS, Android, Roku)
- Cross-platform performance comparison

### 📋 Recent Activity Feed
- Live activity monitoring
- Recent streaming events log
- User interaction tracking

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ishabanya/streaming-analytics-dashboard.git
   cd streaming-analytics-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the dashboard**
   - Open your browser and navigate to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork this repository** to your GitHub account

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Configure:
     - **Repository**: `your-username/streaming-analytics-dashboard`
     - **Branch**: `main`
     - **Main file path**: `streamlit_app.py`
   - Click "Deploy!"

3. **Your app will be live at**
   ```
   https://your-app-name.streamlit.app
   ```

---

## 🎲 Demo Data Features

The dashboard includes realistic demo data featuring:

- **1000+ streaming events** with realistic distribution patterns
- **Popular content titles** (The Matrix, Breaking Bad, Game of Thrones, etc.)
- **Multiple device types** (mobile, desktop, tablet, smart TV, gaming console)
- **Global platforms** (web, iOS, Android, Roku, Fire TV, Apple TV)
- **Geographic diversity** (US, UK, CA, AU, DE, FR, JP, BR, IN, MX)
- **Realistic error scenarios** (network, playback, authentication errors)
- **Performance metrics** (response times, buffer underruns)

---

## ⚙️ Configuration Options

### Time Range Selection
- Last 5 minutes
- Last 15 minutes
- Last 30 minutes
- Last 1 hour
- Last 6 hours

### Auto-Refresh Settings
- Configurable refresh intervals (5-60 seconds)
- Real-time data updates
- Automatic dashboard refresh

### Customization
- **Theme configuration** in `.streamlit/config.toml`
- **Custom CSS** for professional styling
- **Responsive design** for all devices

---

## 🔧 Customization Guide

### Adding Real Data Sources

To connect your own data sources:

1. **Modify the `DemoDataGenerator` class** in `streamlit_app.py`
2. **Replace demo data generation** with your database/API calls
3. **Update the `get_recent_data()` function** to fetch from your data source

### Example: Connecting to a Database
```python
def get_recent_data(minutes: int = 30):
    # Replace demo data with real database query
    query = f"""
    SELECT * FROM streaming_events 
    WHERE timestamp >= NOW() - INTERVAL '{minutes} minutes'
    """
    return pd.read_sql(query, your_database_connection)
```

### Styling Customization
- **Custom CSS** in the app for professional styling
- **Theme configuration** in `.streamlit/config.toml`
- **Responsive design** for all devices

---

## 📈 Performance Features

- **⚡ Caching** - Efficient data processing with Streamlit caching
- **🚀 Optimized Charts** - Fast rendering with Plotly
- **📱 Responsive Design** - Works on desktop, tablet, and mobile
- **🔄 Real-time Updates** - Live data refresh capabilities
- **🎯 Memory Efficient** - Optimized for cloud deployment

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes locally before submitting
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">

**Made with ❤️ for the streaming analytics community**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ishabanya/streaming-analytics-dashboard)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streaming-analytics-dashboard.streamlit.app/)

</div>

---

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **Plotly** for interactive visualizations
- **Pandas** for powerful data processing
- **GitHub** for hosting and version control
- **Streamlit Cloud** for seamless deployment

---

## 📞 Support & Community

- **🐛 Issues**: [GitHub Issues](https://github.com/ishabanya/streaming-analytics-dashboard/issues)
- **📚 Documentation**: [Streamlit Docs](https://docs.streamlit.io/)
- **💬 Community**: [Streamlit Community](https://discuss.streamlit.io/)
- **📧 Contact**: Open an issue or discussion on GitHub

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

[![GitHub Stars](https://img.shields.io/github/stars/ishabanya/streaming-analytics-dashboard?style=social)](https://github.com/ishabanya/streaming-analytics-dashboard/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ishabanya/streaming-analytics-dashboard?style=social)](https://github.com/ishabanya/streaming-analytics-dashboard/network/members)

</div> 