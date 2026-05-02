"""
Monitoring System Simulation Script
Simulates production scenarios: high traffic, errors, and model drift
"""
import requests
import time
import random
import json
import numpy as np
from datetime import datetime
from typing import Dict
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoringSimulator:
    """Simulates production scenarios for monitoring testing."""
    
    def __init__(self, api_url: str = "http://localhost:8000", batch_size: int = 10):
        self.api_url = api_url
        self.batch_size = batch_size
        self.session = requests.Session()
        
    def simulate_normal_traffic(self, duration_seconds: int = 60, requests_per_second: float = 2.0):
        """Simulate normal API traffic."""
        logger.info(f"Simulating normal traffic ({requests_per_second} req/s) for {duration_seconds}s...")
        
        start_time = time.time()
        request_count = 0
        errors = 0
        
        while time.time() - start_time < duration_seconds:
            try:
                # Make prediction request
                features = {
                    "feature_1": np.random.uniform(18, 65),
                    "feature_2": np.random.uniform(5, 120),
                    "feature_3": np.random.uniform(100, 5000),
                    "feature_4": np.random.uniform(50, 2000),
                    "feature_5": np.random.uniform(0, 1)
                }
                
                response = self.session.post(
                    f"{self.api_url}/api/v1/prediction/predict",
                    json={"features": features, "model_type": "classification"},
                    timeout=5
                )
                
                if response.status_code == 200:
                    request_count += 1
                    logger.info(f"✓ Request {request_count}: {response.status_code}")
                else:
                    errors += 1
                    logger.warning(f"✗ Request failed: {response.status_code}")
                
            except Exception as e:
                errors += 1
                logger.error(f"✗ Request error: {e}")
            
            # Control request rate
            time.sleep(1 / requests_per_second)
        
        elapsed = time.time() - start_time
        logger.info(f"✓ Completed: {request_count} successful requests, {errors} errors in {elapsed:.1f}s")
        logger.info(f"  Error rate: {(errors / (request_count + errors) * 100):.2f}%")
        
        return request_count, errors
    
    def simulate_high_traffic(self, duration_seconds: int = 30, requests_per_second: float = 10.0):
        """Simulate high traffic spike."""
        logger.info(f"Simulating HIGH TRAFFIC ({requests_per_second} req/s) for {duration_seconds}s...")
        logger.warning("⚠️  Watch for latency spikes in Grafana!")
        
        return self.simulate_normal_traffic(duration_seconds, requests_per_second)
    
    def simulate_api_errors(self, duration_seconds: int = 30, error_rate: float = 0.3):
        """Simulate API errors."""
        logger.info(f"Simulating API ERRORS ({error_rate*100}% error rate) for {duration_seconds}s...")
        logger.warning("⚠️  Watch for error rate spikes in Grafana!")
        
        start_time = time.time()
        request_count = 0
        errors = 0
        
        while time.time() - start_time < duration_seconds:
            try:
                # Randomly decide if this request should fail
                should_fail = random.random() < error_rate
                
                if should_fail:
                    # Send invalid request
                    response = self.session.post(
                        f"{self.api_url}/api/v1/prediction/predict",
                        json={"invalid": "data"},  # Invalid payload
                        timeout=5
                    )
                else:
                    features = {
                        "feature_1": np.random.uniform(18, 65),
                        "feature_2": np.random.uniform(5, 120),
                        "feature_3": np.random.uniform(100, 5000),
                        "feature_4": np.random.uniform(50, 2000),
                        "feature_5": np.random.uniform(0, 1)
                    }
                    response = self.session.post(
                        f"{self.api_url}/api/v1/prediction/predict",
                        json={"features": features, "model_type": "classification"},
                        timeout=5
                    )
                
                if response.status_code == 200:
                    request_count += 1
                    logger.info(f"✓ Request {request_count}: {response.status_code}")
                else:
                    errors += 1
                    logger.warning(f"✗ Request failed: {response.status_code}")
                
            except Exception as e:
                errors += 1
                logger.error(f"✗ Request error: {e}")
            
            time.sleep(0.5)
        
        elapsed = time.time() - start_time
        actual_error_rate = (errors / (request_count + errors) * 100) if (request_count + errors) > 0 else 0
        logger.info(f"✓ Completed: {request_count} requests, {errors} errors")
        logger.info(f"  Actual error rate: {actual_error_rate:.2f}%")
        
        return request_count, errors
    
    def simulate_model_drift(self, duration_seconds: int = 30, severity: str = "mild"):
        """
        Simulate model drift by sending feature values outside normal distribution.
        
        Args:
            severity: 'mild', 'moderate', or 'severe'
        """
        logger.info(f"Simulating MODEL DRIFT ({severity} severity) for {duration_seconds}s...")
        logger.warning("⚠️  Watch for accuracy degradation and confidence drops in Grafana!")
        
        # Define drift parameters based on severity
        drift_params = {
            "mild": {"feature_shifts": 2, "confidence_reduction": 0.05},
            "moderate": {"feature_shifts": 3.5, "confidence_reduction": 0.15},
            "severe": {"feature_shifts": 5, "confidence_reduction": 0.3}
        }
        
        params = drift_params.get(severity, drift_params["mild"])
        
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < duration_seconds:
            try:
                # Generate shifted features (outside normal distribution)
                features = {
                    "feature_1": np.random.uniform(75, 100),  # Shifted from normal (18-65)
                    "feature_2": np.random.uniform(150, 250),  # Shifted from normal (5-120)
                    "feature_3": np.random.uniform(8000, 15000),  # Shifted from normal (100-5000)
                    "feature_4": np.random.uniform(3000, 5000),  # Shifted from normal (50-2000)
                    "feature_5": np.random.uniform(0, 1)
                }
                
                response = self.session.post(
                    f"{self.api_url}/api/v1/prediction/predict",
                    json={"features": features, "model_type": "classification"},
                    timeout=5
                )
                
                if response.status_code == 200:
                    request_count += 1
                    logger.info(f"✓ Drift request {request_count}: {response.status_code}")
                
            except Exception as e:
                logger.error(f"✗ Drift request error: {e}")
            
            time.sleep(1)
        
        logger.info(f"✓ Completed: {request_count} drift simulation requests")
        return request_count
    
    def check_system_health(self) -> Dict:
        """Check system health via health endpoint."""
        try:
            response = self.session.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                logger.info(f"System Health: {health['status']}")
                logger.info(f"  Error Rate: {health['error_rate']}")
                logger.info(f"  Total Requests: {health['total_requests']}")
                logger.info(f"  Total Errors: {health['total_errors']}")
                return health
        except Exception as e:
            logger.error(f"Health check failed: {e}")
        return {}
    
    def get_drift_summary(self) -> Dict:
        """Get current drift detection summary."""
        try:
            response = self.session.get(f"{self.api_url}/api/v1/monitoring/drift-summary", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Drift summary retrieval failed: {e}")
        return {}
    
    def run_full_simulation(self):
        """Run complete monitoring simulation scenario."""
        logger.info("\n" + "="*80)
        logger.info("ML DASHBOARD MONITORING SIMULATION")
        logger.info("="*80 + "\n")
        
        logger.info("Step 1: Normal traffic baseline (120s)")
        logger.info("  → Watch Request Rate and Error Rate panels")
        self.simulate_normal_traffic(duration_seconds=120, requests_per_second=2.0)
        self.check_system_health()
        time.sleep(5)
        
        logger.info("\nStep 2: High traffic spike (30s)")
        logger.info("  → Watch for Latency increase in the API Latency panel")
        self.simulate_high_traffic(duration_seconds=30, requests_per_second=15.0)
        self.check_system_health()
        time.sleep(5)
        
        logger.info("\nStep 3: API errors simulation (30s)")
        logger.info("  → Watch Error Rate panel spike")
        self.simulate_api_errors(duration_seconds=30, error_rate=0.4)
        self.check_system_health()
        time.sleep(5)
        
        logger.info("\nStep 4: Model drift - Mild (30s)")
        logger.info("  → Watch for feature distribution shifts and confidence drops")
        self.simulate_model_drift(duration_seconds=30, severity="mild")
        drift_info = self.get_drift_summary()
        if drift_info:
            logger.info(f"  Drift Detection Results: {json.dumps(drift_info, indent=2)}")
        time.sleep(5)
        
        logger.info("\nStep 5: Model drift - Moderate (30s)")
        self.simulate_model_drift(duration_seconds=30, severity="moderate")
        drift_info = self.get_drift_summary()
        if drift_info:
            logger.info(f"  Drift Detection Results: {json.dumps(drift_info, indent=2)}")
        time.sleep(5)
        
        logger.info("\nStep 6: Recovery - Normal traffic (60s)")
        logger.info("  → Watch metrics return to normal")
        self.simulate_normal_traffic(duration_seconds=60, requests_per_second=3.0)
        self.check_system_health()
        
        logger.info("\n" + "="*80)
        logger.info("SIMULATION COMPLETE!")
        logger.info("="*80)
        logger.info("\n📊 Check Grafana at http://localhost:3000")
        logger.info("   Username: admin")
        logger.info("   Password: admin")
        logger.info("\n✅ All scenarios have been executed. Check the dashboards for:")
        logger.info("   - Traffic patterns and request rates")
        logger.info("   - Latency increase during high traffic")
        logger.info("   - Error rate spikes during fault injection")
        logger.info("   - Accuracy and confidence degradation during drift")
        logger.info("   - Recovery patterns after incidents")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="ML Dashboard Monitoring Simulator")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--scenario", default="full", 
                       choices=["full", "traffic", "errors", "drift"],
                       help="Simulation scenario to run")
    parser.add_argument("--duration", type=int, default=30, help="Duration in seconds")
    args = parser.parse_args()
    
    simulator = MonitoringSimulator(api_url=args.api_url)
    
    if args.scenario == "full":
        simulator.run_full_simulation()
    elif args.scenario == "traffic":
        simulator.simulate_high_traffic(duration_seconds=args.duration)
    elif args.scenario == "errors":
        simulator.simulate_api_errors(duration_seconds=args.duration)
    elif args.scenario == "drift":
        simulator.simulate_model_drift(duration_seconds=args.duration, severity="moderate")


if __name__ == "__main__":
    main()
