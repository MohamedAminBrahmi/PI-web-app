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
      this.apiService.getSilhouetteAnalysis().toPromise(),
      this.apiService.getClustersSummary().toPromise()
    ]).then(([sil, summary]: any) => {
      this.silhouetteAnalysis = sil;
      this.clustersSummary = summary;
      this.loading = false;
      this.dataService.setLoading(false);
    }).catch((err: any) => {
      this.error = 'Unable to load grouping data. Please check your connection and try again.';
      this.dataService.setError(this.error);
      this.loading = false;
      this.dataService.setLoading(false);
    });
  }

  getGroupQualityMessage(score: number): string {
    if (score >= 0.7) return 'The groups are very clearly defined.';
    if (score >= 0.5) return 'The groups are well separated.';
    if (score >= 0.3) return 'The groups have some overlap but are still useful.';
    return 'Groups provide general guidance.';
  }

  getGroupEmoji(index: number): string {
    const emojis = ['🟢', '🔵', '🟠', '🟣', '🔴', '🟡'];
    return emojis[index % emojis.length];
  }

  getGroupType(value: any): string {
    const avgEvents = value?.avg_events || 0;
    const avgParticipants = value?.avg_participants || 0;
    if (avgEvents > 50 || avgParticipants > 100) return 'Very Active';
    if (avgEvents > 20 || avgParticipants > 40) return 'Active';
    if (avgEvents > 10 || avgParticipants > 20) return 'Moderately Active';
    return 'Growing';
  }

  getClusterSize(value: any): number {
    return value && value.size ? value.size : 0;
  }

  getClusterAvgEvents(value: any): string {
    return value && value.avg_events ? Number(value.avg_events).toFixed(1) : '0.0';
  }

  getClusterAvgParticipants(value: any): string {
    return value && value.avg_participants ? Number(value.avg_participants).toFixed(1) : '0.0';
  }

  getClusterUnits(value: any): string {
    return value && value.units ? (Array.isArray(value.units) ? value.units.join(', ') : '') : '';
  }
}
