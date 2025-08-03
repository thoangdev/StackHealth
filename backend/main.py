from fastapi import FastAPI, Depends, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
import crud
import schemas
import database
import auth
from pdf_generator import generate_pdf_report
from health import router as health_router

app = FastAPI(
    title="Software Scorecard Dashboard API",
    description="API for tracking and visualizing software scorecards with authentication",
    version="2.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Include health check routes
app.include_router(health_router, tags=["health"])


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Software Scorecard Dashboard API v2.0 is running!"}


# Authentication endpoints
@app.post("/auth/login", response_model=schemas.Token)
def login_for_access_token(
    login_request: schemas.LoginRequest,
    db: Session = Depends(database.get_db)
):
    """Authenticate user and return access token"""
    user = auth.authenticate_user(db, login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/auth/register", response_model=schemas.AdminUser)
def register_admin_user(
    user_data: schemas.AdminUserCreate,
    db: Session = Depends(database.get_db)
):
    """Register a new admin user (for demo purposes - restrict in production)"""
    # Check if user already exists
    existing_user = auth.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return auth.create_admin_user(db, user_data.email, user_data.password)


# Product endpoints (protected)
@app.post("/products", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate, 
    db: Session = Depends(database.get_db),
    current_user: database.AdminUser = Depends(auth.get_current_user)
):
    """Create a new product"""
    # Check if product with same name already exists
    db_product = crud.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    
    return crud.create_product(db=db, product=product)


@app.get("/products", response_model=List[schemas.Product])
def list_products(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user: database.AdminUser = Depends(auth.get_current_user)
):
    """Get all products"""
    return crud.get_products(db, skip=skip, limit=limit) 

# Scorecard endpoints (protected)
@app.post("/scorecards", response_model=schemas.Scorecard)
def create_scorecard(
    scorecard: schemas.ScorecardCreate,
    db: Session = Depends(database.get_db),
    current_user: database.AdminUser = Depends(auth.get_current_user)
):
    """Submit a new scorecard with feedback"""
    # Verify product exists
    product = crud.get_product_by_id(db, product_id=scorecard.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Validate category
    valid_categories = ["automation", "performance", "security", "cicd"]
    if scorecard.category not in valid_categories:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        )
    
    return crud.create_scorecard(db=db, scorecard=scorecard)


@app.get("/scorecards", response_model=List[schemas.ScorecardWithProduct])
def list_scorecards(
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: database.AdminUser = Depends(auth.get_current_user)
):
    """Get scorecards, optionally filtered by product and category"""
    scorecards = crud.get_scorecards_by_product(
        db, product_id=product_id, category=category, skip=skip, limit=limit
    )
    
    # Convert to response format with product name
    result = []
    for scorecard in scorecards:
        scorecard_data = schemas.ScorecardWithProduct(
            id=scorecard.id,
            product_id=scorecard.product_id,
            product_name=scorecard.product.name,
            category=scorecard.category,
            date=scorecard.date,
            score=scorecard.score,
            breakdown=scorecard.breakdown,
            feedback=scorecard.feedback,
            tool_suggestions=scorecard.tool_suggestions,
            created_at=scorecard.created_at
        )
        result.append(scorecard_data)
    
    return result


@app.get("/scorecards/{scorecard_id}/pdf")
def get_scorecard_pdf(
    scorecard_id: int,
    db: Session = Depends(database.get_db),
    current_user: database.AdminUser = Depends(auth.get_current_user)
):
    """Generate and return PDF report for a scorecard"""
    scorecard = crud.get_scorecard_by_id(db, scorecard_id=scorecard_id)
    if not scorecard:
        raise HTTPException(status_code=404, detail="Scorecard not found")
    
    # Generate PDF
    pdf_bytes = generate_pdf_report(scorecard)
    
    # Return PDF as response
    filename = f"scorecard_{scorecard.product.name}_{scorecard.category}_{scorecard.date}.pdf"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/pdf"
    }
    
    return Response(content=pdf_bytes, headers=headers, media_type="application/pdf")


@app.get("/scorecards/{scorecard_id}", response_model=schemas.Scorecard)
def get_scorecard(
    scorecard_id: int,
    db: Session = Depends(database.get_db),
    current_user: database.AdminUser = Depends(auth.get_current_user)
):
    """Get a specific scorecard with all details"""
    scorecard = crud.get_scorecard_by_id(db, scorecard_id=scorecard_id)
    if not scorecard:
        raise HTTPException(status_code=404, detail="Scorecard not found")
    
    return scorecard


@app.get("/trends/{product_id}/{category}", response_model=List[schemas.TrendData])
def get_trend_data(
    product_id: int,
    category: str,
    quarters: int = 4,
    db: Session = Depends(database.get_db),
    current_user: database.AdminUser = Depends(auth.get_current_user)
):
    """Get quarterly trend data for a product's specific category"""
    # Verify product exists
    product = crud.get_product_by_id(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Validate category
    valid_categories = ["automation", "performance", "security", "cicd"]
    if category not in valid_categories:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        )
    
    trend_data = crud.get_trend_data(db, product_id, category, quarters)
    
    return [
        schemas.TrendData(
            date=scorecard.date,
            score=scorecard.score,
            category=scorecard.category
        )
        for scorecard in trend_data
    ]


@app.get("/quarterly-improvement/{product_id}/{category}", response_model=List[schemas.TrendData])
def get_quarterly_improvement(
    product_id: int,
    category: str,
    db: Session = Depends(database.get_db),
    current_user: database.AdminUser = Depends(auth.get_current_user)
):
    """Get quarterly improvement data showing one scorecard per quarter"""
    # Verify product exists
    product = crud.get_product_by_id(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Validate category
    valid_categories = ["automation", "performance", "security", "cicd"]
    if category not in valid_categories:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        )
    
    quarterly_data = crud.get_quarterly_improvement_data(db, product_id, category)
    
    return [
        schemas.TrendData(
            date=scorecard.date,
            score=scorecard.score,
            category=scorecard.category
        )
        for scorecard in quarterly_data
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
