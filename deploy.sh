#!/bin/bash

# Streaming Platform ETL + Dashboard Deployment Script
# Supports local, Docker, and cloud deployments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="streaming-platform-etl"
DOCKER_IMAGE="streaming-platform:latest"
DOCKER_COMPOSE_FILE="docker-compose.deploy.yml"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if required files exist
    if [ ! -f "Dockerfile" ]; then
        print_error "Dockerfile not found in current directory."
        exit 1
    fi
    
    if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
        print_error "Docker Compose file $DOCKER_COMPOSE_FILE not found."
        exit 1
    fi
    
    print_success "Prerequisites check passed!"
}

# Function to build Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t $DOCKER_IMAGE .
    print_success "Docker image built successfully!"
}

# Function to deploy with Docker Compose
deploy_docker_compose() {
    print_status "Deploying with Docker Compose..."
    
    # Stop existing containers
    docker-compose -f $DOCKER_COMPOSE_FILE down
    
    # Build and start services
    docker-compose -f $DOCKER_COMPOSE_FILE up -d --build
    
    print_success "Deployment completed!"
    print_status "Services are starting up..."
    
    # Wait for services to be ready
    sleep 10
    
    # Check service status
    docker-compose -f $DOCKER_COMPOSE_FILE ps
}

# Function to deploy locally
deploy_local() {
    print_status "Deploying locally..."
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip3 install -r requirements.txt
    
    # Initialize database
    print_status "Initializing database..."
    python3 init_database.py
    
    print_success "Local deployment completed!"
    print_status "To start the system, run:"
    echo "  Terminal 1: python3 etl_pipeline.py"
    echo "  Terminal 2: python3 log_producer.py"
    echo "  Terminal 3: streamlit run dashboard.py"
}

# Function to deploy to cloud (example for AWS ECS)
deploy_cloud() {
    print_status "Deploying to cloud..."
    
    # This is a placeholder for cloud deployment
    # You would need to implement specific cloud provider logic here
    
    print_warning "Cloud deployment not implemented yet."
    print_status "Please implement cloud-specific deployment logic."
}

# Function to check deployment status
check_status() {
    print_status "Checking deployment status..."
    
    if [ "$DEPLOYMENT_TYPE" = "docker" ]; then
        docker-compose -f $DOCKER_COMPOSE_FILE ps
        docker-compose -f $DOCKER_COMPOSE_FILE logs --tail=20
    else
        print_status "Local deployment - check terminal outputs for status"
    fi
}

# Function to stop deployment
stop_deployment() {
    print_status "Stopping deployment..."
    
    if [ "$DEPLOYMENT_TYPE" = "docker" ]; then
        docker-compose -f $DOCKER_COMPOSE_FILE down
        print_success "Deployment stopped!"
    else
        print_status "Local deployment - stop the Python processes manually"
    fi
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS] COMMAND"
    echo ""
    echo "Commands:"
    echo "  deploy     Deploy the application"
    echo "  status     Check deployment status"
    echo "  stop       Stop the deployment"
    echo "  help       Show this help message"
    echo ""
    echo "Options:"
    echo "  -t, --type TYPE    Deployment type (local|docker|cloud) [default: docker]"
    echo "  -e, --env ENV      Environment (dev|staging|prod) [default: dev]"
    echo ""
    echo "Examples:"
    echo "  $0 deploy                    # Deploy with Docker (default)"
    echo "  $0 deploy -t local           # Deploy locally"
    echo "  $0 deploy -t docker -e prod  # Deploy with Docker in production"
    echo "  $0 status                    # Check deployment status"
    echo "  $0 stop                      # Stop deployment"
}

# Parse command line arguments
DEPLOYMENT_TYPE="docker"
ENVIRONMENT="dev"
COMMAND=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            DEPLOYMENT_TYPE="$2"
            shift 2
            ;;
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        deploy|status|stop|help)
            COMMAND="$1"
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main execution
case $COMMAND in
    deploy)
        print_status "Starting deployment..."
        print_status "Deployment type: $DEPLOYMENT_TYPE"
        print_status "Environment: $ENVIRONMENT"
        
        check_prerequisites
        
        case $DEPLOYMENT_TYPE in
            local)
                deploy_local
                ;;
            docker)
                build_image
                deploy_docker_compose
                ;;
            cloud)
                deploy_cloud
                ;;
            *)
                print_error "Unknown deployment type: $DEPLOYMENT_TYPE"
                exit 1
                ;;
        esac
        
        print_success "Deployment completed successfully!"
        print_status "Dashboard will be available at: http://localhost:8501"
        ;;
    
    status)
        check_status
        ;;
    
    stop)
        stop_deployment
        ;;
    
    help|"")
        show_help
        ;;
    
    *)
        print_error "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac 