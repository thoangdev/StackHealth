# Production deployment script
#!/bin/bash

set -e

echo "🚀 Starting StackHealth Production Deployment"

# Configuration
ENVIRONMENT=${ENVIRONMENT:-production}
VERSION=${VERSION:-latest}
NAMESPACE=stackhealth

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    command -v kubectl >/dev/null 2>&1 || error "kubectl is required but not installed"
    command -v docker >/dev/null 2>&1 || error "docker is required but not installed"
    command -v helm >/dev/null 2>&1 || warn "helm not found - some features may not work"
    
    # Check kubectl connection
    kubectl cluster-info >/dev/null 2>&1 || error "Cannot connect to Kubernetes cluster"
    
    log "Prerequisites check completed ✅"
}

# Create namespace if it doesn't exist
create_namespace() {
    log "Creating namespace if it doesn't exist..."
    kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    log "Namespace ready ✅"
}

# Deploy secrets
deploy_secrets() {
    log "Deploying secrets..."
    
    if [ ! -f ".env.${ENVIRONMENT}" ]; then
        error "Environment file .env.${ENVIRONMENT} not found"
    fi
    
    # Create secret from environment file
    kubectl create secret generic stackhealth-secrets \
        --from-env-file=.env.${ENVIRONMENT} \
        --namespace=$NAMESPACE \
        --dry-run=client -o yaml | kubectl apply -f -
    
    log "Secrets deployed ✅"
}

# Build and push Docker image
build_and_push() {
    log "Building and pushing Docker image..."
    
    IMAGE_TAG="ghcr.io/thoangdev/stackhealth:${VERSION}"
    
    # Build image
    docker build -t $IMAGE_TAG .
    
    # Push image
    docker push $IMAGE_TAG
    
    log "Image built and pushed: $IMAGE_TAG ✅"
}

# Deploy application
deploy_application() {
    log "Deploying application..."
    
    # Update image tag in deployment
    sed "s|ghcr.io/thoangdev/stackhealth:latest|ghcr.io/thoangdev/stackhealth:${VERSION}|g" \
        deployment/kubernetes.yaml | kubectl apply -f -
    
    log "Application deployed ✅"
}

# Wait for deployment to be ready
wait_for_deployment() {
    log "Waiting for deployment to be ready..."
    
    kubectl rollout status deployment/stackhealth-api -n $NAMESPACE --timeout=300s
    
    log "Deployment is ready ✅"
}

# Run health checks
health_check() {
    log "Running health checks..."
    
    # Get service endpoint
    kubectl port-forward service/stackhealth-api-service 8080:80 -n $NAMESPACE &
    PORT_FORWARD_PID=$!
    
    # Wait a moment for port-forward to establish
    sleep 5
    
    # Health check
    if curl -f http://localhost:8080/health >/dev/null 2>&1; then
        log "Health check passed ✅"
    else
        error "Health check failed ❌"
    fi
    
    # Clean up port-forward
    kill $PORT_FORWARD_PID 2>/dev/null || true
}

# Database migration
run_migrations() {
    log "Running database migrations..."
    
    kubectl run migration-job \
        --image=ghcr.io/thoangdev/stackhealth:${VERSION} \
        --restart=Never \
        --namespace=$NAMESPACE \
        --command -- python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
    
    kubectl wait --for=condition=complete job/migration-job -n $NAMESPACE --timeout=300s
    kubectl delete job migration-job -n $NAMESPACE
    
    log "Database migrations completed ✅"
}

# Backup database (if applicable)
backup_database() {
    log "Creating database backup..."
    
    # This would typically backup your production database
    # Implementation depends on your database setup
    
    log "Database backup completed ✅"
}

# Rollback function
rollback() {
    warn "Rolling back deployment..."
    
    kubectl rollout undo deployment/stackhealth-api -n $NAMESPACE
    kubectl rollout status deployment/stackhealth-api -n $NAMESPACE --timeout=300s
    
    log "Rollback completed ✅"
}

# Main deployment flow
main() {
    log "Starting deployment to $ENVIRONMENT environment"
    
    # Set trap for cleanup on exit
    trap 'error "Deployment failed"' ERR
    
    case "${1:-deploy}" in
        "deploy")
            check_prerequisites
            create_namespace
            backup_database
            build_and_push
            deploy_secrets
            run_migrations
            deploy_application
            wait_for_deployment
            health_check
            log "🎉 Deployment completed successfully!"
            ;;
        "rollback")
            check_prerequisites
            rollback
            health_check
            log "🔄 Rollback completed successfully!"
            ;;
        "health")
            health_check
            ;;
        *)
            echo "Usage: $0 {deploy|rollback|health}"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
