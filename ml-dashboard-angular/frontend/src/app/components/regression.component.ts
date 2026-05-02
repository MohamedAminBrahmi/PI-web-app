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
  selectedModel: string = '';
  regressionData: any = null;
  residuals: any = null;
  metrics: any = null;
  loading = false;
  error: string | null = null;

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
        if (Object.keys(this.regressionModels).length > 0) {
          this.selectedModel = Object.keys(this.regressionModels)[0];
          this.loadModelDetails();
        }
        this.loading = false;
        this.dataService.setLoading(false);
      },
      error: (err) => {
        this.error = 'Failed to load regression models';
        this.dataService.setError(this.error);
        this.loading = false;
        this.dataService.setLoading(false);
      }
    });
  }

  onModelChange(): void {
    this.regressionData = null;
    this.residuals = null;
    this.metrics = null;
    this.loadModelDetails();
  }

  loadModelDetails(): void {
    if (!this.selectedModel) return;

    this.loading = true;
    Promise.all([
      this.apiService.getActualVsPredicted(this.selectedModel).toPromise(),
      this.apiService.getResiduals(this.selectedModel).toPromise(),
      this.apiService.getRegressionMetrics(this.selectedModel).toPromise()
    ]).then(([data, resid, met]: any) => {
      this.regressionData = data;
      this.residuals = resid;
      this.metrics = met;
      this.loading = false;
      this.dataService.setLoading(false);
    }).catch((err: any) => {
      this.error = 'Failed to load model details';
      this.dataService.setError(this.error);
      this.loading = false;
      this.dataService.setLoading(false);
    });
  }
}
