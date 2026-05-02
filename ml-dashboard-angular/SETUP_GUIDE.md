# ML Dashboard - Setup & Deployment Guide

## 📋 Step-by-Step Setup
cd "C:\Users\brahm\OneDrive\Desktop\esprit\pi kachefa\dep ML\ml-dashboard-angular" ; docker-compose up -d

cd "C:\Users\brahm\OneDrive\Desktop\esprit\pi kachefa\dep ML\ml-dashboard-angular" ; docker-compose ps

### Step 1: Prepare Your Models

**Option A: Using Automated Training Pipeline (Recommended)**

```bash
# Navigate to project root
cd ml-dashboard-angular

# Run the complete setup and training
python setup.py

# This will:
# 1. Create necessary directories (models, data, mlruns)
# 2. Generate synthetic training data
# 3. Train all model types with MLflow tracking
# 4. Save versioned models
# 5. Display MLflow tracking information
```

**Option B: Manual Model Training**

```bash
cd backend
python train.py
```

Verify your models folder contains all required files:
```
backend/models/
├── cls_results.pkl
├── reg_results.pkl
├── cluster_results.pkl
├── ts_results.pkl
├── kmeans.pkl
├── pca.pkl
├── classifier_scaler.pkl
├── regression_scaler.pkl
├── cluster_scaler.pkl
└── ts_scaler.pkl
```

### Step 2: Quick Deployment with Docker

#### On Windows:
```bash
# Simply run the batch file
start.bat
```

#### On Linux/Mac:
```bash
# Make script executable
chmod +x start.sh

# Run the script
./start.sh
```

### Step 3: Access the Dashboard

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MLflow Tracking**: http://localhost:5000

### Step 3a: Access New Features (Week 3)

- **Prediction Interface**: http://localhost:4200/prediction
- **MLflow Experiments**: http://localhost:5000 (see all training runs)

### Step 4: Navigate the Dashboard

1. **Overview Tab**: See dataset statistics and model metrics
2. **Classification Tab**: View classifiers, confusion matrices, ROC curves
3. **Regression Tab**: Check actual vs predicted values and residuals
4. **Clustering Tab**: Analyze cluster silhouette scores and PCA visualization
5. **Forecasting Tab**: Review time series predictions
6. **🔮 Predict Tab**: Make real-time predictions with any trained model

## 🔧 Manual Setup (Without Docker)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Frontend will open at http://localhost:4200
```

## 🐳 Using Docker Compose

### Build & Run

```bash
# Build all services (including MLflow)
docker-compose build

# Start all services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access Services

- Frontend: http://localhost:4200
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MLflow Tracking UI: http://localhost:5000 (NEW!)

### Available Services

- **ml-dashboard-backend**: FastAPI backend with prediction API
- **ml-dashboard-frontend**: Angular frontend
- **ml-dashboard-mlflow**: MLflow tracking server

## 📊 MLflow Experiment Tracking (NEW!)

### What is MLflow?

MLflow is an open-source platform for managing ML workflows:
- Track experiments and runs
- Log parameters and metrics
- Store model artifacts
- Compare model performance

### Accessing MLflow

1. Navigate to http://localhost:5000
2. Select "ML_Dashboard_Training" experiment
3. View different training runs
4. Compare metrics across runs
5. Download artifacts

### Training Runs

Each time you run `python setup.py`, a new MLflow run is created with:
- **Classification Metrics**: Accuracy, Precision, Recall, F1, AUC
- **Regression Metrics**: MSE, RMSE, MAE, R²
- **Clustering Metrics**: Silhouette scores for different k values
- **Forecasting Metrics**: RMSE, MAE, R²

### Viewing Experiments

```bash
# Via MLflow UI (automatic with Docker)
mlflow ui  # Opens at http://localhost:5000

# Or access during training
python setup.py
```

## 📊 API Endpoints

All endpoints return JSON responses. Here are some key endpoints:

### Health Check
```
GET /api/v1/overview/health
```

### Get Dataset Stats
```
GET /api/v1/overview/stats
```

### 🆕 Prediction Endpoints

#### Make Single Prediction
```
POST /api/v1/prediction/predict
Body:
{
  "model_name": "RandomForest_v1",
  "model_type": "classification",
  "features": {
    "feature_1": 0.5,
    "feature_2": -0.2,
    "feature_3": 1.0,
    "feature_4": 50.0,
    "feature_5": 1
  }
}
```

#### Batch Predictions
```
POST /api/v1/prediction/batch-predict
Body: [
  { "model_name": "...", "model_type": "...", "features": {...} },
  ...
]
```

#### List Available Models
```
GET /api/v1/prediction/predict/available-models
Response:
{
  "classification": ["RandomForest_v1", "RandomForest_v2"],
  "regression": ["LinearRegression", "RandomForest_v1", "RandomForest_v2"],
  "clustering": ["KMeans_v1"],
  "forecasting": ["ARIMA_v1", "RandomForest_v1"]
}
```

### Classification Models
```
GET /api/v1/classification/models
GET /api/v1/classification/confusion-matrix/{model_name}
GET /api/v1/classification/classification-report/{model_name}
```

