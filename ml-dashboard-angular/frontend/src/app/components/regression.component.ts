import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { DataService } from '../services/data.service';

@Component({
  selector: 'app-regression',
  templateUrl: './regression.component.html',
  styleUrls: ['./regression.component.css']
})
export class RegressionComponent implements OnInit {
  regressionModels: any = null;
  bestModel: string = '';
  bestMetrics: any = { r2: 0, rmse: 0, mae: 0, mse: 0 };
  regressionData: any = null;
  loading = false;
  error: string | null = null;
  Math = Math;

  constructor(
    private apiService: ApiService,
    private dataService: DataService
  ) { }

  ngOnInit(): void {
    this.loadRegressionModels();
  }

  loadRegressionModels(): void {
    this.loading = true;
    this.error = null;
    this.dataService.setLoading(true);

    this.apiService.getRegressionModels().subscribe({
      next: (response) => {
        this.regressionModels = response.models;
        // Auto-select the best model (highest R²)
        this.bestModel = this.findBestModel(this.regressionModels);
        if (this.bestModel) {
          this.bestMetrics = this.regressionModels[this.bestModel];
          this.loadModelDetails();
        }
        this.loading = false;
        this.dataService.setLoading(false);
      },
      error: (err) => {
        this.error = 'Unable to load estimation data. Please check your connection and try again.';
        this.dataService.setError(this.error);
        this.loading = false;
        this.dataService.setLoading(false);
      }
    });
  }

  private findBestModel(models: any): string {
    if (!models) return '';
    let best = '';
    let bestScore = -Infinity;
    for (const [name, metrics] of Object.entries(models) as [string, any][]) {
      const r2 = metrics.r2 || 0;
      if (r2 > bestScore) {
        bestScore = r2;
        best = name;
      }
    }
    return best;
  }

  loadModelDetails(): void {
    if (!this.bestModel) return;

    this.loading = true;
    this.apiService.getActualVsPredicted(this.bestModel).toPromise()
      .then((data: any) => {
        this.regressionData = data;
        this.loading = false;
        this.dataService.setLoading(false);
      })
      .catch((err: any) => {
        this.loading = false;
        this.dataService.setLoading(false);
      });
  }

  // Gauge helpers
  getGaugeDash(value: number): string {
    const circumference = 2 * Math.PI * 50;
    const filled = circumference * Math.max(0, value || 0);
    return `${filled} ${circumference}`;
  }

  getR2Level(r2: number): string {
    if (r2 >= 0.8) return 'level-excellent';
    if (r2 >= 0.6) return 'level-good';
    if (r2 >= 0.4) return 'level-fair';
    return 'level-low';
  }

  getR2Emoji(r2: number): string {
    if (r2 >= 0.8) return '🏆';
    if (r2 >= 0.6) return '👍';
    if (r2 >= 0.4) return '📊';
    return '📈';
  }

  getR2Message(r2: number): string {
    if (r2 >= 0.8) return 'Excellent! Estimates closely match real numbers.';
    if (r2 >= 0.6) return 'Good accuracy. Estimates are reliable for planning.';
    if (r2 >= 0.4) return 'Moderate accuracy. Use as a helpful starting point.';
    return 'Estimates give general direction but may vary from reality.';
  }

  getComparisonItems(): any[] {
    if (!this.regressionData?.actual || !this.regressionData?.predicted) return [];
    const items: any[] = [];
    const count = Math.min(10, this.regressionData.actual.length);

    for (let i = 0; i < count; i++) {
      const actual = this.regressionData.actual[i];
      const predicted = this.regressionData.predicted[i];
      const accuracy = actual !== 0 
        ? Math.max(0, (1 - Math.abs(actual - predicted) / Math.abs(actual)) * 100)
        : (predicted === 0 ? 100 : 0);
      
      let cls = 'comp-good';
      if (accuracy < 50) cls = 'comp-low';
      else if (accuracy < 75) cls = 'comp-fair';

      items.push({
        index: i + 1,
        actual: actual.toFixed(0),
        predicted: predicted.toFixed(0),
        accuracy: accuracy.toFixed(0) + '%',
        class: cls
      });
    }
    return items;
  }
}
