# Deployment Guide

This guide covers different deployment options for the OUNASS Pod Forecasting API.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Local Development

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Google Sheets API credentials (see GOOGLE_SHEETS_SETUP.md)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sorted78/ounass-api.git
   cd ounass-api
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Google Sheets credentials
   ```

5. **Run the application:**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/api/v1/health

---

## Docker Deployment

### Build and Run with Docker

1. **Build the Docker image:**
   ```bash
   docker build -t ounass-api:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name ounass-api \
     -p 8000:8000 \
     -v $(pwd)/credentials.json:/app/credentials.json \
     -v $(pwd)/.env:/app/.env \
     -v $(pwd)/logs:/app/logs \
     ounass-api:latest
   ```

3. **Check container logs:**
   ```bash
   docker logs -f ounass-api
   ```

4. **Stop the container:**
   ```bash
   docker stop ounass-api
   docker rm ounass-api
   ```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    image: ounass-api:latest
    container_name: ounass-api
    ports:
      - "8000:8000"
    volumes:
      - ./credentials.json:/app/credentials.json:ro
      - ./.env:/app/.env:ro
      - ./logs:/app/logs
    environment:
      - LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Run with Docker Compose:**
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## Production Deployment

### AWS EC2 Deployment

1. **Launch EC2 Instance:**
   - Instance type: t3.small or larger
   - OS: Ubuntu 22.04 LTS
   - Security group: Allow inbound on port 8000

2. **Connect and setup:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   ```

3. **Deploy application:**
   ```bash
   # Clone repository
   git clone https://github.com/sorted78/ounass-api.git
   cd ounass-api
   
   # Copy credentials
   # Upload your credentials.json and .env files
   
   # Run with Docker
   docker build -t ounass-api:latest .
   docker run -d \
     --name ounass-api \
     -p 8000:8000 \
     -v $(pwd)/credentials.json:/app/credentials.json:ro \
     -v $(pwd)/.env:/app/.env:ro \
     -v $(pwd)/logs:/app/logs \
     --restart unless-stopped \
     ounass-api:latest
   ```

