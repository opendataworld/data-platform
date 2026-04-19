"""
Lago Billing Integration for Data Platform
Manages pricing plans and creates billing events
"""
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import requests
import os


# ==== Pricing Configuration ====

@dataclass
class ServicePricing:
    """Pricing for a single service."""
    service_id: str
    service_name: str
    unit_price_cents: int
    unit: str  # "request", "minute", "mb", "gb", "token"
    included_quantity: int = 0
    monthly_price_cents: int = 0


# Data Platform Service Pricing
SERVICE_PRICING = {
    # Crawling Services
    "crawl.jina-reader": ServicePricing(
        service_id="crawl-jina-reader",
        service_name="Jina Reader Crawling",
        unit_price_cents=1,  # $0.01 per page
        unit="page"
    ),
    "crawl.firecrawl": ServicePricing(
        service_id="crawl-firecrawl",
        service_name="Firecrawl Crawling",
        unit_price_cents=2,
        unit="page"
    ),
    "crawl.playwright": ServicePricing(
        service_id="crawl-playwright",
        service_name="Playwright Crawling",
        unit_price_cents=5,
        unit="page"
    ),
    
    # Embeddings
    "embedding.sentence-transformers": ServicePricing(
        service_id="embedding-sentence-transformers",
        service_name="Sentence Transformers",
        unit_price_cents=0.1,
        unit="1k_tokens"
    ),
    "embedding.bge": ServicePricing(
        service_id="embedding-bge",
        service_name="BGE Embeddings",
        unit_price_cents=0.15,
        unit="1k_tokens"
    ),
    
    # OCR
    "ocr.tesseract": ServicePricing(
        service_id="ocr-tesseract",
        service_name="Tesseract OCR",
        unit_price_cents=1,
        unit="image"
    ),
    "ocr.easyocr": ServicePricing(
        service_id="ocr-easyocr",
        service_name="EasyOCR",
        unit_price_cents=2,
        unit="image"
    ),
    
    # Speech-to-Text
    "stt.whisper": ServicePricing(
        service_id="stt-whisper",
        service_name="Whisper Transcription",
        unit_price_cents=1,
        unit="minute"
    ),
    
    # LLMs
    "llm.ollama": ServicePricing(
        service_id="llm-ollama",
        service_name="Ollama LLM",
        unit_price_cents=0.5,
        unit="1k_tokens"
    ),
    "llm.gpt4all": ServicePricing(
        service_id="llm-gpt4all",
        service_name="GPT4All",
        unit_price_cents=0.3,
        unit="1k_tokens"
    ),
    
    # Data Quality
    "quality.great-expectations": ServicePricing(
        service_id="quality-great-expectations",
        service_name="Great Expectations",
        unit_price_cents=10,
        unit="validation"
    ),
    "quality.soda": ServicePricing(
        service_id="quality-soda",
        service_name="Soda Core",
        unit_price_cents=8,
        unit="validation"
    ),
    
    # Data Governance
    "governance.datahub": ServicePricing(unit_price_cents=1, service_id="governance-datahub", service_name="DataHub Catalog", monthly_price_cents=49900, unit="month")
        service_id="governance-datahub",
        service_name="DataHub Catalog",
        monthly_price_cents=49900,  # $499/month
        unit="month"
    ),
    "governance.atlas": ServicePricing(unit_price_cents=1, service_id="governance-atlas", service_name="Atlas Governance", monthly_price_cents=39900, unit="month")
        service_id="governance-atlas",
        service_name="Atlas Governance",
        monthly_price_cents=39900,
        unit="month"
    ),
    
    # Workflow Orchestration
    "workflow.airflow": ServicePricing(unit_price_cents=1, service_id="workflow-airflow", service_name="Airflow Orchestration", monthly_price_cents=29900, unit="month")
        service_id="workflow-airflow",
        service_name="Airflow Orchestration",
        monthly_price_cents=29900,
        unit="month"
    ),
    "workflow.prefect": ServicePricing(unit_price_cents=1, service_id="workflow-prefect", service_name="Prefect Orchestration", monthly_price_cents=29900, unit="month")
        service_id="workflow-prefect",
        service_name="Prefect Orchestration",
        monthly_price_cents=19900,
        unit="month"
    ),
    
    # Streaming
    "stream.kafka": ServicePricing(unit_price_cents=1, service_id="stream-kafka", service_name="Kafka Stream", monthly_price_cents=19900, unit="month")
        service_id="stream-kafka",
        service_name="Kafka Streaming",
        unit_price_cents=10,
        unit="1k_messages"
    ),
    "stream.redpanda": ServicePricing(unit_price_cents=1, service_id="stream-redpanda", service_name="Redpanda Stream", monthly_price_cents=19900, unit="month")
        service_id="stream-redpanda",
        service_name="Redpanda Streaming",
        unit_price_cents=8,
        unit="1k_messages"
    ),
    
    # LangFlow/Low-Code
    "workflow.langflow": ServicePricing(unit_price_cents=1, service_id="workflow-langflow", service_name="LangFlow", monthly_price_cents=0, unit="month")
        service_id="workflow-langflow",
        service_name="LangFlow",
        monthly_price_cents=19900,
        unit="month"
    ),
    "workflow.n8n": ServicePricing(
        service_id="workflow-n8n",
        service_name="n8n Automation",
        monthly_price_cents=9900,
        unit="month"
    ),
}


