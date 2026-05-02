import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { DataService } from '../services/data.service';

@Component({
  selector: 'app-clustering',
  templateUrl: './clustering.component.html',
  styleUrls: ['./clustering.component.css']
})
export class ClusteringComponent implements OnInit {
  pcaVisualization: any = null;
  silhouetteAnalysis: any = null;
  clustersSummary: any = null;
  loading = false;
  error: string | null = null;

  constructor(
    private apiService: ApiService,
    private dataService: DataService
  ) { }

  ngOnInit(): void {
    this.loadClusteringData();
  }

  loadClusteringData(): void {
    this.loading = true;
    this.error = null;
    this.dataService.setLoading(true);

    Promise.all([
      this.apiService.getPCAVisualization().toPromise(),
      this.apiService.getSilhouetteAnalysis().toPromise(),
      this.apiService.getClustersSummary().toPromise()
    ]).then(([pca, sil, summary]: any) => {
      this.pcaVisualization = pca;
      this.silhouetteAnalysis = sil;
      this.clustersSummary = summary;
      this.loading = false;
      this.dataService.setLoading(false);
    }).catch((err: any) => {
      this.error = 'Failed to load clustering data';
      this.dataService.setError(this.error);
      this.loading = false;
      this.dataService.setLoading(false);
    });
  }

  getScoreWidth(value: any): number {
    const numValue = Number(value);
    return (numValue + 1) * 50;
  }

  getScoreValue(value: any): string {
    return Number(value).toFixed(4);
  }

  getClusterSize(value: any): number {
    return value && value.size ? value.size : 0;
  }

  getClusterAvgEvents(value: any): string {
    return value && value.avg_events ? Number(value.avg_events).toFixed(2) : '0.00';
  }

  getClusterAvgParticipants(value: any): string {
    return value && value.avg_participants ? Number(value.avg_participants).toFixed(2) : '0.00';
  }

  getClusterUnits(value: any): string {
    return value && value.units ? (Array.isArray(value.units) ? value.units.join(', ') : '') : '';
  }
}