4. **Setup reverse proxy with Nginx (optional):**
   ```bash
   sudo apt install nginx -y
   
   # Create Nginx config
   sudo nano /etc/nginx/sites-available/ounass-api
   ```

   Add configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Enable and restart:
   ```bash
   sudo ln -s /etc/nginx/sites-available/ounass-api /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Environment Variables for Production

Update `.env` for production:
```env
GOOGLE_SHEET_ID=your_production_sheet_id
GOOGLE_CREDENTIALS_PATH=/app/credentials.json
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=WARNING
MODEL_RETRAIN_INTERVAL_DAYS=7
```

---

## Kubernetes Deployment

### Kubernetes Manifests

1. **Create namespace:**
   ```yaml
   # namespace.yaml
   apiVersion: v1
   kind: Namespace
   metadata:
     name: ounass-forecasting
   ```

2. **Create secret for credentials:**
   ```bash
   kubectl create secret generic google-credentials \
     --from-file=credentials.json=./credentials.json \
     -n ounass-forecasting
   ```

3. **Create ConfigMap:**
   ```yaml
   # configmap.yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: ounass-api-config
     namespace: ounass-forecasting
   data:
     GOOGLE_SHEET_ID: "your_sheet_id"
     API_HOST: "0.0.0.0"
     API_PORT: "8000"
     LOG_LEVEL: "INFO"
   ```

4. **Create Deployment:**
   ```yaml
   # deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: ounass-api
     namespace: ounass-forecasting
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: ounass-api
     template:
       metadata:
         labels:
           app: ounass-api
       spec:
         containers:
         - name: api
           image: your-registry/ounass-api:latest
           ports:
           - containerPort: 8000
           envFrom:
           - configMapRef:
               name: ounass-api-config
           volumeMounts:
           - name: google-credentials
             mountPath: /app/credentials.json
             subPath: credentials.json
             readOnly: true
           livenessProbe:
             httpGet:
               path: /api/v1/health
               port: 8000
             initialDelaySeconds: 30
             periodSeconds: 30
           readinessProbe:
             httpGet:
               path: /api/v1/health
               port: 8000
             initialDelaySeconds: 10
             periodSeconds: 10
           resources:
             requests:
               memory: "256Mi"
               cpu: "250m"
             limits:
               memory: "512Mi"
               cpu: "500m"
         volumes:
         - name: google-credentials
           secret:
             secretName: google-credentials
   ```

5. **Create Service:**
   ```yaml
   # service.yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: ounass-api-service
     namespace: ounass-forecasting
   spec:
     selector:
       app: ounass-api
     ports:
     - protocol: TCP
       port: 80
       targetPort: 8000
     type: LoadBalancer
   ```

6. **Deploy to Kubernetes:**
   ```bash
   kubectl apply -f namespace.yaml
   kubectl apply -f configmap.yaml
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   
   # Check status
   kubectl get all -n ounass-forecasting
   kubectl logs -f deployment/ounass-api -n ounass-forecasting
   ```

---

## Monitoring and Maintenance

### Health Checks

Set up automated health checks:

```bash
# Cron job for health check (add to crontab)
*/5 * * * * curl -f http://your-api-url/api/v1/health || echo "API health check failed" | mail -s "OUNASS API Alert" admin@example.com
```

### Model Retraining

Schedule automatic model retraining:

```bash
# Weekly retraining (Sunday at 2 AM)
0 2 * * 0 curl -X POST http://your-api-url/api/v1/train
```

### Log Rotation

Configure log rotation in `/etc/logrotate.d/ounass-api`:

```
/path/to/ounass-api/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 root root
    sharedscripts
}
```

### Backup Strategy

1. **Google Sheets**: Already backed up by Google
2. **Trained Models**: Save model files periodically
3. **Application Logs**: Retain for 30 days
4. **Configuration**: Store in version control

### Performance Monitoring

Use monitoring tools:
- **Prometheus + Grafana** for metrics
- **ELK Stack** for log aggregation
- **APM tools** (New Relic, Datadog) for application monitoring

### Security Checklist

- [ ] API authentication enabled
- [ ] HTTPS/TLS configured
- [ ] Credentials stored securely (not in code)
- [ ] Regular security updates
- [ ] Firewall rules configured
- [ ] Rate limiting implemented
- [ ] CORS properly configured
- [ ] Input validation enabled
- [ ] Audit logging enabled

### Scaling Considerations

1. **Horizontal Scaling**: Increase replica count in Kubernetes
2. **Vertical Scaling**: Increase resource limits
3. **Database**: Consider caching layer (Redis) for predictions
4. **Load Balancing**: Use Nginx or cloud load balancer
5. **CDN**: For static content if added

### Troubleshooting

Common issues and solutions:

1. **API not responding:**
   ```bash
   docker logs ounass-api
   # Check for errors in startup
   ```

2. **Google Sheets connection error:**
   - Verify credentials.json is mounted correctly
   - Check service account has sheet access
   - Ensure APIs are enabled in Google Cloud

3. **Model prediction errors:**
   - Retrain the model with latest data
   - Check that budget data exists for requested dates
   - Verify data format in Google Sheets

4. **High memory usage:**
   - Reduce model complexity
   - Implement model caching
   - Increase container memory limits

---

## Update Process

### Rolling Update (Kubernetes)

```bash
# Build new image
docker build -t your-registry/ounass-api:v1.1.0 .
docker push your-registry/ounass-api:v1.1.0

# Update deployment
kubectl set image deployment/ounass-api api=your-registry/ounass-api:v1.1.0 -n ounass-forecasting

# Check rollout status
kubectl rollout status deployment/ounass-api -n ounass-forecasting
```

### Zero-Downtime Update (Docker)

```bash
# Pull new code
git pull origin main

# Build new image
docker build -t ounass-api:new .

# Start new container
docker run -d --name ounass-api-new -p 8001:8000 \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  -v $(pwd)/.env:/app/.env:ro \
  ounass-api:new

# Test new container
curl http://localhost:8001/api/v1/health

# Switch traffic (update load balancer/proxy)
# Stop old container
docker stop ounass-api
docker rm ounass-api

# Rename new container
docker rename ounass-api-new ounass-api
```

---

## Support and Maintenance Contacts

- **Repository**: https://github.com/sorted78/ounass-api
- **Issues**: https://github.com/sorted78/ounass-api/issues
- **Documentation**: See README.md and API_USAGE.md
