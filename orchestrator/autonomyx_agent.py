"""
AutonomyX Agent Specification for Data Platform Orchestrator
Implements the AutonomyX Agent Identity Specification v1.0
"""
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
import uuid
import hashlib


# ==== AutonomyX Data Models ====

class BudgetPolicy(BaseModel):
    """Budget policy for the agent."""
    measurement_period: Literal["day", "week", "month", "year"]
    max_spend_cents: int = Field(ge=0, description="Max spend in cents")


class RatePolicy(BaseModel):
    """Rate limiting policy."""
    window_seconds: int = Field(ge=1)
    max_requests: int = Field(ge=1)


class CredentialInfo(BaseModel):
    """Credential information for an agent."""
    credential_id: str
    token: str
    expires_at: datetime


class AgentCreateRequest(BaseModel):
    """Request to create an agent."""
    agent_name: str
    agent_type: Literal["workflow", "ephemeral", "tool-facing"]
    sponsor_subject_id: str
    tenant_id: str
    allowed_models: List[str]
    allowed_tools: Optional[List[str]] = None
    budget_policy: Optional[BudgetPolicy] = None
    rate_policy: Optional[RatePolicy] = None
    expires_at: Optional[datetime] = None
    owner_ids: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentDetail(BaseModel):
    """Full agent details."""
    agent_id: str
    agent_name: str
    agent_type: str
    sponsor_subject_id: str
    owner_ids: List[str]
    tenant_id: str
    allowed_models: List[str]
    allowed_tools: List[str]
    budget_policy: Optional[BudgetPolicy] = None
    rate_policy: Optional[RatePolicy] = None
    expires_at: Optional[datetime] = None
    status: Literal["requested", "active", "suspended", "expired", "revoked"]
    created_at: datetime
    last_active_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    credential: Optional[CredentialInfo] = None


# ==== Service Registry with AutonomyX ====

