"""create post table

Revision ID: 0219a758e111
Revises: 
Create Date: 2025-08-14 18:37:48.336013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
# if we want to add a migration to our database we could use
# alembic revision -m "create_post_table

# and if we want to migrate these revisions
# we do: alembic upgrade [name_of_revision_variable]

revision: str = '0219a758e111'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
