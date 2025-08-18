"""add content column to posts table

Revision ID: e632d62a4774
Revises: 0219a758e111
Create Date: 2025-08-18 12:22:26.525084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e632d62a4774'
down_revision: Union[str, Sequence[str], None] = '0219a758e111'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# alembic heads -> shows all the new versions that are ahead of the revision
# that we are currently in

# if we want to downgrade we could do
# alembic downgrade [name_of_revision_variable] / -1 (number of revision we would like to go back)
# it could be -1 or -2, depends on how many revisions we have

def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
