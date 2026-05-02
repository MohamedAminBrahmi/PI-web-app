import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { DataService } from '../services/data.service';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.css']
})
export class OverviewComponent implements OnInit {
  datasetStats: any = null;
  modelsInfo: any = null;
  loading = false;
  error: string | null = null;

  constructor(
    private apiService: ApiService,
    private dataService: DataService
  ) { }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;
    this.error = null;
    this.dataService.setLoading(true);

    this.apiService.getDatasetStats().subscribe({
      next: (stats: any) => {
        this.datasetStats = stats;
        this.loadModelsInfo();
      },
      error: (err: any) => {
        this.error = 'Failed to load dataset statistics';
        this.dataService.setError(this.error);
        this.loading = false;
        this.dataService.setLoading(false);
      }
    });
  }

  private loadModelsInfo(): void {
    this.apiService.getModelsInfo().subscribe({
      next: (info: any) => {
        this.modelsInfo = info;
        this.loading = false;
        this.dataService.setLoading(false);
      },
      error: (err: any) => {
        this.error = 'Failed to load models information';
        this.dataService.setError(this.error);
        this.loading = false;
        this.dataService.setLoading(false);
      }
    });
  }
  getFormatted(value: any, field: string): string {
    if (!value || !value[field]) return '-';
    return Number(value[field]).toFixed(4);
  }}
