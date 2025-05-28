"""add_email_verification_table

Revision ID: 8c9b3b1f7202
Revises: 2098409c27ed
Create Date: 2025-05-28 20:01:12.934812+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime, timedelta
import secrets

# revision identifiers, used by Alembic.
revision = '8c9b3b1f7202'
down_revision = '2098409c27ed'
branch_labels = None
depends_on = None


def upgrade():
    # Create email_verifications table
    op.create_table(
        'email_verifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_used', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_email_verifications_id'), 'email_verifications', ['id'], unique=False)
    op.create_index(op.f('ix_email_verifications_token'), 'email_verifications', ['token'], unique=True)

    # Data migration for existing users
    connection = op.get_bind()
    
    # Get all unverified users
    users = connection.execute(
        sa.text("SELECT id, email FROM users WHERE is_verified = false")
    ).fetchall()
    
    # Create verification records for each unverified user
    for user in users:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        connection.execute(
            sa.text("""
                INSERT INTO email_verifications 
                (user_id, token, expires_at, is_used, created_at)
                VALUES (:user_id, :token, :expires_at, false, :created_at)
            """),
            {
                "user_id": user.id,
                "token": token,
                "expires_at": expires_at,
                "created_at": datetime.utcnow()
            }
        )


def downgrade():
    # Drop indexes
    op.drop_index(op.f('ix_email_verifications_token'), table_name='email_verifications')
    op.drop_index(op.f('ix_email_verifications_id'), table_name='email_verifications')
    
    # Drop table
    op.drop_table('email_verifications')
