#!/usr/bin/env python3
import os
import sys
import click
from alembic.config import Config
from alembic import command

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@click.group()
def cli():
    """Database migration management script."""
    pass

@cli.command()
@click.option('--message', '-m', required=True, help='Migration message')
def create(message):
    """Create a new migration."""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, message=message, autogenerate=True)

@cli.command()
def upgrade():
    """Upgrade database to the latest version."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@cli.command()
@click.option('--revision', '-r', required=True, help='Revision to downgrade to')
def downgrade(revision):
    """Downgrade database to a specific revision."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, revision)

@cli.command()
def history():
    """Show migration history."""
    alembic_cfg = Config("alembic.ini")
    command.history(alembic_cfg)

@cli.command()
def current():
    """Show current database version."""
    alembic_cfg = Config("alembic.ini")
    command.current(alembic_cfg)

if __name__ == '__main__':
    cli() 