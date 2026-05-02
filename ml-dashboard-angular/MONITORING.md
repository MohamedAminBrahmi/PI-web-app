# ML Dashboard Monitoring System

## Overview

This is a production-like monitoring system for the ML Dashboard built with **Prometheus**, **Grafana**, and **Alertmanager**. It provides real-time visibility into API performance, model health, and data quality.

## Architecture

```
┌─────────────────┐
│   FastAPI       │──────┐
│   Backend       │      │  Exposes /metrics (Prometheus format)
│   (Port 8000)   │      │
└─────────────────┘      │
                         │
                    ┌────▼─────────┐
                    │ Prometheus   │  Scrapes metrics every 15s
                    │ (Port 9090)  │  Evaluates alerting rules
                    └────┬─────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼──────┐  ┌──────▼────────┐  ┌────▼─────────────┐
   │  Grafana  │  │  AlertManager │  │  Alert Rules    │
   │ (Port3000)│  │  (Port 9093)  │  │ (Thresholds)    │
   └───────────┘  └───────────────┘  └─────────────────┘
```

## Components

### 1. Prometheus
- **Scrapes** metrics from FastAPI `/metrics` endpoint every 15 seconds
- **Stores** metrics in time-series database
- **Evaluates** alerting rules every 30 seconds
- **Web UI**: http://localhost:9090

### 2. Grafana
- **Visualizes** metrics in interactive dashboards
- **Tracks** API performance, model health, data quality
- **Default Credentials**: admin / admin
- **Web UI**: http://localhost:3000

### 3. AlertManager
- **Routes** alerts based on severity
- **Sends** notifications for critical issues
- **Web UI**: http://localhost:9093

### 4. FastAPI Instrumentation
- **Prometheus middleware** for automatic request tracking
- **Custom metrics** for model predictions and drift detection
- **Health endpoint** (`/health`) for system status

## Monitoring Metrics

### API Performance
- **Requests/sec**: Request volume evolution
- **Latency (p50, p95, p99)**: Response time percentiles
- **Error Rate**: Percentage of failed requests
- **Request Size/Response Size**: Payload metrics

### Model Health
- **Accuracy**: Model accuracy vs baseline
- **Precision/Recall**: Classification metrics
- **Prediction Confidence**: Average confidence score
- **Confidence Deviation**: From baseline threshold

### Data Quality
- **Missing Values %**: Data completeness
- **Data Freshness**: Age of data in hours
- **Data Drift**: Feature distribution shifts
- **Model Drift**: Prediction pattern changes

### System Health
- **Active Requests**: Concurrent request count
- **System Errors**: Exception and error counts
- **Error Rate Trend**: Error percentage over time

## Alerting Rules

### Critical Alerts
- **High Error Rate**: >5% request errors
- **API Down**: Service unavailable for >1 minute
- **High System Errors**: >5 errors in 5 minutes

### Warning Alerts
- **High API Latency**: p95 latency >1.0 second
- **Accuracy Degradation**: >5% drop from baseline
- **Confidence Drop**: Significant confidence reduction
- **Data Drift**: Feature distribution shift detected
- **Model Drift**: Prediction pattern change
- **High Missing Values**: >10% missing data
- **Stale Data**: Data older than 24 hours
- **High Active Requests**: >100 concurrent requests

## Getting Started

### 1. Start Services with Docker Compose

```bash
docker-compose up -d
```

Wait for all services to be healthy (20-30 seconds):
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- AlertManager: http://localhost:9093

### 2. Verify Prometheus Scraping

Visit http://localhost:9090/targets and confirm backend target shows "UP"

### 3. Access Grafana Dashboard

```
URL: http://localhost:3000
Username: admin
Password: admin
```

The "ML Dashboard - Production Monitoring" dashboard should be available automatically.

### 4. Run Monitoring Simulation

```bash
# Full scenario (all tests in sequence)
cd backend
python simulate_monitoring.py

# Or run specific scenario
python simulate_monitoring.py --scenario traffic --duration 30
python simulate_monitoring.py --scenario errors --duration 30
python simulate_monitoring.py --scenario drift --duration 30
```

### 5. Monitor Simulation Results

- **Watch Grafana dashboards** as simulation runs
- **Check Alert Manager**: http://localhost:9093
- **View Prometheus metrics**: http://localhost:9090/graph

## Simulation Scenarios

### Scenario 1: Normal Baseline (120s)
- **What**: 2 requests/second at normal feature values
- **Expected**: Stable latency, accuracy, confidence
- **Watch**: Request rate and error rate panels

### Scenario 2: High Traffic (30s)
- **What**: 15 requests/second spike
- **Expected**: Latency increase, queue buildup
- **Watch**: Latency percentiles, active requests
- **Alert**: Possible high latency warning

