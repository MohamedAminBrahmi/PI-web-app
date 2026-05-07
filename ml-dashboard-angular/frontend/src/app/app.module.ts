import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { HomeComponent } from './components/home.component';
import { OverviewComponent } from './components/overview.component';
import { ClassificationComponent } from './components/classification.component';
import { RegressionComponent } from './components/regression.component';
import { ClusteringComponent } from './components/clustering.component';
import { ForecastingComponent } from './components/forecasting.component';
import { PredictionComponent } from './components/prediction.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    OverviewComponent,
    ClassificationComponent,
    RegressionComponent,
    ClusteringComponent,
    ForecastingComponent,
    PredictionComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
