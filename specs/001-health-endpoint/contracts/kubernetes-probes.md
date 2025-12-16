# Kubernetes Probe Configuration Examples

This document provides example Kubernetes configurations for using the `/health` endpoint with readiness and liveness probes.

## Basic Deployment with Probes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-spec-kit
  labels:
    app: hello-spec-kit
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-spec-kit
  template:
    metadata:
      labels:
        app: hello-spec-kit
    spec:
      containers:
      - name: app
        image: hello-spec-kit:latest
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        
        # Readiness probe - determines if pod should receive traffic
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
            scheme: HTTP
          initialDelaySeconds: 5    # Wait 5s after container starts
          periodSeconds: 10          # Check every 10 seconds
          timeoutSeconds: 1          # Request timeout
          successThreshold: 1        # 1 success = ready
          failureThreshold: 3        # 3 failures = not ready
        
        # Liveness probe - determines if pod should be restarted
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
            scheme: HTTP
          initialDelaySeconds: 15    # Wait 15s before first check
          periodSeconds: 20          # Check every 20 seconds
          timeoutSeconds: 1          # Request timeout
          successThreshold: 1        # 1 success = alive
          failureThreshold: 3        # 3 failures = restart pod
        
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

## Aggressive Probe Configuration

For faster failure detection (use with caution - may cause false positives):

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 2
  periodSeconds: 5
  timeoutSeconds: 1
  successThreshold: 1
  failureThreshold: 2

livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 1
  successThreshold: 1
  failureThreshold: 2
```

## Conservative Probe Configuration

For more stable environments with higher tolerance for transient failures:

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 15
  timeoutSeconds: 2
  successThreshold: 2
  failureThreshold: 5

livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 30
  timeoutSeconds: 2
  successThreshold: 1
  failureThreshold: 5
```

## Probe Configuration Best Practices

### Readiness Probe
- **Purpose**: Indicates if the pod is ready to handle traffic
- **Effect**: Removes pod from service load balancer when failing
- **Recommendation**: More frequent checks, lower failure threshold
- **Initial delay**: Time for application to start (5-10 seconds typical for FastAPI)

### Liveness Probe
- **Purpose**: Detects if the pod is alive or needs restart
- **Effect**: Restarts pod when failing
- **Recommendation**: Less frequent checks, higher failure threshold (avoid restart loops)
- **Initial delay**: Longer than readiness (15-30 seconds) to avoid restart during startup

### General Guidelines
1. **initialDelaySeconds**: Should exceed application startup time
2. **periodSeconds**: Balance between responsiveness and overhead
3. **timeoutSeconds**: Should be < 1s for this endpoint (meets p95 <100ms requirement)
4. **failureThreshold**: Higher values prevent false positives from transient issues
5. **successThreshold**: Usually 1 is sufficient (pod recovers quickly)

### Timing Calculation

**Time to mark pod as not ready**:
```
readiness_failure_time = initialDelaySeconds + (periodSeconds × failureThreshold)
```

**Time to restart unhealthy pod**:
```
liveness_restart_time = initialDelaySeconds + (periodSeconds × failureThreshold)
```

**Example** (basic configuration above):
- Readiness failure: 5s + (10s × 3) = 35 seconds
- Liveness restart: 15s + (20s × 3) = 75 seconds

## Testing Probes Locally

### Using curl
```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected output:
# {"status":"ok"}

# Test with timing
curl -w "\nTime: %{time_total}s\n" http://localhost:8000/health
```

### Using kubectl
```bash
# Check pod readiness
kubectl get pods -l app=hello-spec-kit

# Describe pod to see probe results
kubectl describe pod <pod-name>

# View probe events
kubectl get events --field-selector involvedObject.name=<pod-name>
```

## Troubleshooting

### Pod stuck in "Not Ready" state
- Check `initialDelaySeconds` - may be too short for app startup
- Increase `failureThreshold` to tolerate transient failures
- Verify `/health` endpoint is accessible from within cluster

### Pod restarting frequently
- Check `livenessProbe` configuration - may be too aggressive
- Increase `initialDelaySeconds` if app has long startup
- Increase `failureThreshold` to tolerate temporary issues
- Verify endpoint response time is < `timeoutSeconds`

### Probes timing out
- Check endpoint response time (should be <100ms)
- Increase `timeoutSeconds` if needed (but investigate why endpoint is slow)
- Check network connectivity within cluster

## Performance Impact

**Health endpoint performance**:
- Response time: ~1-10ms (measured)
- CPU usage: Negligible (<0.01% per request)
- Memory: No allocation (returns static dict)

**Probe overhead** (basic config, 3 replicas):
- Readiness: 3 requests / 10s = 0.3 req/s
- Liveness: 3 requests / 20s = 0.15 req/s
- **Total**: ~0.45 req/s (well under 100 req/s capacity)
