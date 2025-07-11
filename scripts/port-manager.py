#!/usr/bin/env python3
"""
Universal Port Manager - Simplified version for Claude templates
Single source of truth for all project ports
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import click

# Global port registry location
REGISTRY_FILE = Path.home() / ".config" / "port-manager" / "registry.json"
REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)

# Port ranges by service type
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

def load_registry():
    """Load the global port registry"""
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, 'r') as f:
            return json.load(f)
    return {"ports": {}, "projects": {}}

def save_registry(registry):
    """Save the global port registry"""
    with open(REGISTRY_FILE, 'w') as f:
        json.dump(registry, f, indent=2)

def get_used_ports():
    """Get all ports currently in use on the system"""
    used_ports = set()
    
    # Check with lsof
    try:
        result = subprocess.run(
            ["lsof", "-i", "-P", "-n"],
            capture_output=True,
            text=True
        )
        for line in result.stdout.split('\n')[1:]:
            parts = line.split()
            if len(parts) > 8 and 'LISTEN' in line:
                port_info = parts[8]
                if ':' in port_info:
                    port = port_info.split(':')[-1]
                    try:
                        used_ports.add(int(port))
                    except ValueError:
                        pass
    except:
        pass
    
    # Also check our registry
    registry = load_registry()
    for port in registry["ports"]:
        used_ports.add(int(port))
    
    return used_ports

def find_available_port(service_type="misc", preferred=None):
    """Find an available port for a service type"""
    used_ports = get_used_ports()
    
    # Try preferred port first
    if preferred and preferred not in used_ports:
        return preferred
    
    # Get range for service type
    start, end = PORT_RANGES.get(service_type, PORT_RANGES["misc"])
    
    # Find first available
    for port in range(start, end + 1):
        if port not in used_ports:
            return port
    
    raise ValueError(f"No available ports in {service_type} range")

def init_project(project_path="."):
    """Initialize ports for a project"""
    project_path = Path(project_path).resolve()
    project_name = project_path.name
    
    print(f"🚀 Initializing ports for: {project_name}")
    
    # Common services
    services = {
        "web": "web",
        "api": "api",
        "db": "db",
        "redis": "cache",
        "temporal": "temporal",
        "docs": "misc",
        "metrics": "monitoring"
    }
    
    registry = load_registry()
    if project_name not in registry["projects"]:
        registry["projects"][project_name] = {}
    
    # Create .ports.env
    env_lines = [
        f"# Port configuration for {project_name}",
        f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    
    assigned = {}
    for service, service_type in services.items():
        # Check if already assigned
        if service in registry["projects"][project_name]:
            port = registry["projects"][project_name][service]
        else:
            port = find_available_port(service_type)
            registry["projects"][project_name][service] = port
            registry["ports"][str(port)] = {
                "project": project_name,
                "service": service
            }
        
        assigned[service] = port
        env_lines.append(f"{service.upper()}_PORT={port}")
    
    # Save registry
    save_registry(registry)
    
    # Write .ports.env
    ports_env = project_path / ".ports.env"
    with open(ports_env, 'w') as f:
        f.write('\n'.join(env_lines))
    
    print(f"✅ Created .ports.env")
    print("\nAssigned ports:")
    for service, port in assigned.items():
        print(f"  {service}: {port}")
    
    return assigned

@click.group()
def cli():
    """Universal Port Manager"""
    pass

@cli.command()
def status():
    """Show all registered ports"""
    registry = load_registry()
    used_ports = get_used_ports()
    
    print("🔍 Port Status\n")
    print("Project          Service    Port    Status")
    print("-" * 45)
    
    for port_str, info in sorted(registry["ports"].items(), key=lambda x: int(x[0])):
        port = int(port_str)
        status = "🟢 Active" if port in used_ports else "⚪ Registered"
        print(f"{info['project']:<15} {info['service']:<10} {port:<7} {status}")

@cli.command()
@click.argument('path', default='.')
def init(path):
    """Initialize ports for a project"""
    init_project(path)

@cli.command()
@click.argument('port', type=int)
def free(port):
    """Free a port by killing the process"""
    try:
        result = subprocess.run(f"lsof -ti:{port} | xargs kill -9", shell=True)
        print(f"✅ Port {port} is now free")
    except:
        print(f"❌ Could not free port {port}")

@cli.command()
@click.argument('project', required=False)
def show(project):
    """Show ports for a project"""
    registry = load_registry()
    
    if not project:
        project = Path.cwd().name
    
    if project in registry["projects"]:
        print(f"\n📦 Ports for {project}:\n")
        for service, port in registry["projects"][project].items():
            print(f"  {service}: {port}")
    else:
        print(f"❌ No ports registered for {project}")

@cli.command()
@click.option('--type', '-t', default='misc', help='Service type')
@click.option('--preferred', '-p', type=int, help='Preferred port')
def get_port(type, preferred):
    """Get next available port"""
    port = find_available_port(type, preferred)
    print(port)

@cli.command()
def clean():
    """Clean up unused port registrations"""
    registry = load_registry()
    used_ports = get_used_ports()
    
    # Find dead registrations
    dead_ports = []
    for port_str in registry["ports"]:
        if int(port_str) not in used_ports:
            dead_ports.append(port_str)
    
    # Remove dead ports
    for port in dead_ports:
        info = registry["ports"][port]
        del registry["ports"][port]
        
        # Remove from project
        project = info["project"]
        service = info["service"]
        if project in registry["projects"] and service in registry["projects"][project]:
            del registry["projects"][project][service]
    
    save_registry(registry)
    print(f"✅ Cleaned {len(dead_ports)} dead port registrations")

# Quick check function for scripts
def check_ports_for_project():
    """Quick function to check ports for current project"""
    project = Path.cwd().name
    registry = load_registry()
    
    if project in registry["projects"]:
        return registry["projects"][project]
    else:
        # Auto-initialize if not found
        return init_project(".")

if __name__ == "__main__":
    cli()