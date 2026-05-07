import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})
export class PredictionComponent implements OnInit {
  Math = Math;

  // Activity type options
  activityTypes = [
    { value: 0, label: 'Camp' },
    { value: 1, label: 'Hike' },
    { value: 2, label: 'Workshop' },
    { value: 3, label: 'Community Service' },
    { value: 4, label: 'Sports Event' },
    { value: 5, label: 'Cultural Event' }
  ];

  // Season options
  seasons = [
    { value: 0, label: 'Spring (Mar–May)' },
    { value: 1, label: 'Summer (Jun–Aug)' },
    { value: 2, label: 'Autumn (Sep–Nov)' },
    { value: 3, label: 'Winter (Dec–Feb)' }
  ];

  // Age group options
  ageGroups = [
    { value: 0, label: 'Cubs (8–11 years)' },
    { value: 1, label: 'Scouts (12–16 years)' },
    { value: 2, label: 'Rovers (17–25 years)' },
    { value: 3, label: 'Mixed (all ages)' }
  ];

  // Form values
  activityType: number = 0;
  duration: number = 3;
  budgetPerPerson: number = 50;
  season: number = 1;
  ageGroup: number = 1;

  // State
  prediction: any = null;
  loading: boolean = false;
  error: string = '';
  estimatedParticipants: number = 0;
  safetyBuffer: number = 0;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {}

  estimateParticipants(): void {
    this.loading = true;
    this.error = '';
    this.prediction = null;

    // Map friendly inputs to the feature format the backend expects
    const features = {
      feature_1: this.activityType,
      feature_2: this.duration,
      feature_3: this.budgetPerPerson,
      feature_4: this.season,
      feature_5: this.ageGroup
    };

    // Always use regression with auto-selected best model
    this.apiService.predict('auto', 'regression', features)
      .subscribe(
        (result) => {
          this.prediction = result;
          // Ensure positive integer for participants
          this.estimatedParticipants = Math.max(1, Math.round(Math.abs(result.prediction)));
          this.safetyBuffer = Math.ceil(this.estimatedParticipants * 1.1);
          this.loading = false;
        },
        (error) => {
          console.error('Estimation error:', error);
          this.error = 'Unable to generate estimate. Please try again.';
          this.loading = false;
        }
      );
  }

  resetForm(): void {
    this.activityType = 0;
    this.duration = 3;
    this.budgetPerPerson = 50;
    this.season = 1;
    this.ageGroup = 1;
    this.prediction = null;
    this.error = '';
  }

  getActivityLabel(): string {
    const found = this.activityTypes.find(a => a.value === this.activityType);
    return found ? found.label : '';
  }

  getSeasonLabel(): string {
    const found = this.seasons.find(s => s.value === this.season);
    return found ? found.label : '';
  }

  getAgeGroupLabel(): string {
    const found = this.ageGroups.find(a => a.value === this.ageGroup);
    return found ? found.label : '';
  }
}
