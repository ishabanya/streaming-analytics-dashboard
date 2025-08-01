# Real-Time Streaming Platform Log ETL + Dashboard

A Python-based real-time analytics system for streaming platform logs that processes play/pause events and provides live dashboard metrics.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Log Producer   │───▶│  ETL Pipeline   │───▶│  SQLite DB      │
│  (Simulator)    │    │  (Python)       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Streamlit      │
                       │  Dashboard      │
                       └─────────────────┘
```

## Features

### Real-Time Processing
- Simulated streaming platform logs (play/pause events)
- Real-time ETL pipeline with Python
- Live dashboard updates

### Analytics Metrics
- Plays per minute
- Error rates and types
- Top streaming titles
- User engagement patterns
- Geographic distribution
- Device/platform analytics

### Dashboard Components
- Real-time metrics visualization
- Interactive charts and graphs
- Log search and filtering
- Export capabilities

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_database.py
```

### 3. Start ETL Pipeline
```bash
python etl_pipeline.py
```

### 4. Start Log Producer (in another terminal)
```bash
python log_producer.py
```

### 5. Launch Dashboard
```bash
streamlit run dashboard.py
```

## Project Structure

```
├── README.md
├── requirements.txt
├── config.py                 # Configuration settings
├── init_database.py          # Database initialization
├── log_producer.py           # Simulated log generator
├── etl_pipeline.py           # Main ETL processing
├── dashboard.py              # Streamlit dashboard
├── utils/
│   ├── __init__.py
│   ├── database.py           # Database operations
│   ├── log_parser.py         # Log parsing utilities
│   └── metrics.py            # Analytics calculations
└── data/
    └── streaming.db          # SQLite database
```

## Configuration

The system can be configured via `config.py`:
- Log generation rate
- Database settings
- ETL processing intervals
- Dashboard refresh rates

## License

MIT License 