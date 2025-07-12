#!/usr/bin/env python3
"""
Intelligent Port Management System
Automatically assigns ports based on service type and tracks usage in real-time
"""

import os
import sys
import json
import subprocess
import socket
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.live import Live
from rich.layout import Layout
import yaml

console = Console()

# Industry-standard port ranges by service type
SERVICE_PORT_RANGES = {
    # Web Services (HTTP/HTTPS)
    "web": {
        "development": (3000, 3999),    # React, Vue, Angular dev servers
        "staging": (8000, 8999),        # General web services
        "production": (80, 443),        # Standard HTTP/HTTPS
        "description": "Web applications, UI servers"
    },
    
    # API Services
    "api": {
        "development": (4000, 4999),    # REST APIs, GraphQL
        "staging": (8000, 8999),        # Can overlap with web in staging
        "production": (443, 443),       # HTTPS API
        "description": "REST APIs, GraphQL endpoints"
    },
    
    # Databases
    "database": {
        "postgres": (5432, 5499),       # PostgreSQL and variants
        "mysql": (3306, 3399),          # MySQL/MariaDB
        "mongodb": (27017, 27099),      # MongoDB
        "redis": (6379, 6399),          # Redis
        "elasticsearch": (9200, 9299),   # Elasticsearch
        "cassandra": (9042, 9099),      # Cassandra
        "description": "Database servers"
    },
    
    # Message Queues
    "messaging": {
        "rabbitmq": (5672, 5699),       # RabbitMQ
        "kafka": (9092, 9099),          # Kafka
        "nats": (4222, 4299),           # NATS
        "redis-pubsub": (6379, 6399),   # Redis Pub/Sub
        "description": "Message brokers and queues"
    },
    
    # Caching
    "cache": {
        "redis": (6379, 6399),          # Redis cache
        "memcached": (11211, 11299),    # Memcached
        "hazelcast": (5701, 5799),      # Hazelcast
        "description": "Caching servers"
    },
    
    # Monitoring & Metrics
    "monitoring": {
        "prometheus": (9090, 9099),      # Prometheus
        "grafana": (3000, 3099),        # Grafana
        "jaeger": (16686, 16699),       # Jaeger UI
        "zipkin": (9411, 9419),         # Zipkin
        "signoz": (3301, 3399),         # SigNoz
        "description": "Monitoring and observability"
    },
    
    # Development Tools
    "devtools": {
        "webpack": (8080, 8089),        # Webpack dev server
        "vite": (5173, 5199),           # Vite
        "storybook": (6006, 6099),      # Storybook
        "jupyter": (8888, 8899),        # Jupyter
        "description": "Development tools and utilities"
    },
    
    # Microservices & Service Mesh
    "microservices": {
        "consul": (8500, 8599),         # Consul
        "eureka": (8761, 8799),         # Eureka
        "istio": (15000, 15099),        # Istio
        "linkerd": (8086, 8099),        # Linkerd
        "description": "Service discovery and mesh"
    },
    
    # Search Services
    "search": {
        "elasticsearch": (9200, 9299),   # Elasticsearch
        "solr": (8983, 8999),           # Solr
        "meilisearch": (7700, 7799),    # MeiliSearch
        "description": "Search engines"
    },
    
    # Workflow Engines
    "workflow": {
        "temporal": (7233, 7299),        # Temporal
        "airflow": (8080, 8089),        # Airflow
        "prefect": (4200, 4299),        # Prefect
        "description": "Workflow orchestration"
    },
    
    # Authentication & Security
    "auth": {
        "keycloak": (8080, 8099),       # Keycloak
        "fusionauth": (9011, 9099),     # FusionAuth
        "oauth2-proxy": (4180, 4199),   # OAuth2 Proxy
        "description": "Authentication services"
    },
    
    # Storage & CDN
    "storage": {
        "minio": (9000, 9099),          # MinIO
        "seaweedfs": (9333, 9399),      # SeaweedFS
        "description": "Object storage services"
    }
}

