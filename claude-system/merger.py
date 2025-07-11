#!/usr/bin/env python3
"""
CLAUDE.md Merger - Intelligently merges 3-tier template system
"""

import os
import re
import yaml
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Section:
    """Represents a section in CLAUDE.md"""
    title: str
    content: str
    level: int = 1
    source: str = 'universal'  # 'universal', 'company', 'project', 'developer'
    checksum: str = ''
    override_allowed: bool = True
    metadata: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.checksum:
            self.checksum = hashlib.md5(self.content.encode()).hexdigest()

class ClaudeMerger:
    """Merges multiple tiers of CLAUDE.md templates"""
    
    def __init__(self, project_path: str = '.'):
        self.project_path = Path(project_path)
        self.claude_system_path = Path.home() / '.claude-templates' / 'claude-system'
        self.sections: Dict[str, Section] = {}
        self.config = self._load_configs()
        
    def _load_configs(self) -> Dict:
        """Load all configuration files"""
        configs = {}
        
        # Load system config
        system_config_path = self.claude_system_path / 'config.yaml'
        if system_config_path.exists():
            configs['system'] = yaml.safe_load(open(system_config_path))
            
        # Load company config
        company_config_path = self.project_path / '.claude-company' / 'config.yaml'
        if company_config_path.exists():
            configs['company'] = yaml.safe_load(open(company_config_path))
            
        # Load project config
        project_config_path = self.project_path / '.claude-project' / 'config.yaml'
        if project_config_path.exists():
            configs['project'] = yaml.safe_load(open(project_config_path))
            
        return configs
    
    def parse_markdown_sections(self, content: str, source: str) -> List[Section]:
        """Parse markdown content into sections"""
        sections = []
        
        # Split by headers
        pattern = r'^(#{1,6})\s+(.+)$'
        parts = re.split(pattern, content, flags=re.MULTILINE)
        
        # Process sections
        i = 1  # Skip initial empty part
        while i < len(parts) - 2:
            level = len(parts[i])
            title = parts[i + 1].strip()
            
            # Find content until next header
            content_start = i + 2
            content_end = content_start + 1
            
            # Collect content until next section
            section_content = parts[content_start] if content_start < len(parts) else ''
            
            sections.append(Section(
                title=title,
                content=section_content.strip(),
                level=level,
                source=source
            ))
            
            i += 3
            
        return sections
    
    def load_universal_base(self) -> Dict[str, Section]:
        """Load Tier 1: Universal base templates"""
        base_sections = {}
        
        # Load core template
        core_path = self.claude_system_path / 'base' / 'core.md'
        if core_path.exists():
            content = core_path.read_text()
            sections = self.parse_markdown_sections(content, 'universal')
            for section in sections:
                base_sections[section.title] = section
                
        # Load language-specific templates
        languages_dir = self.claude_system_path / 'base' / 'languages'
        if languages_dir.exists():
            for lang_file in languages_dir.glob('*.md'):
                content = lang_file.read_text()
                sections = self.parse_markdown_sections(content, 'universal')
                for section in sections:
                    section.metadata['language'] = lang_file.stem
                    key = f"{lang_file.stem}:{section.title}"
                    base_sections[key] = section
                    
        return base_sections
    
    def apply_company_overrides(self, base_sections: Dict[str, Section]) -> Dict[str, Section]:
        """Apply Tier 2: Company-specific overrides"""
        sections = base_sections.copy()
        
        # Load company standards
        company_dir = self.project_path / '.claude-company'
        if not company_dir.exists():
            return sections
            
        # Process company standards
        standards_path = company_dir / 'standards.md'
        if standards_path.exists():
            content = standards_path.read_text()
            company_sections = self.parse_markdown_sections(content, 'company')
            
            for section in company_sections:
                if section.title in sections:
                    # Override existing section
                    logger.info(f"Company override: {section.title}")
                    sections[section.title] = section
                else:
                    # Add new company section
                    sections[section.title] = section
                    
        # Apply role-based filtering if configured
        if 'company' in self.config and 'roles' in self.config['company']:
            sections = self._apply_role_filters(sections)
            
        return sections
    
    def apply_project_customizations(self, sections: Dict[str, Section]) -> Dict[str, Section]:
        """Apply Tier 3: Project-specific customizations"""
        project_sections = sections.copy()
        
        # Load project overrides
        project_dir = self.project_path / '.claude-project'
        if project_dir.exists():
            overrides_path = project_dir / 'overrides.md'
            if overrides_path.exists():
                content = overrides_path.read_text()
                custom_sections = self.parse_markdown_sections(content, 'project')
                
                for section in custom_sections:
                    # Check if override is allowed
                    if section.title in project_sections:
                        existing = project_sections[section.title]
                        if not existing.override_allowed and existing.source == 'company':
                            logger.warning(f"Cannot override company policy: {section.title}")
                            continue
                            
                    project_sections[section.title] = section
                    
        return project_sections
    
    def apply_developer_preferences(self, sections: Dict[str, Section], username: str) -> Dict[str, Section]:
        """Apply individual developer preferences"""
        dev_sections = sections.copy()
        
        # Check if developer customization is enabled
        if not self.config.get('project', {}).get('developer_overrides', {}).get('enabled'):
            return dev_sections
            
        # Load developer preferences
        dev_file = self.project_path / '.claude-project' / 'developer' / f'{username}.md'
        if dev_file.exists():
            content = dev_file.read_text()
            dev_custom = self.parse_markdown_sections(content, 'developer')
            
            for section in dev_custom:
                # Developers can only override project-level sections
                if section.title in dev_sections:
                    existing = dev_sections[section.title]
                    if existing.source in ['universal', 'company']:
                        logger.warning(f"Developer cannot override {existing.source} section: {section.title}")
                        continue
                        
                dev_sections[section.title] = section
                
        return dev_sections
    
    def _apply_role_filters(self, sections: Dict[str, Section]) -> Dict[str, Section]:
        """Filter sections based on developer role"""
        role = self.config.get('project', {}).get('primary_role', 'fullstack')
        role_config = self.config.get('company', {}).get('roles', {}).get(role, {})
        
        if not role_config:
            return sections
            
        filtered = {}
        
        # Apply exclusions
        exclude_sections = role_config.get('exclude_sections', [])
        for key, section in sections.items():
            skip = False
            for exclude in exclude_sections:
                if exclude in section.title.lower():
                    skip = True
                    break
            if not skip:
                filtered[key] = section
                
        return filtered
    
    def generate_claude_md(self, sections: Dict[str, Section]) -> str:
        """Generate final CLAUDE.md content"""
        output = []
        
        # Add header
        output.append(f"# CLAUDE.md - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        output.append("*This file is auto-generated from 3-tier template system. Do not edit directly.*")
        output.append("")
        
        # Group sections by level
        sorted_sections = sorted(sections.values(), key=lambda s: (s.level, s.title))
        
        for section in sorted_sections:
            # Add section header
            header = '#' * section.level + ' ' + section.title
            output.append(header)
            output.append("")
            
            # Add content
            if section.content:
                output.append(section.content)
                output.append("")
                
            # Add metadata comment if in debug mode
            if os.getenv('CLAUDE_DEBUG'):
                output.append(f"<!-- Source: {section.source}, Checksum: {section.checksum} -->")
                output.append("")
                
        return '\n'.join(output)
    
    def analyze_changes(self, sections_before: Dict[str, Section], sections_after: Dict[str, Section]) -> Dict[str, any]:
        """Analyze what changed between two section sets"""
        changes = {
            'added': [],
            'removed': [],
            'modified': [],
            'conflicts': [],
            'policy_violations': []
        }
        
        # Find added sections
        for key in sections_after:
            if key not in sections_before:
                changes['added'].append({
                    'section': key,
                    'source': sections_after[key].source,
                    'title': sections_after[key].title
                })
        
        # Find removed sections
        for key in sections_before:
            if key not in sections_after:
                changes['removed'].append({
                    'section': key,
                    'source': sections_before[key].source,
                    'title': sections_before[key].title
                })
        
        # Find modified sections
        for key in sections_after:
            if key in sections_before:
                if sections_after[key].checksum != sections_before[key].checksum:
                    changes['modified'].append({
                        'section': key,
                        'source_before': sections_before[key].source,
                        'source_after': sections_after[key].source,
                        'title': sections_after[key].title
                    })
        
        # Check for policy violations
        if 'company' in self.config:
            policies = self.config['company'].get('policies', {})
            for key, section in sections_after.items():
                if section.source == 'project' and key in sections_before:
                    original = sections_before[key]
                    if original.source == 'company' and not original.override_allowed:
                        changes['policy_violations'].append({
                            'section': key,
                            'policy': 'Cannot override company policy',
                            'attempted_by': section.source
                        })
        
        return changes
    
    def generate_dry_run_report(self, changes: Dict[str, any], content: str) -> str:
        """Generate a detailed dry-run report"""
        report = []
        report.append("=" * 60)
        report.append("CLAUDE.md DRY RUN REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append("SUMMARY")
        report.append("-" * 20)
        report.append(f"✅ Added sections: {len(changes['added'])}")
        report.append(f"❌ Removed sections: {len(changes['removed'])}")
        report.append(f"📝 Modified sections: {len(changes['modified'])}")
        report.append(f"⚠️  Conflicts: {len(changes['conflicts'])}")
        report.append(f"🚫 Policy violations: {len(changes['policy_violations'])}")
        report.append("")
        
        # Details
        if changes['added']:
            report.append("ADDED SECTIONS")
            report.append("-" * 20)
            for item in changes['added']:
                report.append(f"+ {item['title']} (from: {item['source']})")
            report.append("")
        
        if changes['removed']:
            report.append("REMOVED SECTIONS")
            report.append("-" * 20)
            for item in changes['removed']:
                report.append(f"- {item['title']} (was from: {item['source']})")
            report.append("")
        
        if changes['modified']:
            report.append("MODIFIED SECTIONS")
            report.append("-" * 20)
            for item in changes['modified']:
                report.append(f"~ {item['title']}")
                report.append(f"  Before: {item['source_before']}")
                report.append(f"  After: {item['source_after']}")
            report.append("")
        
        if changes['policy_violations']:
            report.append("⚠️  POLICY VIOLATIONS")
            report.append("-" * 20)
            for violation in changes['policy_violations']:
                report.append(f"❌ Section: {violation['section']}")
                report.append(f"   Policy: {violation['policy']}")
                report.append(f"   Attempted by: {violation['attempted_by']}")
            report.append("")
        
        # Preview
        report.append("PREVIEW (first 50 lines)")
        report.append("-" * 20)
        preview_lines = content.split('\n')[:50]
        report.extend(preview_lines)
        if len(content.split('\n')) > 50:
            report.append("... (truncated)")
        
        return '\n'.join(report)
    
    def merge(self, username: Optional[str] = None, dry_run: bool = False) -> str:
        """Main merge function with dry-run support"""
        logger.info(f"Starting CLAUDE.md merge process (dry_run={dry_run})...")
        
        # Load universal base for comparison
        sections_original = self.load_universal_base()
        logger.info(f"Loaded {len(sections_original)} universal sections")
        
        # Apply all tiers
        sections = sections_original.copy()
        sections = self.apply_company_overrides(sections)
        logger.info(f"After company overrides: {len(sections)} sections")
        
        sections = self.apply_project_customizations(sections)
        logger.info(f"After project customizations: {len(sections)} sections")
        
        if username:
            sections = self.apply_developer_preferences(sections, username)
            logger.info(f"After developer preferences: {len(sections)} sections")
        
        # Generate final content
        content = self.generate_claude_md(sections)
        
        if dry_run:
            # Analyze changes
            changes = self.analyze_changes(sections_original, sections)
            
            # Generate report
            report = self.generate_dry_run_report(changes, content)
            
            # Save report to file
            report_path = self.project_path / '.claude-project' / 'dry-run-report.txt'
            report_path.parent.mkdir(exist_ok=True)
            report_path.write_text(report)
            
            # Also save preview
            preview_path = self.project_path / '.claude-project' / 'CLAUDE.md.preview'
            preview_path.write_text(content)
            
            logger.info(f"Dry run complete. Report saved to {report_path}")
            logger.info(f"Preview saved to {preview_path}")
            
            # Print summary to console
            print("\n" + "=" * 60)
            print("DRY RUN SUMMARY")
            print("=" * 60)
            print(f"✅ Added sections: {len(changes['added'])}")
            print(f"❌ Removed sections: {len(changes['removed'])}")
            print(f"📝 Modified sections: {len(changes['modified'])}")
            print(f"⚠️  Policy violations: {len(changes['policy_violations'])}")
            print(f"\nFull report: {report_path}")
            print(f"Preview file: {preview_path}")
            
            if changes['policy_violations']:
                print("\n⚠️  WARNING: Policy violations detected!")
                print("The merge cannot proceed with these violations.")
            
            return report
        else:
            # Check for policy violations before saving
            changes = self.analyze_changes(sections_original, sections)
            if changes['policy_violations']:
                logger.error("Policy violations detected. Merge aborted.")
                for violation in changes['policy_violations']:
                    logger.error(f"  - {violation['section']}: {violation['policy']}")
                raise ValueError("Policy violations prevent merge. Run with --dry-run to see details.")
            
            # Save to file
            output_path = self.project_path / 'CLAUDE.md'
            
            # Backup existing file if it exists
            if output_path.exists():
                backup_path = output_path.with_suffix('.md.backup')
                output_path.rename(backup_path)
                logger.info(f"Backed up existing CLAUDE.md to {backup_path}")
            
            output_path.write_text(content)
            logger.info(f"Generated CLAUDE.md at {output_path}")
            
            return content

def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Merge CLAUDE.md templates')
    parser.add_argument('--project', default='.', help='Project directory')
    parser.add_argument('--username', help='Developer username for preferences')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying them')
    parser.add_argument('--force', action='store_true', help='Force merge even with policy violations (NOT RECOMMENDED)')
    
    args = parser.parse_args()
    
    if args.debug:
        os.environ['CLAUDE_DEBUG'] = '1'
        logging.getLogger().setLevel(logging.DEBUG)
        
    merger = ClaudeMerger(args.project)
    
    try:
        merger.merge(args.username, dry_run=args.dry_run)
    except ValueError as e:
        if args.force:
            logger.warning("Force flag detected. Proceeding despite policy violations...")
            # Note: In production, this should require additional authentication
            merger.merge(args.username, dry_run=False)
        else:
            logger.error(str(e))
            sys.exit(1)

if __name__ == '__main__':
    main()