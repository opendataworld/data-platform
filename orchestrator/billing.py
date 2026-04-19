"""Billing module - stub for now"""
from dataclasses import dataclass

@dataclass
class ServicePricing:
    service_id: str = ""
    service_name: str = ""
    unit_price_cents: int = 0
    unit: str = ""
    included_quantity: int = 0
    monthly_price_cents: int = 0

SERVICE_PRICING = {
    "demo": ServicePricing(service_id="demo", service_name="Demo", unit_price_cents=0, unit="request")
}

class ServiceUsageTracker:
    def track_usage(self, *a, **kw): return {"ok": True}
    def get_customer_usage(self, *a): return {}

class LagoBillingClient:
    def create_customer(self, *a, **kw): return {"id": "demo"}

class BillingAwareAgentMixin:
    pass