class AutonomyXAgentRegistry:
    """Agent registry following AutonomyX specification."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.agents: Dict[str, AgentDetail] = {}
    
    def generate_agent_id(self, agent_name: str, tenant_id: str) -> str:
        """Generate unique agent ID."""
        unique_str = f"{tenant_id}-{agent_name}-{uuid.uuid4()}"
        hash_suffix = hashlib.sha256(unique_str.encode())[:8].hexdigest()
        return f"agent-{agent_name.lower().replace(' ', '-')}-{hash_suffix}"
    
    def generate_credential(self) -> CredentialInfo:
        """Generate new credential."""
        return CredentialInfo(
            credential_id=str(uuid.uuid4()),
            token=f"tok_{uuid.uuid4().hex}",
            expires_at=datetime.now(timezone.utc) + timedelta(days=90)
        )
    
    def create_agent(self, request: AgentCreateRequest) -> AgentDetail:
        """Create a new agent."""
        agent_id = self.generate_agent_id(request.agent_name, request.tenant_id)
        credential = self.generate_credential()
        
        agent = AgentDetail(
            agent_id=agent_id,
            agent_name=request.agent_name,
            agent_type=request.agent_type,
            sponsor_subject_id=request.sponsor_subject_id,
            owner_ids=request.owner_ids or [request.sponsor_subject_id],
            tenant_id=request.tenant_id,
            allowed_models=request.allowed_models,
            allowed_tools=request.allowed_tools or [],
            budget_policy=request.budget_policy,
            rate_policy=request.rate_policy,
            expires_at=request.expires_at,
            status="active",
            created_at=datetime.now(timezone.utc),
            metadata=request.metadata or {},
            credential=credential
        )
        
        self.agents[agent_id] = agent
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[AgentDetail]:
        """Get agent by ID."""
        return self.agents.get(agent_id)
    
    def list_agents(self, tenant_id: Optional[str] = None, 
                   status: Optional[str] = None) -> List[AgentDetail]:
        """List agents with optional filters."""
        agents = list(self.agents.values())
        
        if tenant_id:
            agents = [a for a in agents if a.tenant_id == tenant_id]
        if status:
            agents = [a for a in agents if a.status == status]
        
        return agents
    
    def suspend_agent(self, agent_id: str) -> Optional[AgentDetail]:
        """Suspend an agent."""
        agent = self.agents.get(agent_id)
        if agent:
            agent.status = "suspended"
        return agent
    
    def reactivate_agent(self, agent_id: str) -> Optional[AgentDetail]:
        """Reactivate a suspended agent."""
        agent = self.agents.get(agent_id)
        if agent:
            agent.status = "active"
            agent.last_active_at = datetime.now(timezone.utc)
        return agent
    
    def revoke_agent(self, agent_id: str) -> Optional[AgentDetail]:
        """Revoke an agent."""
        agent = self.agents.get(agent_id)
        if agent:
            agent.status = "revoked"
            agent.credential = None
        return agent
    
    def rotate_credential(self, agent_id: str) -> Optional[CredentialInfo]:
        """Rotate agent credentials."""
        agent = self.agents.get(agent_id)
        if agent and agent.status == "active":
            new_cred = self.generate_credential()
            agent.credential = new_cred
            agent.last_active_at = datetime.now(timezone.utc)
            return new_cred
        return None


# ==== Data Platform Agents with AutonomyX ====

class DataPlatformAgentFactory:
    """Factory for creating data platform agents with AutonomyX."""
    
    # Default tools for each category
    DEFAULT_TOOLS = {
        "crawl": ["crawl_and_extract"],
        "embed": ["embed_text", "chunk_text"],
        "llm": ["query_llm"],
        "quality": ["validate_data", "check_lineage"],
        "nlp": ["extract_entities", "detect_pii", "classify_taxonomy"],
        "workflow": ["orchestrate_workflow", "stream_data"],
    }
    
    def __init__(self, registry: AutonomyXAgentRegistry):
        self.registry = registry
    
    def create_crawl_agent(self, name: str, sponsor_id: str, 
                          tenant_id: str) -> AgentDetail:
        """Create a web crawling agent."""
        request = AgentCreateRequest(
            agent_name=name,
            agent_type="workflow",
            sponsor_subject_id=sponsor_id,
            tenant_id=tenant_id,
            allowed_models=["llama3", "mistral"],
            allowed_tools=self.DEFAULT_TOOLS["crawl"],
            budget_policy=BudgetPolicy(measurement_period="month", max_spend_cents=50000),
            rate_policy=RatePolicy(window_seconds=3600, max_requests=1000),
            metadata={"category": "crawling", "service": "data-platform"}
        )
        return self.registry.create_agent(request)
    
    def create_embedding_agent(self, name: str, sponsor_id: str,
                             tenant_id: str) -> AgentDetail:
        """Create an embedding agent."""
        request = AgentCreateRequest(
            agent_name=name,
            agent_type="workflow",
            sponsor_subject_id=sponsor_id,
            tenant_id=tenant_id,
            allowed_models=["sentence-transformers"],
            allowed_tools=self.DEFAULT_TOOLS["embed"],
            budget_policy=BudgetPolicy(measurement_period="month", max_spend_cents=30000),
            rate_policy=RatePolicy(window_seconds=3600, max_requests=5000),
            metadata={"category": "embedding", "service": "data-platform"}
        )
        return self.registry.create_agent(request)
    
    def create_quality_agent(self, name: str, sponsor_id: str,
                           tenant_id: str) -> AgentDetail:
        """Create a data quality agent."""
        request = AgentCreateRequest(
            agent_name=name,
            agent_type="workflow",
            sponsor_subject_id=sponsor_id,
            tenant_id=tenant_id,
            allowed_models=["llama3"],
            allowed_tools=self.DEFAULT_TOOLS["quality"],
            budget_policy=BudgetPolicy(measurement_period="month", max_spend_cents=20000),
            rate_policy=RatePolicy(window_seconds=3600, max_requests=500),
            metadata={"category": "data-quality", "service": "data-platform"}
        )
        return self.registry.create_agent(request)
    
    def create_nlp_agent(self, name: str, sponsor_id: str,
                        tenant_id: str) -> AgentDetail:
        """Create an NLP agent."""
        request = AgentCreateRequest(
            agent_name=name,
            agent_type="workflow",
            sponsor_subject_id=sponsor_id,
            tenant_id=tenant_id,
            allowed_models=["llama3"],
            allowed_tools=self.DEFAULT_TOOLS["nlp"],
            budget_policy=BudgetPolicy(measurement_period="month", max_spend_cents=25000),
            rate_policy=RatePolicy(window_seconds=3600, max_requests=2000),
            metadata={"category": "nlp", "service": "data-platform"}
        )
        return self.registry.create_agent(request)
    
    def create_orchestrator_agent(self, name: str, sponsor_id: str,
                                tenant_id: str) -> AgentDetail:
        """Create the main orchestrator agent."""
        # All tools
        all_tools = []
        for tools in self.DEFAULT_TOOLS.values():
            all_tools.extend(tools)
        
        request = AgentCreateRequest(
            agent_name=name,
            agent_type="workflow",
            sponsor_subject_id=sponsor_id,
            tenant_id=tenant_id,
            allowed_models=["llama3", "mistral", "phi3"],
            allowed_tools=all_tools,
            budget_policy=BudgetPolicy(measurement_period="month", max_spend_cents=100000),
            rate_policy=RatePolicy(window_seconds=3600, max_requests=10000),
            metadata={"category": "orchestrator", "service": "data-platform"}
        )
        return self.registry.create_agent(request)


# ==== Usage Example ====

if __name__ == "__main__":
    # Create registry
    registry = AutonomyXAgentRegistry()
    factory = DataPlatformAgentFactory(registry)
    
    # Create agents
    orchestrator = factory.create_orchestrator_agent(
        name="data-platform-orchestrator",
        sponsor_id="admin-001",
        tenant_id="tenant-data-platform"
    )
    print(f"Created orchestrator: {orchestrator.agent_id}")
    
    crawl_agent = factory.create_crawl_agent(
        name="web-crawler",
        sponsor_id="admin-001",
        tenant_id="tenant-data-platform"
    )
    print(f"Created crawler: {crawl_agent.agent_id}")
    
    # List all agents
    print("\nAll agents:")
    for agent in registry.list_agents():
        print(f"  {agent.agent_id}: {agent.status}")