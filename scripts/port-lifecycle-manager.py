#!/usr/bin/env python3
"""
Port Lifecycle Management System
Manages port transitions from development to production
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
import subprocess

console = Console()

class PortLifecycleStage(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"
    DEPRECATED = "deprecated"

class ServiceLifecycle:
    """Manages the lifecycle of a service's port allocation"""
    
    def __init__(self, service_name: str, service_type: str, project: str):
        self.service_name = service_name
        self.service_type = service_type
        self.project = project
        self.config_dir = Path.home() / ".config" / "port-lifecycle"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.lifecycle_file = self.config_dir / f"{project}-{service_name}.json"
        self.lifecycle = self.load_lifecycle()
    
    def load_lifecycle(self) -> Dict:
        """Load service lifecycle data"""
        if self.lifecycle_file.exists():
            with open(self.lifecycle_file) as f:
                return json.load(f)
        return {
            "service": self.service_name,
            "type": self.service_type,
            "project": self.project,
            "created": str(datetime.now()),
            "stages": {},
            "transitions": []
        }
    
    def save_lifecycle(self):
        """Save service lifecycle data"""
        with open(self.lifecycle_file, 'w') as f:
            json.dump(self.lifecycle, f, indent=2)
    
    def add_stage(self, stage: PortLifecycleStage, port: int, config: Optional[Dict] = None):
        """Add a lifecycle stage"""
        self.lifecycle["stages"][stage.value] = {
            "port": port,
            "allocated_at": str(datetime.now()),
            "config": config or {},
            "active": True
        }
        
        self.lifecycle["transitions"].append({
            "action": "add_stage",
            "stage": stage.value,
            "port": port,
            "timestamp": str(datetime.now())
        })
        
        self.save_lifecycle()
    
    def promote(self, from_stage: PortLifecycleStage, to_stage: PortLifecycleStage):
        """Promote service from one stage to another"""
        if from_stage.value not in self.lifecycle["stages"]:
            raise ValueError(f"Service not in {from_stage.value} stage")
        
        from_config = self.lifecycle["stages"][from_stage.value]
        
        # Allocate new port for target stage if needed
        if to_stage == PortLifecycleStage.PRODUCTION:
            # Production uses standard ports
            port_map = {
                "web": 80,
                "api": 443,
                "database": 5432
            }
            to_port = port_map.get(self.service_type, from_config["port"])
        else:
            # Calculate port offset based on stage
            stage_offset = {
                PortLifecycleStage.TESTING: 1000,
                PortLifecycleStage.STAGING: 10000,
                PortLifecycleStage.PRODUCTION: 0
            }
            to_port = from_config["port"] + stage_offset.get(to_stage, 0)
        
        # Add new stage
        self.add_stage(to_stage, to_port, from_config["config"])
        
        # Record transition
        self.lifecycle["transitions"].append({
            "action": "promote",
            "from_stage": from_stage.value,
            "to_stage": to_stage.value,
            "from_port": from_config["port"],
            "to_port": to_port,
            "timestamp": str(datetime.now())
        })
        
        self.save_lifecycle()
        return to_port
    
    def deprecate(self, stage: PortLifecycleStage):
        """Deprecate a service stage"""
        if stage.value in self.lifecycle["stages"]:
            self.lifecycle["stages"][stage.value]["active"] = False
            self.lifecycle["stages"][stage.value]["deprecated_at"] = str(datetime.now())
            
            self.lifecycle["transitions"].append({
                "action": "deprecate",
                "stage": stage.value,
                "timestamp": str(datetime.now())
            })
            
            self.save_lifecycle()

