import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { DataService } from '../services/data.service';

@Component({
  selector: 'app-classification',
  templateUrl: './classification.component.html',
  styleUrls: ['./classification.component.css']
})
export class ClassificationComponent implements OnInit {
  classificationModels: any = null;
  bestModel: string = '';
  bestMetrics: any = { accuracy: 0, precision: 0, recall: 0, f1: 0, auc: 0 };
  confusionMatrix: any = null;
  classificationReport: any = null;
  loading = false;
  error: string | null = null;

  constructor(
    private apiService: ApiService,
    private dataService: DataService
  ) { }

  ngOnInit(): void {
    this.loadClassificationModels();
  }

  loadClassificationModels(): void {
    this.loading = true;
    this.error = null;
    this.dataService.setLoading(true);

    this.apiService.getClassificationModels().subscribe({
      next: (response: any) => {
        this.classificationModels = response.models;
        // Auto-select the best model (highest F1 score)
        this.bestModel = this.findBestModel(this.classificationModels);
        if (this.bestModel) {
          this.bestMetrics = this.classificationModels[this.bestModel];
          this.loadModelDetails();
        }
        this.loading = false;
        this.dataService.setLoading(false);
      },
      error: (err: any) => {
        this.error = 'Unable to load participation data. Please check your connection and try again.';
        this.dataService.setError(this.error);
        this.loading = false;
        this.dataService.setLoading(false);
      }
    });
  }

  private findBestModel(models: any): string {
    if (!models) return '';
    let best = '';
    let bestScore = -1;
    for (const [name, metrics] of Object.entries(models) as [string, any][]) {
      const f1 = metrics.f1 || 0;
      if (f1 > bestScore) {
        bestScore = f1;
        best = name;
      }
    }
    return best;
  }

  loadModelDetails(): void {
    if (!this.bestModel) return;

    this.loading = true;
    Promise.all([
      this.apiService.getConfusionMatrix(this.bestModel).toPromise(),
      this.apiService.getClassificationReport(this.bestModel).toPromise()
    ]).then(([cm, report]) => {
      this.confusionMatrix = cm;
      this.classificationReport = report;
      this.loading = false;
      this.dataService.setLoading(false);
    }).catch(err => {
      this.loading = false;
      this.dataService.setLoading(false);
    });
  }

  // Gauge helpers
  getGaugeDash(value: number): string {
    const circumference = 2 * Math.PI * 50;
    const filled = circumference * (value || 0);
    return `${filled} ${circumference}`;
  }

  getAccuracyLevel(accuracy: number): string {
    if (accuracy >= 0.8) return 'level-excellent';
    if (accuracy >= 0.6) return 'level-good';
    if (accuracy >= 0.4) return 'level-fair';
    return 'level-low';
  }

  getAccuracyEmoji(accuracy: number): string {
    if (accuracy >= 0.8) return '🏆';
    if (accuracy >= 0.6) return '👍';
    if (accuracy >= 0.4) return '📊';
    return '📈';
  }

  getAccuracyMessage(accuracy: number): string {
    const pct = (accuracy * 100).toFixed(0);
    if (accuracy >= 0.8) return `Excellent! The system is very reliable at predicting participation.`;
    if (accuracy >= 0.6) return `Good performance. The system makes solid predictions most of the time.`;
    if (accuracy >= 0.4) return `Moderate accuracy. Predictions give a useful starting point for planning.`;
    return `The system is still learning. Use predictions as general guidance.`;
  }

  // Confusion matrix helpers
  getCorrectCount(): number {
    if (!this.confusionMatrix?.confusion_matrix) return 0;
    let correct = 0;
    this.confusionMatrix.confusion_matrix.forEach((row: number[], i: number) => {
      correct += row[i] || 0;
    });
    return correct;
  }

  getIncorrectCount(): number {
    return this.getTotalCount() - this.getCorrectCount();
  }

  getTotalCount(): number {
    if (!this.confusionMatrix?.confusion_matrix) return 0;
    let total = 0;
    this.confusionMatrix.confusion_matrix.forEach((row: number[]) => {
      row.forEach((cell: number) => { total += cell; });
    });
    return total;
  }

  getSuccessRate(): number {
    const total = this.getTotalCount();
    if (total === 0) return 0;
    return (this.getCorrectCount() / total) * 100;
  }

  // Report helpers
  getSimpleReport(): any[] {
    if (!this.classificationReport?.report) return [];
    const report = this.classificationReport.report;
    const icons = ['🟢', '🟡', '🔴', '🔵', '🟣'];
    const names = ['High Participation', 'Medium Participation', 'Low Participation', 'Level 4', 'Level 5'];
    const results: any[] = [];

    let idx = 0;
    for (const [key, value] of Object.entries(report) as [string, any][]) {
      if (['accuracy', 'macro avg', 'weighted avg'].includes(key)) continue;
      results.push({
        icon: icons[idx % icons.length],
        name: names[idx] || `Level ${idx + 1}`,
        accuracy: ((value['f1-score'] || 0) * 100).toFixed(0),
        count: value['support'] || 0
      });
      idx++;
    }
    return results;
  }

  getBarClass(accuracy: number): string {
    if (accuracy >= 70) return 'bar-good';
    if (accuracy >= 50) return 'bar-fair';
    return 'bar-low';
  }
}
