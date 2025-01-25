# Crude Oil Price Tracker

A Python script that automatically extracts daily Brent crude oil prices and stores them in CSV format. Includes automated scheduling for regular updates.

## Features

- 🕒 Automated extraction every 10 days
- 📆 Duplicate prevention for historical data
- 🔐 Secure API key management using `.env` file
- 📈 CSV storage with timestamps
- 📧 Error handling and status notifications
- ⚙️ Configurable scheduling interval

## Prerequisites

- Python 3.6+
- Alpha Vantage API key (free tier available)
- requests library

## Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/oil-price-tracker.git
cd oil-price-tracker
```