class PortLifecycleManager:
    """Manages port lifecycle across all services"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "port-lifecycle"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.global_config_file = self.config_dir / "global-config.json"
        self.deployment_config_file = self.config_dir / "deployment-config.yaml"
        self.global_config = self.load_global_config()
    
    def load_global_config(self) -> Dict:
        """Load global lifecycle configuration"""
        if self.global_config_file.exists():
            with open(self.global_config_file) as f:
                return json.load(f)
        return {
            "promotion_rules": {
                "development_to_testing": {"min_uptime_hours": 1},
                "testing_to_staging": {"min_uptime_hours": 24, "tests_passed": True},
                "staging_to_production": {"min_uptime_hours": 168, "approval_required": True}
            },
            "port_mapping": {},
            "active_services": {}
        }
    
    def save_global_config(self):
        """Save global lifecycle configuration"""
        with open(self.global_config_file, 'w') as f:
            json.dump(self.global_config, f, indent=2)
    
    def generate_deployment_config(self, stage: PortLifecycleStage) -> Dict:
        """Generate deployment configuration for a stage"""
        config = {
            "version": "3.8",
            "stage": stage.value,
            "generated_at": str(datetime.now()),
            "services": {}
        }
        
        # Get all services in this stage
        for lifecycle_file in self.config_dir.glob("*.json"):
            if lifecycle_file.name == "global-config.json":
                continue
            
            with open(lifecycle_file) as f:
                lifecycle = json.load(f)
            
            if stage.value in lifecycle["stages"]:
                stage_config = lifecycle["stages"][stage.value]
                if stage_config.get("active", False):
                    service_name = lifecycle["service"]
                    config["services"][service_name] = {
                        "port": stage_config["port"],
                        "type": lifecycle["type"],
                        "project": lifecycle["project"],
                        "config": stage_config.get("config", {})
                    }
        
        return config
    
    def export_docker_compose(self, stage: PortLifecycleStage, output_file: Optional[str] = None):
        """Export Docker Compose configuration for a stage"""
        deployment_config = self.generate_deployment_config(stage)
        
        docker_compose = {
            "version": "3.8",
            "services": {}
        }
        
        for service_name, service_config in deployment_config["services"].items():
            docker_service = {
                "container_name": f"{service_name}-{stage.value}",
                "ports": [f"{service_config['port']}:{service_config['port']}"],
                "environment": {
                    "SERVICE_PORT": str(service_config['port']),
                    "STAGE": stage.value
                },
                "labels": {
                    "lifecycle.stage": stage.value,
                    "lifecycle.port": str(service_config['port']),
                    "lifecycle.type": service_config['type']
                }
            }
            
            # Add stage-specific configuration
            if stage == PortLifecycleStage.PRODUCTION:
                docker_service["restart"] = "always"
                docker_service["deploy"] = {
                    "replicas": 2,
                    "update_config": {
                        "parallelism": 1,
                        "delay": "10s"
                    }
                }
            
            docker_compose["services"][service_name] = docker_service
        
        # Add networks
        docker_compose["networks"] = {
            f"{stage.value}-network": {
                "driver": "bridge"
            }
        }
        
        # Save to file
        if output_file:
            with open(output_file, 'w') as f:
                yaml.dump(docker_compose, f, default_flow_style=False)
        
        return docker_compose
    
    def export_kubernetes_config(self, stage: PortLifecycleStage) -> List[Dict]:
        """Export Kubernetes configuration for a stage"""
        deployment_config = self.generate_deployment_config(stage)
        k8s_configs = []
        
        for service_name, service_config in deployment_config["services"].items():
            # Create deployment
            deployment = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": f"{service_name}-{stage.value}",
                    "labels": {
                        "app": service_name,
                        "stage": stage.value
                    }
                },
                "spec": {
                    "replicas": 3 if stage == PortLifecycleStage.PRODUCTION else 1,
                    "selector": {
                        "matchLabels": {
                            "app": service_name,
                            "stage": stage.value
                        }
                    },
                    "template": {
                        "metadata": {
                            "labels": {
                                "app": service_name,
                                "stage": stage.value
                            }
                        },
                        "spec": {
                            "containers": [{
                                "name": service_name,
                                "image": f"{service_config['project']}/{service_name}:{stage.value}",
                                "ports": [{
                                    "containerPort": service_config['port']
                                }],
                                "env": [
                                    {"name": "SERVICE_PORT", "value": str(service_config['port'])},
                                    {"name": "STAGE", "value": stage.value}
                                ]
                            }]
                        }
                    }
                }
            }
            
            # Create service
            service = {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": f"{service_name}-{stage.value}"
                },
                "spec": {
                    "type": "LoadBalancer" if stage == PortLifecycleStage.PRODUCTION else "ClusterIP",
                    "ports": [{
                        "port": service_config['port'],
                        "targetPort": service_config['port']
                    }],
                    "selector": {
                        "app": service_name,
                        "stage": stage.value
                    }
                }
            }
            
            k8s_configs.extend([deployment, service])
        
        return k8s_configs
    
    def show_lifecycle_status(self):
        """Show lifecycle status for all services"""
        table = Table(
            title="🔄 Port Lifecycle Status",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Service", style="cyan", no_wrap=True)
        table.add_column("Project", style="green")
        table.add_column("Development", justify="center")
        table.add_column("Testing", justify="center")
        table.add_column("Staging", justify="center")
        table.add_column("Production", justify="center")
        
        # Get all lifecycle files
        services = {}
        for lifecycle_file in self.config_dir.glob("*.json"):
            if lifecycle_file.name == "global-config.json":
                continue
            
            with open(lifecycle_file) as f:
                lifecycle = json.load(f)
            
            service_key = f"{lifecycle['project']}/{lifecycle['service']}"
            services[service_key] = lifecycle
        
        # Display services
        for service_key, lifecycle in sorted(services.items()):
            row = [
                lifecycle['service'],
                lifecycle['project']
            ]
            
            for stage in [PortLifecycleStage.DEVELOPMENT, PortLifecycleStage.TESTING, 
                         PortLifecycleStage.STAGING, PortLifecycleStage.PRODUCTION]:
                if stage.value in lifecycle["stages"]:
                    stage_info = lifecycle["stages"][stage.value]
                    if stage_info.get("active", False):
                        row.append(f"🟢 {stage_info['port']}")
                    else:
                        row.append(f"🔴 {stage_info['port']}")
                else:
                    row.append("—")
            
            table.add_row(*row)
        
        console.print(table)
    
    def generate_migration_plan(self, service_name: str, project: str, 
                               from_stage: PortLifecycleStage, 
                               to_stage: PortLifecycleStage) -> Dict:
        """Generate a migration plan for promoting a service"""
        plan = {
            "service": service_name,
            "project": project,
            "from_stage": from_stage.value,
            "to_stage": to_stage.value,
            "steps": [],
            "estimated_time": "30 minutes",
            "rollback_plan": []
        }
        
        # Add migration steps based on stages
        if to_stage == PortLifecycleStage.PRODUCTION:
            plan["steps"] = [
                "1. Run final test suite",
                "2. Create production database backup",
                "3. Update DNS records",
                "4. Deploy to production cluster",
                "5. Run smoke tests",
                "6. Monitor for 30 minutes",
                "7. Update documentation"
            ]
            plan["rollback_plan"] = [
                "1. Revert DNS changes",
                "2. Restore from backup",
                "3. Redeploy previous version",
                "4. Notify stakeholders"
            ]
            plan["estimated_time"] = "2-4 hours"
        else:
            plan["steps"] = [
                f"1. Allocate {to_stage.value} port",
                f"2. Deploy to {to_stage.value} environment",
                "3. Run integration tests",
                "4. Update monitoring",
                "5. Notify team"
            ]
            plan["rollback_plan"] = [
                f"1. Remove from {to_stage.value}",
                "2. Release allocated port",
                "3. Restore previous state"
            ]
        
        return plan

# CLI Commands
@click.group()
def cli():
    """Port Lifecycle Management System"""
    pass

@cli.command()
@click.argument('service_name')
@click.argument('service_type')
@click.argument('project')
@click.option('--port', type=int, help='Initial port (auto-allocated if not specified)')
def init(service_name, service_type, project, port):
    """Initialize a service lifecycle"""
    lifecycle = ServiceLifecycle(service_name, service_type, project)
    
    if not port:
        # Auto-allocate port using intelligent port manager
        from intelligent_port_manager import IntelligentPortManager
        manager = IntelligentPortManager()
        port = manager.allocate_port(service_name, service_type, "development", project)
    
    lifecycle.add_stage(PortLifecycleStage.DEVELOPMENT, port)
    console.print(f"[green]✅ Initialized {service_name} lifecycle with development port {port}[/green]")

@cli.command()
@click.argument('service_name')
@click.argument('project')
@click.argument('from_stage', type=click.Choice(['development', 'testing', 'staging']))
@click.argument('to_stage', type=click.Choice(['testing', 'staging', 'production']))
def promote(service_name, project, from_stage, to_stage):
    """Promote service to next stage"""
    lifecycle = ServiceLifecycle(service_name, "unknown", project)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Promoting {service_name}...", total=3)
        
        # Generate migration plan
        manager = PortLifecycleManager()
        plan = manager.generate_migration_plan(
            service_name, project,
            PortLifecycleStage(from_stage),
            PortLifecycleStage(to_stage)
        )
        
        progress.update(task, advance=1, description="Generated migration plan")
        
        # Show plan
        console.print(Panel(
            "\n".join(plan["steps"]),
            title=f"Migration Plan: {from_stage} → {to_stage}",
            border_style="yellow"
        ))
        
        # Confirm
        if click.confirm("Proceed with promotion?"):
            new_port = lifecycle.promote(
                PortLifecycleStage(from_stage),
                PortLifecycleStage(to_stage)
            )
            progress.update(task, advance=1, description="Promoted service")
            
            console.print(f"[green]✅ Promoted {service_name} to {to_stage} with port {new_port}[/green]")
            
            # Export configs
            if to_stage in ['staging', 'production']:
                manager.export_docker_compose(
                    PortLifecycleStage(to_stage),
                    f"docker-compose.{to_stage}.yml"
                )
                progress.update(task, advance=1, description="Generated deployment configs")
                console.print(f"[green]✅ Generated docker-compose.{to_stage}.yml[/green]")

@cli.command()
def status():
    """Show lifecycle status"""
    manager = PortLifecycleManager()
    manager.show_lifecycle_status()

@cli.command()
@click.argument('stage', type=click.Choice(['development', 'testing', 'staging', 'production']))
@click.option('--format', type=click.Choice(['docker', 'kubernetes']), default='docker')
@click.option('--output', '-o', help='Output file')
def export(stage, format, output):
    """Export deployment configuration"""
    manager = PortLifecycleManager()
    
    if format == 'docker':
        config = manager.export_docker_compose(PortLifecycleStage(stage), output)
        if not output:
            console.print(yaml.dump(config, default_flow_style=False))
        else:
            console.print(f"[green]✅ Exported Docker Compose config to {output}[/green]")
    else:
        configs = manager.export_kubernetes_config(PortLifecycleStage(stage))
        if output:
            with open(output, 'w') as f:
                yaml.dump_all(configs, f, default_flow_style=False)
            console.print(f"[green]✅ Exported Kubernetes configs to {output}[/green]")
        else:
            console.print(yaml.dump_all(configs, default_flow_style=False))

@cli.command()
@click.argument('service_name')
@click.argument('project')
def history(service_name, project):
    """Show service lifecycle history"""
    lifecycle = ServiceLifecycle(service_name, "unknown", project)
    
    if lifecycle.lifecycle.get("transitions"):
        console.print(f"\n[bold]Lifecycle History for {service_name}[/bold]\n")
        
        for transition in lifecycle.lifecycle["transitions"]:
            timestamp = transition["timestamp"][:19]
            action = transition["action"]
            
            if action == "add_stage":
                console.print(f"[green]{timestamp}[/green] Added to {transition['stage']} (port {transition['port']})")
            elif action == "promote":
                console.print(f"[blue]{timestamp}[/blue] Promoted from {transition['from_stage']} to {transition['to_stage']}")
            elif action == "deprecate":
                console.print(f"[red]{timestamp}[/red] Deprecated {transition['stage']}")
    else:
        console.print(f"[yellow]No history found for {service_name}[/yellow]")

if __name__ == "__main__":
    cli()