### Regression Models
```
GET /api/v1/regression/models
GET /api/v1/regression/actual-vs-predicted/{model_name}
GET /api/v1/regression/residuals/{model_name}
```

### Clustering
```
GET /api/v1/clustering/pca-visualization
GET /api/v1/clustering/silhouette-analysis
GET /api/v1/clustering/clusters-summary
```

### Forecasting
```
GET /api/v1/forecasting/models
GET /api/v1/forecasting/forecast/{model_name}
GET /api/v1/forecasting/time-series-data
```

## 🔄 Updating API URL

### For Development

Edit `frontend/src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1'
};
```

### For Production

Edit `frontend/src/environments/environment.prod.ts`:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-api-domain.com/api/v1'
};
```

## 🚀 Production Deployment

### Building for Production

```bash
cd frontend
npm run build
```

This creates an optimized build in `frontend/dist/ml-dashboard`

### Deploying with Docker

```bash
# Build production Docker images
docker-compose build --no-cache

# Run with production settings
docker-compose up -d

# Scale services if needed
docker-compose up -d --scale backend=3
```

## 🛠️ Troubleshooting

### Models not training?
```bash
# Run setup with verbose output
python setup.py

# Or run training script directly
cd backend
python train.py
```

### MLflow not tracking?
```bash
# Check configuration
python setup.py --config

# View MLflow UI
mlflow ui
# Open http://localhost:5000
```

### Prediction endpoint returns 404?
```bash
# Verify models are loaded
curl http://localhost:8000/api/v1/prediction/predict/available-models

# Check if training was completed
ls -la backend/models/
```

### Models not loading?
```bash
# Check backend logs
docker-compose logs backend

# Verify models directory
ls -la backend/models/

# Regenerate models
python setup.py
```

### Frontend shows error?
```bash
# Check frontend logs
docker-compose logs frontend

# Check browser console (F12)
# Verify API URL is correct at frontend/src/environments/environment.ts
```

### Port already in use?
```bash
# Find and kill process (Linux/Mac)
lsof -i :8000  # Find backend
lsof -i :4200  # Find frontend
lsof -i :5000  # Find MLflow

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change ports in docker-compose.yml
```

## 📝 Customization

### Adding Custom Endpoints

1. Create new route file in `backend/app/routes/`
2. Add router to main.py:
```python
from app.routes import your_new_route
app.include_router(your_new_route.router, prefix=API_V1_STR)
```

### Styling the Dashboard

Edit component CSS files:
- `frontend/src/app/components/*.component.css`
- `frontend/src/styles.css` for global styles

### Changing Colors

Update gradient colors in component CSS files:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 📚 Resources & Documentation

### New Documentation Files
- **[TRAINING.md](TRAINING.md)** - Complete guide to the training pipeline and MLflow
- **[.env.example](.env.example)** - Environment variables template

### Official Documentation
- [MLflow Documentation](https://mlflow.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/docs)
- [Angular Guide](https://angular.io/guide/setup-local)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [scikit-learn Documentation](https://scikit-learn.org/)

### Quick References
- API Documentation (auto-generated): http://localhost:8000/docs
- MLflow Tracking: http://localhost:5000
- GitHub Repository: [Your repo URL]

## ✅ Deployment Checklist

- [ ] Models are trained and saved
- [ ] All .pkl files are in models/ directory
- [ ] Docker & Docker Compose are installed
- [ ] Environment configuration is correct
- [ ] Ports 4200 and 8000 are available
- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] Can navigate between dashboard tabs
- [ ] API endpoints return data

## ✨ Weekly Requirements & Validation Criteria

### 1. Experiment Tracking (MLflow)
- [ ] Training runs are tracked (parameters, metrics, artifacts)
- [ ] At least two runs are visible and comparable

### 2. Automated Training Pipeline
- [ ] End-to-end pipeline (preprocessing → training → evaluation → saving)
- [ ] Reproducible without manual intervention

### 3. Model Management
- [ ] Models are saved and versioned
- [ ] Previous versions remain accessible

### 4. Model Serving (API)
- [ ] A functional API is implemented (e.g., FastAPI)
- [ ] A prediction endpoint (`/predict`) is operational
- [ ] Test successful: input data → prediction returned

### 5. Containerization
- [ ] Application runs using Docker
- [ ] (Optional but recommended) use of Docker Compose

### 6. Code Quality
- [ ] Code is clean, structured, and runs without major errors
- [ ] (Optional) automated tests

### 7. Web App Integration
- [ ] Your Web Application calls the prediction API
- [ ] Full pipeline works end-to-end:
  - User Interface → API → Model → Displayed Result
  - *Note: This part was not fully covered in the workshop but remains simple to implement (HTTP request)*

### Expected Deliverables
- ✓ Functional API (local or Dockerized)
- ✓ MLflow with visible runs
- ✓ Automated pipeline
- ✓ Model accessible via API
- ✓ Web App connected to the API

## 🎉 You're Done!

Your ML Dashboard is now live! Access it at:
- http://localhost:4200

Enjoy exploring your models! 📊
