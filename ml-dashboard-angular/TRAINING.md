# ML Training Pipeline Documentation

## 📋 Overview

This document describes the automated ML training pipeline with MLflow experiment tracking for the ML Dashboard project.

## 🎯 Features

### 1. **Automated Training Pipeline**
- End-to-end preprocessing → training → evaluation → saving
- Support for multiple ML tasks:
  - Classification (Random Forest v1 & v2)
  - Regression (Linear Regression, Random Forest v1 & v2)
  - Clustering (KMeans with PCA visualization)
  - Time Series Forecasting (Random Forest)

### 2. **MLflow Integration**
- Automatic experiment tracking
- Parameter and metric logging
- Model artifact storage
- Run comparison and visualization

### 3. **Model Versioning**
- Multiple model versions (v1, v2)
- Model performance tracking
- Previous versions remain accessible
- Easy model rollback

### 4. **Model Serving (API)**
- REST API with prediction endpoints
- Support for single and batch predictions
- Model availability listing
- Confidence scores for predictions

## 🚀 Quick Start

### Option 1: Using Setup Script

```bash
# Run the complete setup and training
python setup.py

# View configuration
python setup.py --config

# Setup environment only (no training)
python setup.py --setup-only
```

### Option 2: Manual Training

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run training pipeline
python train.py
```

### Option 3: Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Training will run automatically, and MLflow will be available at:
# http://localhost:5000
```

## 📊 Training Pipeline Components

### Classification Pipeline
- **Models**: Random Forest (v1: 100 trees, v2: 200 trees)
- **Metrics**:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - ROC AUC
  - Confusion Matrix
  - Classification Report
  - ROC Curve

### Regression Pipeline
- **Models**: 
  - Linear Regression
  - Random Forest (v1: 100 trees, v2: 200 trees)
- **Metrics**:
  - MSE (Mean Squared Error)
  - RMSE (Root Mean Squared Error)
  - MAE (Mean Absolute Error)
  - R² Score
  - Actual vs Predicted values
  - Residuals

### Clustering Pipeline
- **Algorithm**: KMeans (3 clusters)
- **Metrics**:
  - Silhouette scores (for k=2 to 7)
  - PCA visualization (2D)
  - Cluster centers
  - Inertia
  - Cluster assignments

### Forecasting Pipeline
- **Algorithm**: Random Forest with sliding window
- **Metrics**:
  - RMSE
  - MAE
  - R² Score
  - Forecast predictions
  - Time series data

## 📁 File Structure

```
ml-dashboard-angular/
├── backend/
│   ├── train.py              # Main training pipeline
│   ├── config_utils.py       # Configuration management
│   ├── requirements.txt      # Python dependencies
│   ├── models/               # Saved models directory
│   ├── data/                 # Training data directory
│   ├── mlruns/               # MLflow tracking directory
│   └── app/
│       ├── main.py           # FastAPI application
│       ├── routes/
│       │   └── prediction.py # Prediction endpoints
│       └── ...
├── setup.py                  # Setup and training script
└── ...
```

## 🔧 Configuration

Edit environment variables in `.env` or pass them directly:

```bash
# MLflow Configuration
MLFLOW_TRACKING_URI="file:./backend/mlruns"
MLFLOW_EXPERIMENT_NAME="ML_Dashboard_Training"

# API Configuration
API_HOST="0.0.0.0"
API_PORT="8000"
API_RELOAD="True"

# Training Configuration
TRAIN_TEST_SPLIT="0.2"
RANDOM_STATE="42"
N_ESTIMATORS="100"

# Dataset Configuration
DATASET_SIZE="1000"
N_FEATURES="5"
N_CLUSTERS="3"
```

View current configuration:
```bash
python setup.py --config
```

## 📈 MLflow Usage

### Access MLflow UI

```bash
# During development
mlflow ui

# Via Docker
# Already running on http://localhost:5000
```

### View Experiments and Runs

1. Open MLflow UI at `http://localhost:5000`
2. Select the "ML_Dashboard_Training" experiment
3. View different runs and compare metrics
4. Download artifacts (models, results)

### Export Metrics

```python
import mlflow

client = mlflow.tracking.MlflowClient()
experiment = client.get_experiment_by_name("ML_Dashboard_Training")
runs = client.search_runs(experiment.experiment_id)

for run in runs:
    print(f"Run ID: {run.info.run_id}")
    print(f"Metrics: {run.data.metrics}")
    print(f"Params: {run.data.params}")
```

## 🔮 Making Predictions

### Using the API

