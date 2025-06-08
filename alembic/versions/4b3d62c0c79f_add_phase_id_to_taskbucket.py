"""add phase_id to Taskbucket

Revision ID: 4b3d62c0c79f
Revises: 53e5ee25d8f0
Create Date: 2025-06-08 23:32:36.486695
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b3d62c0c79f'
down_revision: Union[str, None] = '53e5ee25d8f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create task_buckets table
    op.create_table(
        'task_buckets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('phase_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['phase_id'], ['project_phases.id'], name='fk_task_buckets_phase_id'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_buckets_id'), 'task_buckets', ['id'], unique=False)

    # Add columns to tasks table using batch mode (SQLite-safe)
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('task_bucket_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('order', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_tasks_task_bucket_id', 'task_buckets', ['task_bucket_id'], ['id'])


def downgrade() -> None:
    # Drop columns from tasks table using batch mode (SQLite-safe)
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_constraint('fk_tasks_task_bucket_id', type_='foreignkey')
        batch_op.drop_column('order')
        batch_op.drop_column('task_bucket_id')

    op.drop_index(op.f('ix_task_buckets_id'), table_name='task_buckets')
    op.drop_table('task_buckets')