# Environment configurations
ENVIRONMENT_CONFIG = {
    "development": {
        "prefix": "",
        "suffix": "",
        "base_offset": 0
    },
    "staging": {
        "prefix": "stg-",
        "suffix": "",
        "base_offset": 10000  # Add 10000 to all ports
    },
    "production": {
        "prefix": "prod-",
        "suffix": "",
        "base_offset": 0,     # Use standard ports
        "use_standard": True  # Use standard ports (80, 443, etc)
    }
}

class PortStatus(Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    RESERVED = "reserved"
    BLOCKED = "blocked"

class IntelligentPortManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "intelligent-port-manager"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.config_dir / "port-registry.json"
        self.history_file = self.config_dir / "port-history.json"
        self.registry = self.load_registry()
        self.history = self.load_history()
        
    def load_registry(self) -> Dict:
        """Load the port registry"""
        if self.registry_file.exists():
            with open(self.registry_file) as f:
                return json.load(f)
        return {
            "ports": {},
            "services": {},
            "environments": {},
            "updated": str(datetime.now())
        }
    
    def load_history(self) -> List:
        """Load port allocation history"""
        if self.history_file.exists():
            with open(self.history_file) as f:
                return json.load(f)
        return []
    
    def save_registry(self):
        """Save the port registry"""
        self.registry["updated"] = str(datetime.now())
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def save_history(self):
        """Save port allocation history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def is_port_available(self, port: int) -> bool:
        """Check if a port is available"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return True
        except:
            return False
    
    def get_service_type(self, service_name: str) -> Optional[str]:
        """Intelligently determine service type from name"""
        service_lower = service_name.lower()
        
        # Database detection
        if any(db in service_lower for db in ['postgres', 'mysql', 'mongo', 'redis', 'elastic', 'cassandra']):
            return "database"
        
        # Web service detection
        if any(web in service_lower for web in ['web', 'ui', 'frontend', 'react', 'vue', 'angular']):
            return "web"
        
        # API detection
        if any(api in service_lower for api in ['api', 'rest', 'graphql', 'backend']):
            return "api"
        
        # Messaging detection
        if any(msg in service_lower for msg in ['rabbitmq', 'kafka', 'nats', 'queue', 'broker']):
            return "messaging"
        
        # Monitoring detection
        if any(mon in service_lower for mon in ['prometheus', 'grafana', 'metrics', 'monitor']):
            return "monitoring"
        
        # Workflow detection
        if any(wf in service_lower for wf in ['temporal', 'airflow', 'workflow']):
            return "workflow"
        
        # Auth detection
        if any(auth in service_lower for auth in ['auth', 'keycloak', 'oauth']):
            return "auth"
        
        return None
    
    def allocate_port(self, 
                     service_name: str, 
                     service_type: Optional[str] = None,
                     environment: str = "development",
                     project: Optional[str] = None) -> Optional[int]:
        """Intelligently allocate a port for a service"""
        
        # Auto-detect service type if not provided
        if not service_type:
            service_type = self.get_service_type(service_name)
            if not service_type:
                service_type = "web"  # Default to web
        
        # Get appropriate port range
        if service_type == "database":
            # Special handling for database types
            if "postgres" in service_name.lower():
                port_range = SERVICE_PORT_RANGES["database"]["postgres"]
            elif "mysql" in service_name.lower():
                port_range = SERVICE_PORT_RANGES["database"]["mysql"]
            elif "mongo" in service_name.lower():
                port_range = SERVICE_PORT_RANGES["database"]["mongodb"]
            elif "redis" in service_name.lower():
                port_range = SERVICE_PORT_RANGES["database"]["redis"]
            else:
                port_range = SERVICE_PORT_RANGES["database"]["postgres"]  # Default
        else:
            # Get range for service type and environment
            ranges = SERVICE_PORT_RANGES.get(service_type, SERVICE_PORT_RANGES["web"])
            if environment in ranges:
                port_range = ranges[environment]
            elif "development" in ranges:
                port_range = ranges["development"]
            else:
                # Get first available range
                for key, value in ranges.items():
                    if isinstance(value, tuple):
                        port_range = value
                        break
        
        # Apply environment offset
        env_config = ENVIRONMENT_CONFIG.get(environment, ENVIRONMENT_CONFIG["development"])
        base_offset = env_config.get("base_offset", 0)
        
        # Find available port in range
        start_port = port_range[0] + base_offset
        end_port = port_range[1] + base_offset
        
        for port in range(start_port, end_port + 1):
            # Check if port is already registered
            if str(port) in self.registry["ports"]:
                continue
            
            # Check if port is actually available
            if self.is_port_available(port):
                # Register the port
                self.register_port(port, service_name, service_type, environment, project)
                return port
        
        # No available port found in range
        console.print(f"[red]No available ports in range {start_port}-{end_port} for {service_type}[/red]")
        return None
    
    def register_port(self, 
                     port: int, 
                     service_name: str, 
                     service_type: str,
                     environment: str,
                     project: Optional[str] = None):
        """Register a port allocation"""
        port_info = {
            "service": service_name,
            "type": service_type,
            "environment": environment,
            "project": project or "unknown",
            "allocated_at": str(datetime.now()),
            "status": PortStatus.IN_USE.value,
            "pid": self.get_process_using_port(port)
        }
        
        self.registry["ports"][str(port)] = port_info
        
        # Update service registry
        if service_name not in self.registry["services"]:
            self.registry["services"][service_name] = []
        self.registry["services"][service_name].append(port)
        
        # Add to history
        self.history.append({
            "action": "allocate",
            "port": port,
            "service": service_name,
            "timestamp": str(datetime.now())
        })
        
        self.save_registry()
        self.save_history()
    
    def release_port(self, port: int):
        """Release a port"""
        if str(port) in self.registry["ports"]:
            port_info = self.registry["ports"][str(port)]
            
            # Remove from service registry
            service_name = port_info["service"]
            if service_name in self.registry["services"]:
                self.registry["services"][service_name].remove(port)
                if not self.registry["services"][service_name]:
                    del self.registry["services"][service_name]
            
            # Remove from port registry
            del self.registry["ports"][str(port)]
            
            # Add to history
            self.history.append({
                "action": "release",
                "port": port,
                "service": service_name,
                "timestamp": str(datetime.now())
            })
            
            self.save_registry()
            self.save_history()
    
    def get_process_using_port(self, port: int) -> Optional[int]:
        """Get PID of process using port"""
        try:
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                return int(result.stdout.strip().split()[0])
        except:
            pass
        return None
    
    def sync_registry(self):
        """Sync registry with actual port usage"""
        # Check all registered ports
        for port_str, port_info in list(self.registry["ports"].items()):
            port = int(port_str)
            if self.is_port_available(port):
                # Port is free but registered as in use
                console.print(f"[yellow]Port {port} is free but registered to {port_info['service']}. Releasing...[/yellow]")
                self.release_port(port)
    
    def generate_docker_compose_env(self, project: str, environment: str = "development") -> str:
        """Generate docker-compose environment file with allocated ports"""
        env_content = f"""# Auto-generated port configuration
# Project: {project}
# Environment: {environment}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        # Get all services for this project
        project_services = {}
        for port_str, port_info in self.registry["ports"].items():
            if port_info.get("project") == project and port_info.get("environment") == environment:
                service_type = port_info["type"].upper()
                if service_type not in project_services:
                    project_services[service_type] = []
                project_services[service_type].append((port_info["service"], int(port_str)))
        
        # Generate environment variables
        for service_type, services in sorted(project_services.items()):
            env_content += f"# {service_type} Services\n"
            for service_name, port in services:
                var_name = f"{service_name.upper().replace('-', '_')}_PORT"
                env_content += f"{var_name}={port}\n"
            env_content += "\n"
        
        return env_content
    
    def show_intelligent_status(self):
        """Show intelligent port status with recommendations"""
        # Create main table
        table = Table(
            title="🧠 Intelligent Port Management Status",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Port", style="cyan", no_wrap=True)
        table.add_column("Service", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Environment", style="blue")
        table.add_column("Project", style="magenta")
        table.add_column("Status", justify="center")
        table.add_column("Allocated", style="dim")
        
        # Sort ports numerically
        sorted_ports = sorted(self.registry["ports"].items(), key=lambda x: int(x[0]))
        
        for port_str, port_info in sorted_ports:
            status_icon = "🟢" if port_info["status"] == PortStatus.IN_USE.value else "🔴"
            
            table.add_row(
                port_str,
                port_info["service"],
                port_info["type"],
                port_info["environment"],
                port_info.get("project", "unknown"),
                status_icon,
                port_info["allocated_at"][:19]  # Just date and time
            )
        
        console.print(table)
        
        # Show recommendations
        self.show_recommendations()
    
    def show_recommendations(self):
        """Show port allocation recommendations"""
        recommendations = []
        
        # Check for services using non-standard ports
        for port_str, port_info in self.registry["ports"].items():
            port = int(port_str)
            service_type = port_info["type"]
            
            # Get expected range for this service type
            if service_type in SERVICE_PORT_RANGES:
                expected_ranges = []
                for key, value in SERVICE_PORT_RANGES[service_type].items():
                    if isinstance(value, tuple):
                        expected_ranges.append(value)
                
                # Check if port is in any expected range
                in_expected_range = any(start <= port <= end for start, end in expected_ranges)
                
                if not in_expected_range:
                    recommendations.append(
                        f"⚠️  {port_info['service']} ({service_type}) on port {port} - "
                        f"Consider using standard {service_type} port range"
                    )
        
        if recommendations:
            console.print("\n📋 [bold yellow]Recommendations:[/bold yellow]")
            for rec in recommendations:
                console.print(f"   {rec}")
    
    def export_for_llm(self) -> Dict:
        """Export port status in LLM-friendly format"""
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_ports_allocated": len(self.registry["ports"]),
                "by_type": self._count_by_type(),
                "by_environment": self._count_by_environment(),
                "by_project": self._count_by_project()
            },
            "available_ranges": self._get_available_ranges(),
            "allocated_ports": self.registry["ports"],
            "recommendations": self._get_recommendations_for_llm()
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """Count ports by service type"""
        counts = {}
        for port_info in self.registry["ports"].values():
            service_type = port_info["type"]
            counts[service_type] = counts.get(service_type, 0) + 1
        return counts
    
    def _count_by_environment(self) -> Dict[str, int]:
        """Count ports by environment"""
        counts = {}
        for port_info in self.registry["ports"].values():
            env = port_info["environment"]
            counts[env] = counts.get(env, 0) + 1
        return counts
    
    def _count_by_project(self) -> Dict[str, int]:
        """Count ports by project"""
        counts = {}
        for port_info in self.registry["ports"].values():
            project = port_info.get("project", "unknown")
            counts[project] = counts.get(project, 0) + 1
        return counts
    
    def _get_available_ranges(self) -> Dict[str, List[Tuple[int, int]]]:
        """Get available port ranges by service type"""
        available = {}
        
        for service_type, ranges in SERVICE_PORT_RANGES.items():
            available[service_type] = []
            
            for key, value in ranges.items():
                if isinstance(value, tuple):
                    start, end = value
                    # Find gaps in allocation
                    allocated_in_range = [
                        int(p) for p in self.registry["ports"]
                        if start <= int(p) <= end
                    ]
                    
                    if len(allocated_in_range) < (end - start):
                        available[service_type].append((start, end))
        
        return available
    
    def _get_recommendations_for_llm(self) -> List[str]:
        """Get recommendations in LLM-friendly format"""
        recommendations = []
        
        # Check for port conflicts
        for port_str, port_info in self.registry["ports"].items():
            if not self.is_port_available(int(port_str)):
                recommendations.append(
                    f"Port {port_str} is registered to {port_info['service']} "
                    f"but appears to be in use by another process"
                )
        
        return recommendations

# CLI Commands
@click.group()
def cli():
    """Intelligent Port Management System"""
    pass

@cli.command()
@click.argument('service_name')
@click.option('--type', 'service_type', help='Service type (web, api, database, etc)')
@click.option('--env', 'environment', default='development', help='Environment (development, staging, production)')
@click.option('--project', help='Project name')
def allocate(service_name, service_type, environment, project):
    """Allocate a port for a service"""
    manager = IntelligentPortManager()
    
    # Sync registry first
    manager.sync_registry()
    
    # Allocate port
    port = manager.allocate_port(service_name, service_type, environment, project)
    
    if port:
        console.print(f"[green]✅ Allocated port {port} for {service_name}[/green]")
        console.print(f"[dim]Type: {service_type or 'auto-detected'}[/dim]")
        console.print(f"[dim]Environment: {environment}[/dim]")
        
        # Show how to use it
        console.print(f"\n[bold]To use this port:[/bold]")
        console.print(f"Export: [cyan]export {service_name.upper().replace('-', '_')}_PORT={port}[/cyan]")
        console.print(f"Docker: [cyan]-p {port}:{port}[/cyan]")
    else:
        console.print(f"[red]❌ Failed to allocate port for {service_name}[/red]")

@cli.command()
@click.argument('port', type=int)
def release(port):
    """Release a port"""
    manager = IntelligentPortManager()
    manager.release_port(port)
    console.print(f"[green]✅ Released port {port}[/green]")

@cli.command()
def status():
    """Show intelligent port status"""
    manager = IntelligentPortManager()
    manager.sync_registry()
    manager.show_intelligent_status()

@cli.command()
def sync():
    """Sync registry with actual port usage"""
    manager = IntelligentPortManager()
    manager.sync_registry()
    console.print("[green]✅ Registry synced with actual port usage[/green]")

@cli.command()
@click.argument('project')
@click.option('--env', 'environment', default='development', help='Environment')
def generate_env(project, environment):
    """Generate environment file for project"""
    manager = IntelligentPortManager()
    env_content = manager.generate_docker_compose_env(project, environment)
    
    filename = f".ports.{environment}.env"
    with open(filename, 'w') as f:
        f.write(env_content)
    
    console.print(f"[green]✅ Generated {filename}[/green]")
    console.print(env_content)

@cli.command()
def export_llm():
    """Export port data for LLM consumption"""
    manager = IntelligentPortManager()
    data = manager.export_for_llm()
    
    # Save to file
    export_file = Path.home() / ".config" / "intelligent-port-manager" / "llm-export.json"
    with open(export_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    console.print(f"[green]✅ Exported LLM data to {export_file}[/green]")
    console.print(json.dumps(data, indent=2))

@cli.command()
def ranges():
    """Show standard port ranges by service type"""
    table = Table(
        title="📋 Standard Port Ranges by Service Type",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Service Type", style="cyan", no_wrap=True)
    table.add_column("Port Range", style="green")
    table.add_column("Common Services", style="yellow")
    table.add_column("Description", style="dim")
    
    for service_type, config in SERVICE_PORT_RANGES.items():
        if "description" in config:
            # Extract port ranges
            ranges = []
            examples = []
            
            for key, value in config.items():
                if isinstance(value, tuple):
                    ranges.append(f"{key}: {value[0]}-{value[1]}")
                    if key in ["postgres", "mysql", "mongodb", "redis"]:
                        examples.append(key.capitalize())
            
            table.add_row(
                service_type,
                "\n".join(ranges[:3]),  # Show first 3 ranges
                ", ".join(examples[:3]) if examples else service_type.capitalize(),
                config["description"]
            )
    
    console.print(table)

if __name__ == "__main__":
    cli()