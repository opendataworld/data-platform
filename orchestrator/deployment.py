"""
Data Platform Agent - With Service Deployment Integration
The agent can deploy services on-demand via docker deploy
"""
import os
import subprocess
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

# LangGraph imports
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPOSE_FILE = REPO_ROOT / "docker-compose.yml"

PROFILE_SERVICES: Dict[str, List[str]] = {
    "sso": ["oauth2-proxy"],
    "catalog": ["openmetadata"],
    "ingest": ["airbyte", "firecrawl", "crawl4ai", "iab-taxonomy", "g2-api", "google-search-console"],
    "crawl": ["firecrawl", "crawl4ai", "redis", "playwright", "iab-taxonomy", "g2-api", "searxng"],
    "label": ["labelstudio", "argilla"],
    "feedback": ["argilla"],
    "test": ["playwright"],
    "resolve": ["zingg"],
    "semantic": ["cube"],
    "viz": ["superset"],
    "cdp": ["unomi"],
    "store": ["postgres", "surrealdb"],
    "kg-edit": ["terminusdb", "jena"],
    "kg-pub": ["graphdb", "jena"],
    "search": ["searxng", "google-search-console"],
}


def _run_compose_cmd(args: List[str]) -> subprocess.CompletedProcess:
    """Run docker compose command from repository root and return result."""
    return subprocess.run(
        ["docker", "compose", "-f", str(COMPOSE_FILE), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


# ==== Docker Deploy Tool for Agent ====

@tool
def docker_deploy(profile: str, service: str = None) -> Dict:
    """
    Deploy services on-demand using Docker Compose.
    The agent will call this when additional services are needed.
    
    Args:
        profile: The profile to deploy (ml, ingest, store, catalog, crawl, etc.)
        service: Optional specific service name. If not provided, deploys the entire profile.
    
    Example:
        docker_deploy(profile="ml")  # Deploy all ML services
        docker_deploy(profile="ml", service="ollama")  # Deploy only Ollama
    """
    try:
        if profile not in PROFILE_SERVICES:
            return {"error": f"Unknown profile '{profile}'", "available_profiles": sorted(PROFILE_SERVICES)}

        if service and service not in PROFILE_SERVICES[profile]:
            return {
                "error": f"Service '{service}' is not part of profile '{profile}'",
                "profile_services": PROFILE_SERVICES[profile],
            }

        args = ["--profile", profile, "up", "-d"]
        if service:
            args.append(service)
        result = _run_compose_cmd(args)
        
        if result.returncode == 0:
            return {
                "status": "deployed",
                "profile": profile,
                "service": service or "all",
                "message": f"Successfully deployed {service or profile} services",
                "stdout": result.stdout.strip(),
            }
        else:
            return {
                "error": result.stderr.strip() or "docker compose up failed",
                "profile": profile,
                "stdout": result.stdout.strip(),
            }
    except Exception as e:
        return {"error": str(e)}


@tool
def docker_stop(profile: str = None, service: str = None) -> Dict:
    """
    Stop deployed services.
    
    Args:
        profile: The profile to stop
        service: Optional specific service name
    """
    try:
        if service:
            result = _run_compose_cmd(["stop", service])
        elif profile:
            if profile not in PROFILE_SERVICES:
                return {"error": f"Unknown profile '{profile}'", "available_profiles": sorted(PROFILE_SERVICES)}
            services = PROFILE_SERVICES[profile]
            result = _run_compose_cmd(["stop", *services])
        else:
            result = _run_compose_cmd(["down"])

        if result.returncode != 0:
            return {"error": result.stderr.strip() or "docker compose stop failed", "profile": profile, "service": service}

        return {"status": "stopped", "profile": profile, "service": service or ("all" if not profile else PROFILE_SERVICES[profile]), "stdout": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}


@tool
def docker_status() -> Dict:
    """
    Get status of all services - currently running and available.
    """
    try:
        result = _run_compose_cmd(["ps", "--format", "json"])
        
        services = []
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line:
                    services.append(json.loads(line))
        
        return {
            "running": services,
            "count": len(services)
        }
    except Exception as e:
        return {"error": str(e)}


@tool
def docker_ps() -> List[Dict]:
    """
    List running containers.
    """
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True
        )
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                containers.append({
                    "name": parts[0],
                    "status": parts[1] if len(parts) > 1 else "unknown"
                })
        
        return containers
    except Exception as e:
        return [{"error": str(e)}]


@tool
def list_available_profiles() -> Dict:
    """
    List available Docker profiles and what services they include.
    """
    return {"profiles": PROFILE_SERVICES}


# ==== Agent Tools ====

# All tools available to the agent
AGENT_TOOLS = [
    docker_deploy,
    docker_stop,
    docker_status,
    docker_ps,
    list_available_profiles,
]


# ==== Data Platform Agent ====

class DataPlatformAgent:
    """
    Main orchestrator agent with on-demand service deployment.
    The agent can deploy additional services when needed.
    """
    
    def __init__(self, model: str = "gpt-4", base_url: str = None):
        self.model = model
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
        self.api_key = os.getenv("OPENAI_API_KEY", "dummy")
        
        # Create the agent with docker deploy tools
        self.llm = ChatOpenAI(
            model=model,
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        self.agent = create_react_agent(self.llm, AGENT_TOOLS)
    
    async def run(self, prompt: str) -> Dict:
        """
        Run the agent with automatic service deployment.
        
        The agent will:
        1. Analyze the request
        2. Deploy any needed services automatically
        3. Execute the task
        """
        result = await self.agent.ainvoke({"messages": [("user", prompt)]})
        
        return {
            "response": result["messages"][-1].content,
            "deployed_services": self._get_deployed_services()
        }
    
    def _get_deployed_services(self) -> List[str]:
        """Get list of currently deployed services."""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True
            )
            return [s for s in result.stdout.strip().split('\n') if s]
        except:
            return []


# ==== Main Execution ====

if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🤖 Data Platform Agent")
        print("=" * 40)
        
        # List available tools
        print("\n📦 Available Agent Tools:")
        for tool in AGENT_TOOLS:
            print(f"  - {tool.name}")
        
        # Example: Deploy ML services
        print("\n🚀 Example: Deploying ML services...")
        result = docker_deploy.invoke({"profile": "ml"})
        print(result)
        
        print("\n✅ Agent ready!")
    
    asyncio.run(main())
