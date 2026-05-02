# ML Dashboard - Angular + FastAPI

A modern, production-ready ML Dashboard that visualizes classification, regression, clustering, and time series forecasting models. Built with Angular for the frontend and FastAPI for the backend.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)

## ✨ Features

### 📊 Dashboard Pages
- **Overview**: Dataset statistics & model performance metrics
- **Classification**: Model comparison, confusion matrix, ROC curves
- **Regression**: Actual vs predicted, residuals analysis
- **Clustering**: PCA visualization, silhouette analysis, cluster summary
- **Forecasting**: Time series predictions, RMSE/MAE metrics

### 🔧 Backend (FastAPI)
- RESTful API with automatic documentation
- CORS support for frontend integration
- Model loading & caching system
- 4 main model categories with comprehensive endpoints

### 🎨 Frontend (Angular)
- Responsive modern UI with gradient themes
- Real-time data loading
- Model selection & comparison
- Mobile-friendly navigation

## 📁 Project Structure

```
ml-dashboard-angular/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py             # Configuration
│   │   ├── models_loader.py      # ML models loader
│   │   └── routes/
│   │       ├── overview.py
│   │       ├── classification.py
│   │       ├── regression.py
│   │       ├── clustering.py
│   │       └── forecasting.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── overview.component.*
│   │   │   │   ├── classification.component.*
│   │   │   │   ├── regression.component.*
│   │   │   │   ├── clustering.component.*
│   │   │   │   └── forecasting.component.*
│   │   │   ├── services/
│   │   │   │   ├── api.service.ts
│   │   │   │   └── data.service.ts
│   │   │   ├── models/
│   │   │   │   └── api.model.ts
│   │   │   ├── app.component.*
│   │   │   ├── app.module.ts
│   │   │   └── app-routing.module.ts
│   │   ├── environments/
│   │   │   ├── environment.ts
│   │   │   └── environment.prod.ts
│   │   ├── main.ts
│   │   ├── index.html
│   │   └── styles.css
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── start.sh
├── start.bat
└── README.md
```

## 🔧 Prerequisites

- **For Docker**: Docker & Docker Compose
- **For Local Development**:
  - Python 3.11+
  - Node.js 18+
  - Angular CLI 17+

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

Access the dashboard at `http://localhost:4200`

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy your models & data
# Place your .pkl files in ../ml_dashboardd-main/models/
# Place your CSV files in ../ml_dashboardd-main/data/

# Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Access the dashboard at `http://localhost:4200`

## 📡 Backend Setup

### Models Directory Structure

Place your trained models in `ml_dashboardd-main/models/`:

```
models/
├── cls_results.pkl
├── label_encoder.pkl
├── reg_results.pkl
├── cluster_df.pkl
├── kmeans.pkl
├── pca_coords.pkl
├── cluster_features.pkl
├── sil_by_k.pkl
├── feature_cols.pkl
├── cat_features.pkl
├── num_features.pkl
├── ts_results.pkl
├── ts_data.pkl
├── cluster_scaler.pkl
└── master.pkl
```

### API Endpoints

#### Overview
- `GET /api/v1/overview/health` - Health check
- `GET /api/v1/overview/stats` - Dataset statistics
- `GET /api/v1/overview/models-info` - Models information

#### Classification
- `GET /api/v1/classification/models` - List models
- `GET /api/v1/classification/confusion-matrix/{model_name}` - Confusion matrix
- `GET /api/v1/classification/roc-curve/{model_name}` - ROC curve
- `GET /api/v1/classification/classification-report/{model_name}` - Classification report

#### Regression
- `GET /api/v1/regression/models` - List models
- `GET /api/v1/regression/actual-vs-predicted/{model_name}` - Predictions
- `GET /api/v1/regression/residuals/{model_name}` - Residuals
- `GET /api/v1/regression/metrics/{model_name}` - Metrics

#### Clustering
- `GET /api/v1/clustering/pca-visualization` - PCA data
- `GET /api/v1/clustering/silhouette-analysis` - Silhouette scores
- `GET /api/v1/clustering/clusters-summary` - Cluster summary

#### Forecasting
- `GET /api/v1/forecasting/models` - List models
- `GET /api/v1/forecasting/forecast/{model_name}` - Forecast data
- `GET /api/v1/forecasting/time-series-data` - Time series data

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Individual Docker Images

```bash
# Build backend
docker build -f Dockerfile.backend -t ml-dashboard-backend .

# Build frontend
docker build -f Dockerfile.frontend -t ml-dashboard-frontend .

# Run backend
docker run -p 8000:8000 -v $(pwd)/ml_dashboardd-main/models:/app/models ml-dashboard-backend

# Run frontend
docker run -p 4200:4200 ml-dashboard-frontend
```

## 📚 API Documentation

### Interactive API Docs
Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 CORS Configuration

The backend allows requests from:
- `http://localhost:4200`
- `http://localhost:3000`
- `http://127.0.0.1:4200`
- `http://127.0.0.1:3000`

To add more origins, edit `backend/app/config.py`:

```python
ALLOWED_ORIGINS = [
    "http://your-domain.com",
    "https://your-domain.com",
]
```

## 📝 Environment Configuration

### Frontend (environment.ts)

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1'
};
```

For production, update `environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.your-domain.com/api/v1'
};
```

## 🚀 Production Deployment

### Using Nginx

Create `nginx.conf`:

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:4200;
}

server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://backend/api/;
    }

    location / {
        proxy_pass http://frontend/;
    }
}
```

Then use the commented nginx service in `docker-compose.yml`.

### Environment Variables

Create a `.env` file:

```
API_URL=https://api.your-domain.com/api/v1
DEBUG=false
WORKERS=4
```

## ❓ Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is available
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Check if models are loaded
curl http://localhost:8000/api/v1/overview/health
```

### Frontend shows blank page
- Check browser console for errors
- Verify API URL in environment files
- Check CORS headers in backend response

### Models not loading
- Ensure .pkl files are in correct directory
- Check file permissions
- Verify model paths in config.py

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Angular Documentation](https://angular.io/docs)
- [Docker Documentation](https://docs.docker.com/)

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Support

For issues and questions, please check:
1. API documentation at `/docs`
2. Browser console errors
3. Backend logs: `docker-compose logs backend`

---

**Happy analyzing! 📊**
