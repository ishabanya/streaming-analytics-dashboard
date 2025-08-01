# 📊 Streaming Platform Analytics Dashboard

A comprehensive real-time analytics dashboard for streaming platforms, built with Streamlit and deployable on Streamlit Cloud.

## 🚀 Live Demo

**Deployed on Streamlit Cloud:** [View Live Dashboard](https://streaming-analytics-dashboard.streamlit.app)

## 🎯 Features

### 📈 Real-Time Analytics
- **Plays per minute** tracking
- **Error rate monitoring** with detailed breakdowns
- **User engagement** metrics
- **Performance analytics** with response time analysis

### 🏆 Content Analytics
- **Top streaming titles** with play counts and percentages
- **Content performance** rankings
- **Viewership patterns** analysis

### 🌍 Geographic Insights
- **User distribution** by country
- **Regional performance** metrics
- **Global analytics** visualization

### 📱 Device & Platform Analytics
- **Device type distribution** (mobile, desktop, tablet, smart TV)
- **Platform usage** statistics (web, iOS, Android, Roku)
- **Cross-platform** performance comparison

### ⚡ Performance Monitoring
- **Response time** distribution and analysis
- **Buffer underrun** tracking
- **System performance** metrics

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Cloud

## 🚀 Quick Start

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
   - Open your browser and go to `http://localhost:8501`

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

## 📊 Dashboard Sections

### 🎯 Key Metrics
- **Plays per Minute**: Real-time streaming activity
- **Error Rate**: System health monitoring
- **Active Users**: Current user engagement
- **Avg Response Time**: Performance metrics

### 📈 Plays Over Time
- Interactive line chart showing plays per minute
- Real-time data updates
- Time range selection

### 🏆 Top Titles
- Horizontal bar chart of most popular content
- Play count and percentage breakdown
- Detailed rankings table

### ⚠️ Error Analysis
- Error type distribution (pie chart)
- Error trends over time (line chart)
- Detailed error categorization

### 🌍 Geographic Distribution
- User distribution by country
- Regional performance insights
- Global analytics visualization

### 📱 Device & Platform Stats
- Device type distribution (pie chart)
- Platform usage statistics (pie chart)
- Cross-platform comparison

### 📋 Recent Activity
- Live activity feed
- Recent streaming events
- User interaction logs

## ⚙️ Configuration

### Time Range Selection
- Last 5 minutes
- Last 15 minutes
- Last 30 minutes
- Last 1 hour
- Last 6 hours

### Auto-Refresh
- Configurable refresh intervals (5-60 seconds)
- Real-time data updates
- Automatic dashboard refresh

## 🎲 Demo Data

The dashboard includes realistic demo data featuring:
- **1000+ streaming events** with realistic distribution
- **Popular content titles** (The Matrix, Breaking Bad, etc.)
- **Multiple device types** and platforms
- **Global geographic distribution**
- **Realistic error scenarios**
- **Performance metrics**

## 🔧 Customization

### Adding Real Data
To connect real data sources:

1. **Modify the `DemoDataGenerator` class** in `streamlit_app.py`
2. **Replace demo data generation** with your data source
3. **Update the `get_recent_data()` function** to fetch from your database/API

### Styling
- **Custom CSS** in the app for professional styling
- **Theme configuration** in `.streamlit/config.toml`
- **Responsive design** for all devices

## 📈 Performance Features

- **Caching**: Efficient data processing with Streamlit caching
- **Optimized charts**: Fast rendering with Plotly
- **Responsive design**: Works on desktop, tablet, and mobile
- **Real-time updates**: Live data refresh capabilities

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the amazing framework
- **Plotly** for interactive visualizations
- **Pandas** for data processing
- **GitHub** for hosting and version control

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ishabanya/streaming-analytics-dashboard/issues)
- **Documentation**: [Streamlit Docs](https://docs.streamlit.io/)
- **Community**: [Streamlit Community](https://discuss.streamlit.io/)

---

**Made with ❤️ for the streaming analytics community** 