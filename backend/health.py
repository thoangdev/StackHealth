from fastapi import APIRouter
import psutil
import time
import sys
from datetime import datetime
from sqlalchemy import text
from database import get_db

router = APIRouter()

# Store startup time
startup_time = time.time()

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "uptime_seconds": int(time.time() - startup_time)
    }

@router.get("/health/detailed")
async def detailed_health():
    """Detailed health check with system metrics"""
    try:
        # System metrics
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database check
        db_status = "unknown"
        try:
            db = next(get_db())
            db.execute(text("SELECT 1"))
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
        finally:
            db.close()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0.0",
            "uptime_seconds": int(time.time() - startup_time),
            "system": {
                "python_version": sys.version,
                "platform": sys.platform,
                "memory_usage_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_usage_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "cpu_count": psutil.cpu_count()
            },
            "database": {
                "status": db_status
            },
            "endpoints": {
                "api_docs": "/docs",
                "health": "/health",
                "metrics": "/health/detailed"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@router.get("/health/readiness")
async def readiness_check():
    """Readiness check for Kubernetes"""
    try:
        # Check database connection
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not_ready", "error": str(e)}

@router.get("/health/liveness")
async def liveness_check():
    """Liveness check for Kubernetes"""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
