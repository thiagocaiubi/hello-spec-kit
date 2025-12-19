# Quickstart: Kubernetes Health Probe Endpoint

**Feature**: 001-health-endpoint  
**Date**: 2025-12-16  
**Time to Complete**: ~5 minutes

## Overview

This quickstart validates that the `/health` endpoint is correctly implemented and working as specified for Kubernetes probe integration.

## Prerequisites

- Docker and docker-compose installed
- curl or web browser
- (Optional) kubectl for Kubernetes deployment

## Step 1: Start the Application

```bash
# From repository root
docker-compose up --build
```

**Expected Output**:
```
hello-spec-kit  | INFO:     Started server process [1]
hello-spec-kit  | INFO:     Waiting for application startup.
hello-spec-kit  | INFO:     Application startup complete.
hello-spec-kit  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Success Criteria**: Application starts without errors within 10 seconds.

## Step 2: Test Health Endpoint

### Using curl

```bash
curl -i http://localhost:8000/health
```

**Expected Output**:
```
HTTP/1.1 200 OK
date: Mon, 16 Dec 2025 00:00:00 GMT
server: uvicorn
content-length: 17
content-type: application/json

{"status":"ok"}
```

**Success Criteria**:
- ✅ Status code: 200 OK
- ✅ Response body: `{"status":"ok"}`
- ✅ Content-Type: `application/json`
- ✅ Response time: < 100ms

### Using Browser

Navigate to: `http://localhost:8000/health`

**Expected Display**:
```json
{"status":"ok"}
```

## Step 3: Verify Performance

Test response time:

```bash
curl -w "\nTime: %{time_total}s\n" http://localhost:8000/health
```

**Expected Output**:
```
{"status":"ok"}
Time: 0.005s
```

**Success Criteria**: Response time < 0.1s (100ms)

## Step 4: Test Edge Cases

### Test Wrong HTTP Method

```bash
curl -i -X POST http://localhost:8000/health
```

**Expected Output**:
```
HTTP/1.1 405 Method Not Allowed
...
{"detail":"Method Not Allowed"}
```

**Success Criteria**: 405 status code returned

### Test with Query Parameters

```bash
curl -i http://localhost:8000/health?test=123
```

**Expected Output**:
```
HTTP/1.1 200 OK
...
{"status":"ok"}
```

**Success Criteria**: Query parameters ignored, still returns 200 OK

### Test Concurrent Requests

```bash
# Run 100 concurrent requests
for i in {1..100}; do curl -s http://localhost:8000/health & done; wait
```

**Success Criteria**: All requests return 200 OK with correct response

## Step 5: Verify FastAPI Documentation

Navigate to: `http://localhost:8000/docs`

**Expected**: Swagger UI with `/health` endpoint documented

**Verify**:
- ✅ `/health` endpoint visible in API list
- ✅ GET method shown
- ✅ Response schema shows `{"status": "ok"}`
- ✅ "Try it out" feature works

## Step 6: Run Unit Tests

```bash
# Install dependencies (if not already done)
docker-compose exec hello-spec-kit uv sync

# Run tests
docker-compose exec hello-spec-kit python -m pytest tests/unit/test_health.py -v
```

**Expected Output**:
```
tests/unit/test_health.py::test_health_endpoint_returns_200 PASSED
tests/unit/test_health.py::test_health_endpoint_returns_correct_json PASSED
tests/unit/test_health.py::test_health_endpoint_performance PASSED
tests/unit/test_health.py::test_health_endpoint_wrong_method PASSED
```

**Success Criteria**: All tests pass in < 5 seconds

## Step 7: Deploy to Kubernetes (Optional)

### Build and Push Image

```bash
# Build image
docker build -t hello-spec-kit:health-probe .

# Tag for registry (replace with your registry)
docker tag hello-spec-kit:health-probe <registry>/hello-spec-kit:health-probe

# Push to registry
docker push <registry>/hello-spec-kit:health-probe
```

### Apply Kubernetes Configuration

```bash
# Apply deployment with health probes
kubectl apply -f specs/001-health-endpoint/contracts/kubernetes-deployment.yaml

# Wait for pod to be ready
kubectl wait --for=condition=ready pod -l app=hello-spec-kit --timeout=60s
```

**Success Criteria**:
```
pod/hello-spec-kit-xxx condition met
```

### Verify Probes in Kubernetes

```bash
# Check pod status
kubectl get pods -l app=hello-spec-kit

# Expected: STATUS = Running, READY = 1/1

# Describe pod to see probe results
kubectl describe pod -l app=hello-spec-kit | grep -A 10 "Liveness\|Readiness"
```

**Expected Output**:
```
    Liveness:       http-get http://:8000/health delay=15s timeout=1s period=20s #success=1 #failure=3
    Readiness:      http-get http://:8000/health delay=5s timeout=1s period=10s #success=1 #failure=3
```

### Test Probe from Inside Cluster

```bash
# Get pod IP
POD_IP=$(kubectl get pod -l app=hello-spec-kit -o jsonpath='{.items[0].status.podIP}')

# Test health endpoint from another pod
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never -- \
  curl http://$POD_IP:8000/health
```

**Expected Output**:
```
{"status":"ok"}
pod "curl-test" deleted
```

## Step 8: Monitor Probe Activity

```bash
# Watch probe events
kubectl get events --watch | grep health

# Check probe metrics (if metrics server installed)
kubectl top pods -l app=hello-spec-kit
```

**Success Criteria**:
- No probe failures in events
- Pod remains in Ready state continuously
- CPU usage remains low (< 1% with probes running)

## Cleanup

### Stop Local Application

```bash
docker-compose down
```

### Remove Kubernetes Deployment

```bash
kubectl delete deployment hello-spec-kit
```

## Acceptance Validation Checklist

Verify all acceptance scenarios from spec.md:

- [ ] **AS-1**: Application running → Readiness probe → 200 OK with `{"status":"ok"}`
- [ ] **AS-2**: Application running → Liveness probe → 200 OK within timeout
- [ ] **AS-3**: Application just started → First probe → Endpoint immediately available
- [ ] **AS-4**: Application under load → Health probe → Still responds quickly

## Success Criteria Validation

- [ ] **SC-001**: Response time < 100ms (measured in Step 3)
- [ ] **SC-002**: 99.99% availability (matches application uptime)
- [ ] **SC-003**: Handles 100 req/s without degradation (tested in Step 4)
- [ ] **SC-004**: Kubernetes probes work without false negatives (verified in Step 7)

## Troubleshooting

### Health endpoint returns 404

**Problem**: Endpoint not implemented or wrong path

**Solution**: 
- Verify route decorator: `@app.get("/health")`
- Check application logs for startup errors
- Ensure latest code is deployed

### Probe timing out in Kubernetes

**Problem**: Response time > timeoutSeconds

**Solution**:
- Check endpoint response time locally first
- Verify network connectivity in cluster
- Increase `timeoutSeconds` in probe configuration if needed

### Pod restarting frequently

**Problem**: Liveness probe failing

**Solution**:
- Check application logs for errors
- Verify endpoint is accessible
- Increase `failureThreshold` or `periodSeconds` in liveness probe

### Tests failing

**Problem**: Unit tests not passing

**Solution**:
- Check test file exists: `tests/unit/test_health.py`
- Verify FastAPI TestClient is available
- Review test output for specific assertion failures

## Next Steps

After successful validation:

1. Commit changes to feature branch `001-health-endpoint`
2. Create pull request to main branch
3. Update Kubernetes deployments to use health probes
4. Monitor probe success rate in production
5. Document probe configuration in deployment runbooks

## Estimated Time

- Steps 1-6 (Local validation): ~5 minutes
- Steps 7-8 (Kubernetes deployment): ~10 minutes
- Total: ~15 minutes