#### Single Prediction
```bash
curl -X POST "http://localhost:8000/api/v1/prediction/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "RandomForest_v1",
    "model_type": "classification",
    "features": {
      "feature_1": 0.5,
      "feature_2": -0.2,
      "feature_3": 1.0,
      "feature_4": 50.0,
      "feature_5": 1
    }
  }'
```

#### Batch Predictions
```bash
curl -X POST "http://localhost:8000/api/v1/prediction/batch-predict" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "model_name": "RandomForest_v1",
      "model_type": "classification",
      "features": {"feature_1": 0.5, ...}
    },
    ...
  ]'
```

#### Available Models
```bash
curl -X GET "http://localhost:8000/api/v1/prediction/predict/available-models"
```

### Using TypeScript/Angular Frontend

```typescript
// In your component
constructor(private apiService: ApiService) {}

makePrediction() {
  this.apiService.predict('RandomForest_v1', 'classification', {
    feature_1: 0.5,
    feature_2: -0.2,
    feature_3: 1.0,
    feature_4: 50.0,
    feature_5: 1
  }).subscribe(
    (result) => console.log('Prediction:', result),
    (error) => console.error('Error:', error)
  );
}
```

## 📊 Model Artifacts

### Classification Results
```
cls_results.pkl
├── RandomForest_v1
│   ├── accuracy: float
│   ├── precision: float
│   ├── recall: float
│   ├── f1: float
│   ├── auc: float
│   ├── confusion_matrix: List[List[int]]
│   ├── classification_report: Dict
│   └── roc_curve: Dict (fpr, tpr)
└── RandomForest_v2
    └── ...
```

### Regression Results
```
reg_results.pkl
├── LinearRegression
│   ├── mse: float
│   ├── rmse: float
│   ├── mae: float
│   ├── r2: float
│   ├── actual_vs_predicted: Dict
│   └── residuals: List[float]
└── ...
```

### Clustering Results
```
cluster_results.pkl
├── clusters: List[int]
├── pca_coords: List[List[float]]
├── silhouette_scores: Dict
├── cluster_centers: List[List[float]]
└── inertia: float
```

### Forecasting Results
```
ts_results.pkl
├── forecast: List[float]
├── actual: List[float]
├── metrics: Dict
└── time_series_data: List[float]
```

## 🐛 Troubleshooting

### Issue: Models not found

**Solution**: Run the training pipeline first
```bash
python setup.py
```

### Issue: MLflow not tracking runs

**Solution**: Check MLflow URI configuration
```bash
python setup.py --config
```

### Issue: Prediction endpoint returns 404

**Solution**: Verify models are loaded
```bash
curl http://localhost:8000/api/v1/prediction/predict/available-models
```

### Issue: Docker build fails

**Solution**: Clear cache and rebuild
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## 📚 API Endpoints

### Prediction Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/prediction/predict` | Make a single prediction |
| POST | `/api/v1/prediction/batch-predict` | Make multiple predictions |
| GET | `/api/v1/prediction/predict/available-models` | List available models |

### Metrics Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/overview/stats` | Dataset statistics |
| GET | `/api/v1/classification/models` | Classification models metrics |
| GET | `/api/v1/regression/models` | Regression models metrics |
| GET | `/api/v1/clustering/silhouette-analysis` | Clustering metrics |
| GET | `/api/v1/forecasting/models` | Forecasting models metrics |

## 🎓 Advanced Usage

### Custom Model Training

Edit `backend/train.py` to add custom models:

```python
class CustomPipeline:
    def train(self, X, y):
        # Your custom training code
        with mlflow.start_run():
            model = YourCustomModel()
            model.fit(X, y)
            
            # Log metrics
            mlflow.log_metric("accuracy", accuracy)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
```

### Custom Feature Engineering

Add preprocessing steps in the pipeline:

```python
def _preprocess(self, X):
    # Custom preprocessing
    X_transformed = your_transformer.fit_transform(X)
    return X_transformed
```

## 📝 Best Practices

1. **Version Control**: Always commit model training scripts
2. **Experiment Tracking**: Use meaningful run names
3. **Model Evaluation**: Always validate on test set
4. **Documentation**: Keep track of model changes
5. **Data Management**: Maintain data versioning
6. **API Testing**: Test predictions with various inputs

## 🚀 Deployment

### Local Deployment
```bash
python setup.py  # Train models
python -m uvicorn backend.app.main:app --reload  # Start API
cd frontend && npm start  # Start frontend
```

### Docker Deployment
```bash
docker-compose up --build
```

### Production Deployment

1. Build production images
2. Configure MLflow remote backend (e.g., AWS S3)
3. Deploy with Kubernetes or cloud provider
4. Set up model serving with dedicated service

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review MLflow documentation
3. Check FastAPI documentation
4. Open an issue on GitHub

## 📄 License

[Your License Here]
