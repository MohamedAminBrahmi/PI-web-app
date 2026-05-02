import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})
export class PredictionComponent implements OnInit {
  
  availableModels: any = {};
  selectedModelType: string = 'classification';
  selectedModel: string = '';
  
  featureKeys = ['feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_5'];
  featureLabels = [
    'AGE',
    'DURATION',
    'ACTIVITY BUDGET',
    'UNIT BUDGET',
    'GENRE'
  ];
  
  features: any = {
    feature_1: 0,
    feature_2: 0,
    feature_3: 0,
    feature_4: 50,
    feature_5: 0
  };
  
  prediction: any = null;
  loading: boolean = false;
  error: string = '';
  
  constructor(private apiService: ApiService) {}
  
  ngOnInit(): void {
    this.loadAvailableModels();
  }
  
  loadAvailableModels(): void {
    this.apiService.getAvailableModels().subscribe(
      (data) => {
        this.availableModels = data;
        if (data.classification && data.classification.length > 0) {
          this.selectedModel = data.classification[0];
        }
      },
      (error) => {
        console.error('Error loading models:', error);
        this.error = 'Failed to load available models';
      }
    );
  }
  
  onModelTypeChange(): void {
    const models = this.availableModels[this.selectedModelType] || [];
    this.selectedModel = models.length > 0 ? models[0] : '';
  }
  
  makePrediction(): void {
    if (!this.selectedModel) {
      this.error = 'Please select a model';
      return;
    }
    
    this.loading = true;
    this.error = '';
    
    this.apiService.predict(this.selectedModel, this.selectedModelType, this.features)
      .subscribe(
        (result) => {
          this.prediction = result;
          this.loading = false;
        },
        (error) => {
          console.error('Prediction error:', error);
          this.error = error.error?.detail || 'Failed to make prediction';
          this.loading = false;
        }
      );
  }
  
  resetForm(): void {
    this.features = {
      feature_1: 0,
      feature_2: 0,
      feature_3: 0,
      feature_4: 50,
      feature_5: 0
    };
    this.prediction = null;
    this.error = '';
  }
  
  getModelList(): string[] {
    return this.availableModels[this.selectedModelType] || [];
  }
}
