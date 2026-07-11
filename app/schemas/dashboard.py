from pydantic import BaseModel
from typing import List, Optional

class KPICards(BaseModel):
    total_production_value: float
    production_growth: str          # "+12.4% vs last month"
    funds_in_escrow: float
    upcoming_net30: float
    pending_invoices_count: int

class PipelineOrderResponse(BaseModel):
    order_number: str
    item_name: str
    color_variant: str
    total_value: float
    escrow_secured: bool
    current_stage: str
    progress_percentage: int
    est_delivery: str

class ActivityResponse(BaseModel):
    type: str
    title: str
    description: str
    time_ago: str

class FactoryResponse(BaseModel):
    name: str
    location: str
    phase: str

class DashboardResponse(BaseModel):
    kpis: KPICards
    pipeline: List[PipelineOrderResponse]
    activities: List[ActivityResponse]
    factories: List[FactoryResponse]