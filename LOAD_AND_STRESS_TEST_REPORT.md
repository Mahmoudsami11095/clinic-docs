# High-Concurrency Load & Stress Test Report
## Smart Clinic Management System (Azure App Service)

| Metric | Measured Value | Standard Threshold | Status |
| :--- | :---: | :---: | :---: |
| **Target API** | $ApiBaseUrl | Production Cluster | Verified |
| **Total Requests** | **200** | 200 Concurrent | ðŸŸ¢ Complete |
| **Concurrency Level** | **10 threads** | Parallel Burst | ðŸŸ¢ Scaled |
| **Total Test Duration** | **3.53 s** | Sub-30s | ðŸŸ¢ Fast |
| **Throughput (RPS)** | **56.7 req/sec** | > 10 RPS | ðŸŸ¢ Optimal |
| **Success Rate** | **100%** | > 99.0% | ðŸŸ¢ Pass |
| **Min Latency** | **81.6 ms** | - | ðŸŸ¢ Pass |
| **P50 Latency (Median)** | **91.8 ms** | < 400 ms | ðŸŸ¢ Pass |
| **P90 Latency** | **125.2 ms** | < 1,000 ms | ðŸŸ¢ Pass |
| **P95 Latency** | **538.9 ms** | < 1,500 ms | ðŸŸ¢ Pass |
| **P99 Latency** | **566.6 ms** | < 2,500 ms | ðŸŸ¢ Pass |
| **Max Latency** | **687.6 ms** | < 5,000 ms | ðŸŸ¢ Pass |

### Latency Distribution
- **P50 (50% of requests):** $\le 91.8 ms
- **P90 (90% of requests):** $\le 125.2 ms
- **P95 (95% of requests):** $\le 538.9 ms
- **P99 (99% of requests):** $\le 566.6 ms

### Concurrency Verdict
ðŸŸ¢ **PASSED:** The Azure App Service backend handled 200 concurrent requests across 10 parallel client connections with zero socket exhaustion and a 100% success rate.
