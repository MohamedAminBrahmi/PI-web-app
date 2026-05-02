import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OverviewComponent } from './components/overview.component';
import { ClassificationComponent } from './components/classification.component';
import { RegressionComponent } from './components/regression.component';
import { ClusteringComponent } from './components/clustering.component';
import { ForecastingComponent } from './components/forecasting.component';
import { PredictionComponent } from './components/prediction.component';

const routes: Routes = [
  { path: '', redirectTo: '/overview', pathMatch: 'full' },
  { path: 'overview', component: OverviewComponent },
  { path: 'classification', component: ClassificationComponent },
  { path: 'regression', component: RegressionComponent },
  { path: 'clustering', component: ClusteringComponent },
  { path: 'forecasting', component: ForecastingComponent },
  { path: 'prediction', component: PredictionComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
