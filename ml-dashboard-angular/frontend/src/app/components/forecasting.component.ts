import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { DataService } from '../services/data.service';

@Component({
  selector: 'app-forecasting',
  templateUrl: './forecasting.component.html',
  styleUrls: ['./forecasting.component.css']
})
export class ForecastingComponent implements OnInit {
  forecastingModels: any = null;
  bestModel: string = '';
  bestMetrics: any = { rmse: 0, mae: 0, mape: 0 };
  forecastData: any = null;
  timeSeriesData: any = null;
  loading = false;
  error: string | null = null;
  Math = Math;

  constructor(
    private apiService: ApiService,
    private dataService: DataService
  ) { }

  ngOnInit(): void {
    this.loadForecastingModels();
  }

  loadForecastingModels(): void {
    this.loading = true;
    this.error = null;
    this.dataService.setLoading(true);

    this.apiService.getForecastingModels().subscribe({
      next: (response) => {
        this.forecastingModels = response.models;
        // Auto-select the best model (lowest MAPE)
        this.bestModel = this.findBestModel(this.forecastingModels);
        if (this.bestModel) {
          this.bestMetrics = this.forecastingModels[this.bestModel];
          this.loadForecastData();
        }
        this.loading = false;
        this.dataService.setLoading(false);
      },
      error: (err) => {
        this.error = 'Unable to load forecast data. Please check your connection and try again.';
        this.dataService.setError(this.error);
        this.loading = false;
        this.dataService.setLoading(false);
      }
    });
  }

  private findBestModel(models: any): string {
    if (!models) return '';
    let best = '';
    let bestMape = Infinity;
    for (const [name, metrics] of Object.entries(models) as [string, any][]) {
      const mape = metrics.mape || Infinity;
      if (mape < bestMape) {
        bestMape = mape;
        best = name;
      }
    }
    return best;
  }

  loadForecastData(): void {
    if (!this.bestModel) return;

    this.loading = true;
    Promise.all([
      this.apiService.getForecast(this.bestModel).toPromise(),
      this.apiService.getTimeSeriesData().toPromise()
    ]).then(([forecast, tsData]: any) => {
      this.forecastData = forecast;
      this.timeSeriesData = tsData;
      this.loading = false;
      this.dataService.setLoading(false);
    }).catch((err: any) => {
      this.loading = false;
      this.dataService.setLoading(false);
    });
  }

  // Accuracy helpers
  getForecastAccuracy(): string {
    return Math.max(0, 100 - (this.bestMetrics.mape || 0)).toFixed(1);
  }

  getGaugeDash(): string {
    const circumference = 2 * Math.PI * 50;
    const accuracy = Math.max(0, (100 - (this.bestMetrics.mape || 0)) / 100);
    const filled = circumference * accuracy;
    return `${filled} ${circumference}`;
  }

  getMapeLevel(mape: number): string {
    if (mape <= 5) return 'level-excellent';
    if (mape <= 15) return 'level-good';
    if (mape <= 30) return 'level-fair';
    return 'level-low';
  }

  getMapeEmoji(mape: number): string {
    if (mape <= 5) return '🏆';
    if (mape <= 15) return '👍';
    if (mape <= 30) return '📊';
    return '📈';
  }

  getMapeMessage(mape: number): string {
    if (mape <= 5) return 'Excellent! Forecasts are very close to what actually happens.';
    if (mape <= 15) return 'Good accuracy. Forecasts are reliable for planning purposes.';
    if (mape <= 30) return 'Moderate accuracy. Use forecasts as a helpful starting point.';
    return 'Forecasts provide general direction for planning.';
  }

  getForecastItems(): any[] {
    if (!this.forecastData?.actual || !this.forecastData?.predicted) return [];
    const items: any[] = [];
    const count = Math.min(15, this.forecastData.actual.length);

    // Find max value for bar scaling
    let maxVal = 1;
    for (let i = 0; i < count; i++) {
      maxVal = Math.max(maxVal, Math.abs(this.forecastData.actual[i]), Math.abs(this.forecastData.predicted[i]));
    }

    for (let i = 0; i < count; i++) {
      const actual = this.forecastData.actual[i];
      const predicted = this.forecastData.predicted[i];
      const accuracy = actual !== 0
        ? Math.max(0, (1 - Math.abs(actual - predicted) / Math.max(1, Math.abs(actual))) * 100)
        : (predicted === 0 ? 100 : 0);

      let cls = 'fi-good';
      if (accuracy < 50) cls = 'fi-low';
      else if (accuracy < 75) cls = 'fi-fair';

      items.push({
        index: i + 1,
        actual: actual.toFixed(1),
        predicted: predicted.toFixed(1),
        actualPct: (Math.abs(actual) / maxVal) * 100,
        predictedPct: (Math.abs(predicted) / maxVal) * 100,
        accuracy: accuracy.toFixed(0) + '%',
        class: cls
      });
    }
    return items;
  }
}