### Scenario 3: API Errors (30s)
- **What**: 40% invalid requests sent
- **Expected**: Error rate spike, failed predictions
- **Watch**: Error rate and system errors
- **Alert**: High error rate critical alert

### Scenario 4: Model Drift - Mild (30s)
- **What**: Features shifted outside normal range
- **Expected**: Accuracy drop, confidence reduction
- **Watch**: Accuracy deviation, prediction confidence
- **Alert**: Accuracy degradation warning

### Scenario 5: Model Drift - Moderate (30s)
- **What**: More severe feature shifts
- **Expected**: Significant accuracy loss
- **Watch**: Drift detection metrics
- **Alert**: Model drift and accuracy alerts

### Scenario 6: Recovery (60s)
- **What**: Return to normal traffic
- **Expected**: Metrics normalize, alerts clear
- **Watch**: Recovery patterns

## Drift Detection

### Methods
- **Univariate Drift**: Individual feature distribution changes (KS test, Hellinger distance)
- **Multivariate Drift**: Multiple feature correlation changes
- **Prediction Drift**: Confidence and accuracy pattern changes

### Thresholds
- **Data Drift**: Distribution shift score > 0.3
- **Model Drift**: Drift score > 0.3
- **Accuracy Drop**: <95% of baseline (5% threshold)
- **Confidence Drop**: <95% of baseline

### Detection Logic
```python
# Example drift detection
if accuracy < baseline * 0.95:
    trigger_accuracy_degradation_alert()
    
if feature_ks_test_statistic > 0.3:
    trigger_data_drift_alert()
```

## Key Metrics Explained

### Latency Percentiles
- **p50**: 50% of requests respond faster than this
- **p95**: 95% of requests respond faster than this (SLA target)
- **p99**: 99% of requests respond faster than this

### Error Rate
- **Definition**: (Failed Requests) / (Total Requests) × 100%
- **Alert Threshold**: >5% (critical)
- **Indicates**: Service reliability issues

### Accuracy vs Baseline
- **Calculation**: ((Current Accuracy - Baseline) / Baseline) × 100%
- **Alert Threshold**: <-5% (warning)
- **Indicates**: Model performance degradation

### Data Drift Score
- **Range**: 0.0 to 1.0
- **0.0-0.2**: No drift
- **0.2-0.5**: Minor drift
- **0.5-1.0**: Significant drift
- **Alert Threshold**: >0.3

## Observability Levels

### Metrics (What Happens)
- Request counts, latencies, error rates
- Model accuracy, confidence, precision/recall
- Data quality metrics, drift scores
- System resource usage

### Logs (Why It Happens)
- Request errors and exceptions
- Model retraining triggers
- Drift detection events
- Alert trigger events

### Traces (How It Happens)
- Request flow from API to model
- Feature preprocessing steps
- Model inference pipeline
- Data validation steps

## Advanced Configuration

### Custom Alert Rules
Edit `monitoring/alert_rules.yml` to add custom rules:

```yaml
- alert: CustomAlert
  expr: your_metric > threshold
  for: duration
  labels:
    severity: critical
  annotations:
    summary: "Alert description"
```

### Dashboard Customization
- Login to Grafana
- Edit "ML Dashboard - Production Monitoring"
- Add/remove panels, adjust thresholds
- Save changes

### Prometheus Retention
Edit `docker-compose.yml` Prometheus command:
```yaml
command:
  - '--storage.tsdb.retention.time=30d'
```

## Troubleshooting

### Prometheus not scraping metrics
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Verify backend is running
curl http://localhost:8000/metrics
```

### Grafana shows no data
1. Wait 2-3 minutes for Prometheus to scrape data
2. Check Grafana datasource: Settings > Data Sources > Prometheus
3. Click "Test" to verify connection

### Alerts not firing
1. Check AlertManager: http://localhost:9093
2. Verify alert rules: http://localhost:9090/alerts
3. Check FastAPI metrics are being recorded: http://localhost:8000/metrics

### High memory usage
- Reduce Prometheus retention time
- Reduce scrape interval in prometheus.yml
- Clean old volumes: `docker volume prune`

## Next Steps

1. **Integrate with Slack/Email**: Configure AlertManager webhook
2. **Add Custom Dashboards**: Create domain-specific visualizations
3. **Implement Auto-Scaling**: Use metrics to trigger scaling
4. **Setup Logging**: Add ELK or Loki for log aggregation
5. **Performance Tuning**: Optimize alert rules and thresholds

## Documentation Links

- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)
- [AlertManager Docs](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/instrumentation/)

## Support

For issues or questions:
1. Check Prometheus targets: http://localhost:9090/targets
2. Review alert rules: http://localhost:9090/alerts
3. Check FastAPI logs: `docker logs ml-dashboard-backend`
4. View Grafana dashboards for anomalies
