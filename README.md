# Cardiovascular Disease Prediction - ML Web Application

An end-to-end Machine Learning web application designed to predict cardiovascular disease risk based on patient health metrics.

## 🚀 Features

- **Machine Learning Model**: Trained model (`cardio_model.pkl`) with feature scaling (`scaler.pkl`).
- **RESTful API**: Flask backend providing prediction endpoints and health metrics evaluation.
- **Modern Frontend**: Responsive web interface with interactive checkup form, analytics, and information pages.
- **Concurrent Development**: Run both backend and frontend concurrently with a single npm command.

## 📁 Project Structure

```
.
├── backend/
│   ├── app.py              # Flask REST API
│   ├── train_model.py      # Model training script
│   ├── test_api.py         # API testing script
│   ├── cardio_model.pkl    # Trained ML model
│   ├── scaler.pkl          # Feature scaler
│   ├── cardio_train.csv    # Dataset
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Landing page
│   ├── checkup.html        # Health checkup form
│   ├── about.html          # About & info page
│   ├── script.js           # Frontend logic & API integration
│   └── styles.css          # Styling
├── package.json            # NPM scripts & dev dependencies
└── README.md
```

## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm

### Backend Setup

1. Navigate to the backend directory or install from root:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Run the Flask server:
   ```bash
   python backend/app.py
   ```

### Frontend Setup

1. Install npm dependencies:
   ```bash
   npm install
   ```

2. Start the development server (runs both backend and frontend):
   ```bash
   npm run dev
   ```
