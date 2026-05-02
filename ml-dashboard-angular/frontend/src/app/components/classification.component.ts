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
  selectedModel: string = '';
  confusionMatrix: any = null;
  rocCurve: any = null;
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
        if (Object.keys(this.classificationModels).length > 0) {
          this.selectedModel = Object.keys(this.classificationModels)[0];
          this.loadModelDetails();
        }
        this.loading = false;
        this.dataService.setLoading(false);
      },
      error: (err: any) => {
        this.error = 'Failed to load classification models';
        this.dataService.setError(this.error);
        this.loading = false;
        this.dataService.setLoading(false);
      }
    });
  }

  onModelChange(): void {
    this.confusionMatrix = null;
    this.rocCurve = null;
    this.classificationReport = null;
    this.loadModelDetails();
  }

  loadModelDetails(): void {
    if (!this.selectedModel) return;

    this.loading = true;
    Promise.all([
      this.apiService.getConfusionMatrix(this.selectedModel).toPromise(),
      this.apiService.getROCCurve(this.selectedModel).toPromise(),
      this.apiService.getClassificationReport(this.selectedModel).toPromise()
    ]).then(([cm, roc, report]) => {
      this.confusionMatrix = cm;
      this.rocCurve = roc;
      this.classificationReport = report;
      this.loading = false;
      this.dataService.setLoading(false);
    }).catch(err => {
      this.error = 'Failed to load model details';
      this.dataService.setError(this.error);
      this.loading = false;
      this.dataService.setLoading(false);
    });
  }

  isNumber(value: any): boolean {
    return typeof value === 'number';
  }

  shouldShowRow(key: any): boolean {
    const keyStr = String(key);
    return !['accuracy', 'macro avg', 'weighted avg'].includes(keyStr);
  }

  getMetricsAsArray(obj: any): any[] {
    if (!obj) return [];
    return Object.entries(obj).map(([k, v]) => ({ key: k, value: v }));
  }
}
