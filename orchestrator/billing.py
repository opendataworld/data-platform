"""Billing module - disabled for now"""
from dataclasses import dataclass

@dataclass
class ServicePricing:
    service_id: str = ""
    service_name: str = ""
    unit_price_cents: int = 0
    unit: str = ""
    included_quantity: int = 0
    monthly_price_cents: int = 0

SERVICE_PRICING = {}

class ServiceUsageTracker:
    def track_usage(self, *a, **kw): return {"ok": True}
    def get_customer_usage(self, *a): return {}

class LagoBillingClient:
    def create_customer(self, *a, **kw): return {"id": "demo"}

class BillingAwareAgentMixin:
    pass
