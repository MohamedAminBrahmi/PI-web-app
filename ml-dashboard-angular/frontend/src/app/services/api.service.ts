import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  // Overview endpoints
  healthCheck(): Observable<any> {
    return this.http.get(`${this.apiUrl}/overview/health`);
  }

  getDatasetStats(): Observable<any> {
    return this.http.get(`${this.apiUrl}/overview/stats`);
  }

  getModelsInfo(): Observable<any> {
    return this.http.get(`${this.apiUrl}/overview/models-info`);
  }

  // Classification endpoints
  getClassificationModels(): Observable<any> {
    return this.http.get(`${this.apiUrl}/classification/models`);
  }

  getConfusionMatrix(modelName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/classification/confusion-matrix/${modelName}`);
  }

  getROCCurve(modelName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/classification/roc-curve/${modelName}`);
  }

  getClassificationReport(modelName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/classification/classification-report/${modelName}`);
  }

  // Regression endpoints
  getRegressionModels(): Observable<any> {
    return this.http.get(`${this.apiUrl}/regression/models`);
  }

  getActualVsPredicted(modelName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/regression/actual-vs-predicted/${modelName}`);
  }

  getResiduals(modelName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/regression/residuals/${modelName}`);
  }

  getRegressionMetrics(modelName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/regression/metrics/${modelName}`);
  }

  // Clustering endpoints
  getPCAVisualization(): Observable<any> {
    return this.http.get(`${this.apiUrl}/clustering/pca-visualization`);
  }

  getSilhouetteAnalysis(): Observable<any> {
    return this.http.get(`${this.apiUrl}/clustering/silhouette-analysis`);
  }

  getClustersSummary(): Observable<any> {
    return this.http.get(`${this.apiUrl}/clustering/clusters-summary`);
  }

  // Forecasting endpoints
  getForecastingModels(): Observable<any> {
    return this.http.get(`${this.apiUrl}/forecasting/models`);
  }

  getForecast(modelName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/forecasting/forecast/${modelName}`);
  }

  getTimeSeriesData(): Observable<any> {
    return this.http.get(`${this.apiUrl}/forecasting/time-series-data`);
  }

  // Prediction endpoints
  predict(modelName: string, modelType: string, features: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/prediction/predict`, {
      model_name: modelName,
      model_type: modelType,
      features: features
    });
  }

  getAvailableModels(): Observable<any> {
    return this.http.get(`${this.apiUrl}/prediction/predict/available-models`);
  }

  batchPredict(predictions: any[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/prediction/batch-predict`, predictions);
  }
}
