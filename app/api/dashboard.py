from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.dashboard import ProductionOrder, ActivityLog, Factory
from app.schemas.dashboard import DashboardResponse, KPICards, PipelineOrderResponse, ActivityResponse, FactoryResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardResponse)
def get_dashboard_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 1. Calculate KPI Cards (Matches top row of UI)
    # Real-world app would use aggregation queries like func.sum() here
    kpis = KPICards(
        total_production_value=248390.00,
        production_growth="+12.4% vs last month",
        funds_in_escrow=52100.50,
        upcoming_net30=14200.00,
        pending_invoices_count=2
    )

    # 2. Fetch Active Production Pipeline (Middle pipeline cards)
    orders = db.query(ProductionOrder).filter(ProductionOrder.user_id == current_user.id).all()
    pipeline_data = [
        PipelineOrderResponse(
            order_number=o.order_number,
            item_name=o.item_name,
            color_variant=o.color_variant,
            total_value=o.total_value,
            escrow_secured=bool(o.escrow_secured),
            current_stage=o.current_stage,
            progress_percentage=o.progress_percentage,
            est_delivery=o.est_delivery.strftime("%b %d, %Y") if o.est_delivery else "TBD"
        ) for o in orders
    ]

    # 3. Fetch Recent Activity Feed (Right side panel)
    logs = db.query(ActivityLog).filter(ActivityLog.user_id == current_user.id).order_by(ActivityLog.created_at.desc()).limit(3).all()
    activity_data = [
        ActivityResponse(
            type=l.type,
            title=l.title,
            description=l.description,
            time_ago="2 hours ago" # Helper function could calculate humanized time difference
        ) for l in logs
    ]

    # 4. Fetch Assigned Factories (Bottom right panel)
    # Queries unique factories linked to the active production orders
    factories_raw = db.query(Factory).join(ProductionOrder).filter(ProductionOrder.user_id == current_user.id).distinct().all()
    factory_data = [
        FactoryResponse(name=f.name, location=f.location, phase=f.phase) for f in factories_raw
    ]

    return {
        "kpis": kpis,
        "pipeline": pipeline_data,
        "activities": activity_data,
        "factories": factory_data
    }