# ==== Lago Client ====

class LagoBillingClient:
    """Client for Lago billing API."""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or os.getenv("LAGO_URL", "http://localhost:3000")
        self.api_key = api_key or os.getenv("LAGO_API_KEY", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_customer(self, customer_id: str, name: str, email: str) -> dict:
        """Create a customer in Lago."""
        # In production, this would call the Lago API
        return {
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "status": "created"
        }
    
    def create_event(self, customer_id: str, event_code: str, properties: dict = None) -> dict:
        """Create a billing event."""
        # In production, this would call the Lago API
        return {
            "event_id": f"evt_{customer_id}_{event_code}_{datetime.now().timestamp()}",
            "customer_id": customer_id,
            "event_code": event_code,
            "properties": properties or {},
            "timestamp": datetime.now().isoformat()
        }
    
    def get_usage(self, customer_id: str) -> dict:
        """Get customer usage."""
        return {
            "customer_id": customer_id,
            "events_count": 0,
            "total_amount_cents": 0
        }


# ==== Service Usage Tracker ====

class ServiceUsageTracker:
    """Tracks service usage for billing."""
    
    def __init__(self, billing_client: LagoBillingClient = None):
        self.billing_client = billing_client or LagoBillingClient()
        self.usage_cache: Dict[str, List[dict]] = {}
    
    def track_usage(self, customer_id: str, service_id: str, quantity: float, metadata: dict = None):
        """Track service usage."""
        pricing = SERVICE_PRICING.get(service_id)
        if not pricing:
            return
        
        # Calculate cost
        if pricing.monthly_price_cents > 0:
            amount = pricing.monthly_price_cents
        else:
            amount = int(quantity * pricing.unit_price_cents)
        
        event = {
            "service_id": service_id,
            "service_name": pricing.service_name,
            "quantity": quantity,
            "unit": pricing.unit,
            "amount_cents": amount,
            "metadata": metadata or {}
        }
        
        # Store in cache
        if customer_id not in self.usage_cache:
            self.usage_cache[customer_id] = []
        self.usage_cache[customer_id].append(event)
        
        # Create event in Lago
        self.billing_client.create_event(
            customer_id=customer_id,
            event_code=service_id,
            properties={
                "quantity": quantity,
                "amount_cents": amount,
                "unit": pricing.unit
            }
        )
        
        return event
    
    def get_customer_usage(self, customer_id: str) -> dict:
        """Get all usage for a customer."""
        events = self.usage_cache.get(customer_id, [])
        total = sum(e["amount_cents"] for e in events)
        
        return {
            "customer_id": customer_id,
            "events": events,
            "total_amount_cents": total,
            "total_amount_usd": total / 100
        }


# ==== Agent Integration ====

class BillingAwareAgentMixin:
    """Mixin to add billing awareness to agents."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.billing_client = LagoBillingClient()
        self.tracker = ServiceUsageTracker(self.billing_client)
    
    def get_service_price(self, service_id: str) -> ServicePricing:
        """Get pricing for a service."""
        return SERVICE_PRICING.get(service_id)
    
    def list_services_with_pricing(self) -> List[Dict]:
        """List all services with their pricing."""
        return [
            {
                "service_id": sp.service_id,
                "service_name": sp.service_name,
                "price_per_unit_cents": sp.unit_price_cents,
                "unit": sp.unit,
                "monthly_price_cents": sp.monthly_price_cents
            }
            for sp in SERVICE_PRICING.values()
        ]
    
    def track_service_usage(self, customer_id: str, service_id: str, quantity: float, metadata: dict = None):
        """Track usage for billing."""
        return self.tracker.track_usage(customer_id, service_id, quantity, metadata)
    
    def get_customer_billing_summary(self, customer_id: str) -> dict:
        """Get billing summary for a customer."""
        return self.tracker.get_customer_usage(customer_id)
    
    def create_customer(self, customer_id: str, name: str, email: str):
        """Create a customer in billing system."""
        return self.billing_client.create_customer(customer_id, name, email)


# ==== Usage Examples ====

if __name__ == "__main__":
    # Example usage
    tracker = ServiceUsageTracker()
    
    # Track some usage
    tracker.track_usage("customer-123", "crawl.jina-reader", 100)
    tracker.track_usage("customer-123", "embedding.sentence-transformers", 10000)
    tracker.track_usage("customer-123", "llm.ollama", 5000)
    
    # Get billing summary
    summary = tracker.get_customer_usage("customer-123")
    print(f"Customer billing summary:")
    print(f"  Total: ${summary['total_amount_usd']:.2f}")
    print(f"  Events: {len(summary['events'])}")