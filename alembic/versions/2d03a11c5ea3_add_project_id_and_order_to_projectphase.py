"""Add project_id and order to ProjectPhase

Revision ID: 2d03a11c5ea3
Revises: 4b3d62c0c79f
Create Date: 2025-06-09 11:46:00.475644
"""

from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union

# Revision identifiers, used by Alembic.
revision: str = '2d03a11c5ea3'
down_revision: Union[str, None] = '4b3d62c0c79f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema using batch operations compatible with SQLite."""
    with op.batch_alter_table("project_phases") as batch_op:
        batch_op.add_column(sa.Column("project_id", sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column("order", sa.Integer(), nullable=False))
        batch_op.create_foreign_key("fk_project_phases_project_id", "projects", ["project_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema using batch operations."""
    with op.batch_alter_table("project_phases") as batch_op:
        batch_op.drop_constraint("fk_project_phases_project_id", type_="foreignkey")
        batch_op.drop_column("order")
        batch_op.drop_column("project_id")
