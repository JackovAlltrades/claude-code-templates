#!/usr/bin/env python3
"""
Universal Port Manager - Central port management for all projects
Automatically detects Docker services, running processes, and assigns ports
"""

import os
import sys
import json
import socket
import subprocess
import psutil
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Configuration
PORT_REGISTRY_PATH = Path.home() / ".config" / "universal-port-manager"
GLOBAL_REGISTRY = PORT_REGISTRY_PATH / "registry.json"
PORT_RANGES = {
    "web": (8000, 8099),
    "api": (8100, 8199),
    "db": (5400, 5499),
    "cache": (6300, 6399),
    "queue": (5670, 5680),
    "monitoring": (9000, 9099),
    "temporal": (7230, 7239),
    "misc": (3000, 3099)
}

console = Console()

class PortManager:
    def __init__(self):
        self.ensure_registry()
        self.load_registry()
    
    def ensure_registry(self):
        """Create registry directory and file if not exists"""
        PORT_REGISTRY_PATH.mkdir(parents=True, exist_ok=True)
        if not GLOBAL_REGISTRY.exists():
            self.registry = {
                "ports": {},
                "projects": {},
                "last_updated": datetime.now().isoformat()
            }
            self.save_registry()
    
    def load_registry(self):
        """Load the global registry"""
        with open(GLOBAL_REGISTRY, 'r') as f:
            self.registry = json.load(f)
    
    def save_registry(self):
        """Save the global registry"""
        self.registry["last_updated"] = datetime.now().isoformat()
        with open(GLOBAL_REGISTRY, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def scan_system_ports(self) -> Dict[int, Dict]:
        """Scan all ports currently in use on the system"""
        active_ports = {}
        
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN':
                port = conn.laddr.port
                try:
                    process = psutil.Process(conn.pid)
                    active_ports[port] = {
                        "pid": conn.pid,
                        "process": process.name(),
                        "cmdline": ' '.join(process.cmdline()[:3]),
                        "status": "system"
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    active_ports[port] = {
                        "pid": conn.pid,
                        "process": "unknown",
                        "status": "system"
                    }
        
        return active_ports
    
    def scan_docker_services(self) -> List[Dict]:
        """Scan Docker containers and their exposed ports"""
        docker_services = []
        
        try:
            # Get running containers
            result = subprocess.run(
                ["docker", "ps", "--format", "json"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        container = json.loads(line)
                        # Parse ports
                        if 'Ports' in container:
                            docker_services.append({
                                "name": container.get('Names', 'unknown'),
                                "image": container.get('Image', 'unknown'),
                                "ports": container.get('Ports', ''),
                                "id": container.get('ID', '')[:12]
                            })
        except Exception as e:
            console.print(f"[yellow]Warning: Could not scan Docker services: {e}[/yellow]")
        
        return docker_services
    
    def scan_project_configs(self, project_path: Path) -> Dict[str, List[int]]:
        """Scan project for port configurations"""
        ports_found = {
            "docker-compose": [],
            "package.json": [],
            ".env": [],
            "config": [],
            "makefile": []
        }
        
        # Check docker-compose files
        for compose_file in project_path.glob("**/docker-compose*.y*ml"):
            try:
                with open(compose_file, 'r') as f:
                    compose_data = yaml.safe_load(f)
                    if compose_data and 'services' in compose_data:
                        for service, config in compose_data['services'].items():
                            if 'ports' in config:
                                for port_mapping in config['ports']:
                                    if ':' in str(port_mapping):
                                        host_port = str(port_mapping).split(':')[0]
                                        try:
                                            ports_found["docker-compose"].append(int(host_port))
                                        except ValueError:
                                            pass
            except Exception:
                pass
        
        # Check package.json
        pkg_json = project_path / "package.json"
        if pkg_json.exists():
            try:
                with open(pkg_json, 'r') as f:
                    pkg_data = json.load(f)
                    # Look for port in scripts
                    scripts = pkg_data.get('scripts', {})
                    for script in scripts.values():
                        if 'PORT=' in script:
                            port_match = script.split('PORT=')[1].split()[0]
                            try:
                                ports_found["package.json"].append(int(port_match))
                            except ValueError:
                                pass
            except Exception:
                pass
        
        # Check .env files
        for env_file in project_path.glob("**/.env*"):
            if env_file.is_file() and not env_file.name.endswith('.example'):
                try:
                    with open(env_file, 'r') as f:
                        for line in f:
                            if 'PORT' in line and '=' in line:
                                try:
                                    port = int(line.split('=')[1].strip())
                                    ports_found[".env"].append(port)
                                except ValueError:
                                    pass
                except Exception:
                    pass
        
        # Check Makefile
        makefile = project_path / "Makefile"
        if makefile.exists():
            try:
                with open(makefile, 'r') as f:
                    content = f.read()
                    # Look for common port patterns
                    import re
                    port_patterns = [
                        r':(\d{4,5})',  # :8080
                        r'PORT[= ]+(\d{4,5})',  # PORT=8080
                        r'localhost:(\d{4,5})'  # localhost:8080
                    ]
                    for pattern in port_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            try:
                                port = int(match)
                                if 1000 < port < 65535:
                                    ports_found["makefile"].append(port)
                            except ValueError:
                                pass
            except Exception:
                pass
        
        return ports_found
    
    def find_available_port(self, service_type: str = "misc", 
                          preferred: Optional[int] = None) -> int:
        """Find an available port for a service type"""
        # Get active ports
        active_ports = self.scan_system_ports()
        registered_ports = set(int(p) for p in self.registry["ports"].keys())
        used_ports = set(active_ports.keys()) | registered_ports
        
        # Try preferred port first
        if preferred and preferred not in used_ports:
            return preferred
        
        # Get range for service type
        start, end = PORT_RANGES.get(service_type, PORT_RANGES["misc"])
        
        # Find first available
        for port in range(start, end + 1):
            if port not in used_ports:
                return port
        
        # If no port in range, try misc range
        if service_type != "misc":
            return self.find_available_port("misc")
        
        raise ValueError("No available ports found")
    
    def register_project_port(self, project: str, service: str, 
                            port: int, auto_assigned: bool = False):
        """Register a port for a project/service"""
        # Update ports registry
        self.registry["ports"][str(port)] = {
            "project": project,
            "service": service,
            "assigned_at": datetime.now().isoformat(),
            "auto_assigned": auto_assigned
        }
        
        # Update projects registry
        if project not in self.registry["projects"]:
            self.registry["projects"][project] = {}
        
        self.registry["projects"][project][service] = port
        
        self.save_registry()
    
    def get_project_ports(self, project: str) -> Dict[str, int]:
        """Get all ports assigned to a project"""
        return self.registry["projects"].get(project, {})
    
    def cleanup_dead_ports(self):
        """Remove ports that are no longer in use"""
        active_ports = self.scan_system_ports()
        dead_ports = []
        
        for port, info in self.registry["ports"].items():
            if int(port) not in active_ports:
                dead_ports.append(port)
        
        for port in dead_ports:
            project = self.registry["ports"][port]["project"]
            service = self.registry["ports"][port]["service"]
            
            # Remove from ports registry
            del self.registry["ports"][port]
            
            # Remove from projects registry
            if project in self.registry["projects"]:
                if service in self.registry["projects"][project]:
                    del self.registry["projects"][project][service]
        
        self.save_registry()
        return len(dead_ports)
    
    def generate_project_env(self, project_path: Path, project_name: Optional[str] = None):
        """Generate .ports.env file for a project"""
        if not project_name:
            project_name = project_path.name
        
        # Scan project for existing configurations
        existing_ports = self.scan_project_configs(project_path)
        
        # Common services for projects
        common_services = {
            "web": "web",
            "api": "api",
            "db": "db",
            "redis": "cache",
            "temporal": "temporal",
            "docs": "web",
            "metrics": "monitoring"
        }
        
        env_content = f"# Port assignments for {project_name}\n"
        env_content += f"# Generated by Universal Port Manager on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        assigned_ports = {}
        
        for service, service_type in common_services.items():
            # Check if we already have a port for this service
            existing = self.get_project_ports(project_name).get(service)
            
            if existing:
                port = existing
            else:
                # Check if found in project configs
                preferred = None
                for source, ports in existing_ports.items():
                    if ports:
                        preferred = ports[0]
                        break
                
                port = self.find_available_port(service_type, preferred)
                self.register_project_port(project_name, service, port, auto_assigned=True)
            
            assigned_ports[service] = port
            env_content += f"{service.upper()}_PORT={port}\n"
        
        # Write .ports.env file
        ports_env_file = project_path / ".ports.env"
        with open(ports_env_file, 'w') as f:
            f.write(env_content)
        
        return assigned_ports

@click.group()
def cli():
    """Universal Port Manager - Central port management for all projects"""
    pass

@cli.command()
def status():
    """Show current port usage across system"""
    pm = PortManager()
    
    # Get all port information
    system_ports = pm.scan_system_ports()
    docker_services = pm.scan_docker_services()
    registered_ports = pm.registry["ports"]
    
    # Create status table
    table = Table(title="System Port Status", box=box.ROUNDED)
    table.add_column("Port", style="cyan", width=8)
    table.add_column("Project", style="green", width=20)
    table.add_column("Service", style="yellow", width=15)
    table.add_column("Process", style="blue", width=20)
    table.add_column("Status", style="magenta", width=10)
    
    # Add registered ports
    all_ports = set()
    for port, info in registered_ports.items():
        all_ports.add(int(port))
        process = "Not running"
        status = "Registered"
        
        if int(port) in system_ports:
            process = system_ports[int(port)]["process"]
            status = "Active"
        
        table.add_row(
            str(port),
            info["project"],
            info["service"],
            process,
            status
        )
    
    # Add system ports not in registry
    for port, info in system_ports.items():
        if port not in all_ports:
            table.add_row(
                str(port),
                "-",
                "-",
                info["process"],
                "System"
            )
    
    console.print(table)
    
    # Docker services info
    if docker_services:
        docker_table = Table(title="Docker Services", box=box.ROUNDED)
        docker_table.add_column("Container", style="cyan", width=20)
        docker_table.add_column("Image", style="green", width=25)
        docker_table.add_column("Ports", style="yellow", width=30)
        
        for service in docker_services:
            docker_table.add_row(
                service["name"],
                service["image"],
                service["ports"]
            )
        
        console.print(docker_table)

@cli.command()
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('--name', '-n', help='Project name (defaults to directory name)')
def init(project_path, name):
    """Initialize port configuration for a project"""
    pm = PortManager()
    project_path = Path(project_path).resolve()
    project_name = name or project_path.name
    
    console.print(f"[bold blue]Initializing ports for project: {project_name}[/bold blue]")
    
    # Generate port assignments
    assigned_ports = pm.generate_project_env(project_path, project_name)
    
    # Display assigned ports
    table = Table(title=f"Port Assignments for {project_name}", box=box.ROUNDED)
    table.add_column("Service", style="cyan", width=15)
    table.add_column("Port", style="green", width=10)
    
    for service, port in assigned_ports.items():
        table.add_row(service, str(port))
    
    console.print(table)
    console.print(f"[green]✓ Created .ports.env file in {project_path}[/green]")

@cli.command()
@click.argument('port', type=int)
def free(port):
    """Free up a port by killing the process using it"""
    try:
        # Find process using the port
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port and conn.status == 'LISTEN':
                process = psutil.Process(conn.pid)
                console.print(f"[yellow]Found process using port {port}:[/yellow]")
                console.print(f"  PID: {conn.pid}")
                console.print(f"  Process: {process.name()}")
                console.print(f"  Command: {' '.join(process.cmdline()[:3])}")
                
                if click.confirm("Kill this process?"):
                    process.kill()
                    console.print(f"[green]✓ Process killed, port {port} is now free[/green]")
                return
        
        console.print(f"[green]Port {port} is already free[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@cli.command()
def clean():
    """Clean up dead port registrations"""
    pm = PortManager()
    removed = pm.cleanup_dead_ports()
    console.print(f"[green]✓ Cleaned up {removed} dead port registrations[/green]")

@cli.command()
@click.argument('project')
def show(project):
    """Show ports assigned to a project"""
    pm = PortManager()
    ports = pm.get_project_ports(project)
    
    if not ports:
        console.print(f"[yellow]No ports registered for project: {project}[/yellow]")
        return
    
    table = Table(title=f"Ports for {project}", box=box.ROUNDED)
    table.add_column("Service", style="cyan", width=15)
    table.add_column("Port", style="green", width=10)
    
    for service, port in ports.items():
        table.add_row(service, str(port))
    
    console.print(table)

@cli.command()
def scan():
    """Scan current directory for port configurations"""
    pm = PortManager()
    project_path = Path.cwd()
    
    console.print(f"[bold blue]Scanning {project_path} for port configurations...[/bold blue]")
    
    ports_found = pm.scan_project_configs(project_path)
    
    table = Table(title="Port Configurations Found", box=box.ROUNDED)
    table.add_column("Source", style="cyan", width=20)
    table.add_column("Ports", style="green", width=40)
    
    for source, ports in ports_found.items():
        if ports:
            table.add_row(source, ", ".join(map(str, sorted(set(ports)))))
    
    console.print(table)

@cli.command()
@click.option('--all', '-a', is_flag=True, help='Export all projects')
@click.option('--project', '-p', help='Export specific project')
def export(all, project):
    """Export port configuration"""
    pm = PortManager()
    
    if all:
        data = pm.registry
    elif project:
        data = {
            "project": project,
            "ports": pm.get_project_ports(project)
        }
    else:
        # Export current project
        project_name = Path.cwd().name
        data = {
            "project": project_name,
            "ports": pm.get_project_ports(project_name)
        }
    
    console.print(json.dumps(data, indent=2))

if __name__ == "__main__":
    cli()