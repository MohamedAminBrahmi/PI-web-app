// Data models for API responses
export interface ModelMetrics {
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1?: number;
  auc?: number;
  mse?: number;
  rmse?: number;
  mae?: number;
  r2?: number;
  mape?: number;
}

export interface ClassificationModel {
  [key: string]: ModelMetrics;
}

export interface RegressionModel {
  [key: string]: ModelMetrics;
}

export interface DatasetStats {
  total_records: number;
  total_columns: number;
  date_range: {
    start: string;
    end: string;
  };
  missing_values: {
    [key: string]: number;
  };
  numeric_summary: any;
  models: {
    classification: string[];
    regression: string[];
    time_series: string[];
  };
}

export interface ConfusionMatrixData {
  model: string;
  confusion_matrix: number[][];
  shape: [number, number];
}

export interface RegressionData {
  model: string;
  actual: number[];
  predicted: number[];
  count: number;
}

export interface ResidualData {
  model: string;
  residuals: number[];
  mean: number;
  std: number;
  count: number;
}

export interface PCAVisualization {
  pca: {
    x: number[];
    y: number[];
  };
  clusters: number[];
  features: string[];
}

export interface SilhouetteAnalysis {
  silhouette_scores: {
    [key: string]: number;
  };
  best_k: number;
  best_score: number;
}

export interface TimeSeriesForecast {
  model: string;
  actual: number[];
  predicted: number[];
  rmse: number;
  mae: number;
  mape: number;
}

export interface TimeSeriesData {
  train: number[];
  test: number[];
  train_size: number;
  test_size: number;
}
