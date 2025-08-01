# Deployment Guide - Streaming Platform ETL + Dashboard

This guide covers multiple deployment options for the Streaming Platform ETL + Dashboard system.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- Kubernetes cluster (for cloud deployment)

### 1. Local Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_database.py

# Start the system (3 terminals)
python etl_pipeline.py
python log_producer.py
streamlit run dashboard.py
```

### 2. Docker Deployment

```bash
# Build and deploy with Docker Compose
./deploy.sh deploy -t docker

# Or manually
docker-compose -f docker-compose.deploy.yml up -d --build
```

### 3. Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -k kubernetes/

# Check deployment status
kubectl get pods -l app=streaming-platform
```

## 📋 Deployment Options

### Local Development
- **Best for**: Development and testing
- **Pros**: Fast iteration, easy debugging
- **Cons**: Limited scalability, manual process

### Docker Deployment
- **Best for**: Production, consistent environments
- **Pros**: Containerized, reproducible, easy scaling
- **Cons**: Requires Docker infrastructure

### Kubernetes Deployment
- **Best for**: Cloud production, high availability
- **Pros**: Auto-scaling, load balancing, high availability
- **Cons**: Complex setup, requires Kubernetes expertise

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHONUNBUFFERED` | Python output buffering | `1` |
| `STREAMLIT_SERVER_PORT` | Dashboard port | `8501` |
| `STREAMLIT_SERVER_ADDRESS` | Dashboard address | `0.0.0.0` |
| `LOG_GENERATION_RATE` | Logs per second | `10` |
| `ETL_PROCESSING_INTERVAL` | ETL cycle interval | `5` |

### Database Configuration

The system uses SQLite by default. For production, consider:
- PostgreSQL for better concurrency
- Redis for caching
- Elasticsearch for log storage

## 🌐 Production Deployment

### 1. Docker Production

```bash
# Production deployment
./deploy.sh deploy -t docker -e prod

# With custom configuration
docker-compose -f docker-compose.deploy.yml -f docker-compose.prod.yml up -d
```

### 2. Kubernetes Production

```bash
# Create namespace
kubectl create namespace streaming-platform

# Apply production manifests
kubectl apply -f kubernetes/ -n streaming-platform

# Set up ingress
kubectl apply -f kubernetes/ingress.yaml
```

### 3. Cloud Platforms

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag streaming-platform:latest $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/streaming-platform:latest
docker push $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/streaming-platform:latest
```

#### Google Cloud Run
```bash
# Deploy to Cloud Run
gcloud run deploy streaming-platform \
  --image gcr.io/$PROJECT_ID/streaming-platform \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances
```bash
# Deploy to ACI
az container create \
  --resource-group myResourceGroup \
  --name streaming-platform \
  --image streaming-platform:latest \
  --ports 8501
```

## 🔒 Security Considerations

### 1. Network Security
- Use HTTPS/TLS encryption
- Configure firewall rules
- Implement rate limiting
- Set up VPN for internal access

### 2. Application Security
- Use environment variables for secrets
- Implement authentication/authorization
- Regular security updates
- Input validation and sanitization

### 3. Data Security
- Encrypt data at rest
- Secure database connections
- Regular backups
- Data retention policies

## 📊 Monitoring & Logging

### 1. Application Monitoring
```bash
# Check application health
curl http://localhost:8501/_stcore/health

# Monitor logs
docker-compose logs -f streaming-app
```

### 2. System Monitoring
- CPU and memory usage
- Disk space monitoring
- Network traffic analysis
- Error rate tracking

### 3. Logging
- Application logs in `/app/logs`
- System logs via Docker/Kubernetes
- Centralized logging (ELK stack)

## 🔄 CI/CD Pipeline

### GitHub Actions
The repository includes a GitHub Actions workflow that:
1. Runs tests on pull requests
2. Builds Docker images
3. Deploys to staging/production
4. Monitors deployment health

### Manual Deployment
```bash
# Build and test
./deploy.sh deploy -t docker

# Check status
./deploy.sh status

# Stop deployment
./deploy.sh stop
```

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts**
   ```bash
   # Check port usage
   lsof -i :8501
   # Change port in config.py
   ```

2. **Database issues**
   ```bash
   # Reinitialize database
   python init_database.py
   ```

3. **Docker issues**
   ```bash
   # Clean up containers
   docker-compose down -v
   docker system prune
   ```

4. **Kubernetes issues**
   ```bash
   # Check pod status
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

### Performance Optimization

1. **Database optimization**
   - Add indexes for frequently queried columns
   - Implement connection pooling
   - Regular database maintenance

2. **Application optimization**
   - Enable caching
   - Optimize queries
   - Use async processing where possible

3. **Infrastructure optimization**
   - Auto-scaling policies
   - Load balancing
   - CDN for static assets

## 📈 Scaling

### Horizontal Scaling
- Multiple application instances
- Load balancer configuration
- Database read replicas

### Vertical Scaling
- Increase CPU/memory resources
- Optimize application code
- Database performance tuning

## 🔄 Backup & Recovery

### Data Backup
```bash
# Backup database
cp data/streaming.db data/streaming.db.backup

# Backup logs
tar -czf logs_backup.tar.gz logs/
```

### Disaster Recovery
1. Regular automated backups
2. Cross-region replication
3. Recovery testing procedures
4. Documentation of recovery steps

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Verify configuration settings
4. Contact the development team

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Python Best Practices](https://docs.python-guide.org/) 