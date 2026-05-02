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
  selectedModel: string = '';
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
        if (Object.keys(this.forecastingModels).length > 0) {
          this.selectedModel = Object.keys(this.forecastingModels)[0];
          this.loadForecastData();
        }
        this.loading = false;
        this.dataService.setLoading(false);
      },
      error: (err) => {
        this.error = 'Failed to load forecasting models';
        this.dataService.setError(this.error);
        this.loading = false;
        this.dataService.setLoading(false);
      }
    });
  }

  onModelChange(): void {
    this.forecastData = null;
    this.loadForecastData();
  }

  loadForecastData(): void {
    if (!this.selectedModel) return;

    this.loading = true;
    Promise.all([
      this.apiService.getForecast(this.selectedModel).toPromise(),
      this.apiService.getTimeSeriesData().toPromise()
    ]).then(([forecast, tsData]: any) => {
      this.forecastData = forecast;
      this.timeSeriesData = tsData;
      this.loading = false;
      this.dataService.setLoading(false);
    }).catch((err: any) => {
      this.error = 'Failed to load forecast data';
      this.dataService.setError(this.error);
      this.loading = false;
      this.dataService.setLoading(false);
    });
  }
}
