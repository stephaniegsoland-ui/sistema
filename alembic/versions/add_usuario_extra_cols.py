"""add usuario extra columns

Revision ID: add_usuario_extra_cols
Revises: 14c6100b8513
Create Date: 2026-06-02 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'add_usuario_extra_cols'
down_revision: Union[str, Sequence[str], None] = '14c6100b8513'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add extra usuario columns."""
    # Add string/text columns with safe defaults so existing rows are fine
    op.add_column('usuario', sa.Column('telefono', sqlmodel.sql.sqltypes.AutoString(), nullable=True, server_default=''))
    op.add_column('usuario', sa.Column('direccion', sqlmodel.sql.sqltypes.AutoString(), nullable=True, server_default=''))
    op.add_column('usuario', sa.Column('notas', sqlmodel.sql.sqltypes.AutoString(), nullable=True, server_default=''))
    op.add_column('usuario', sa.Column('cv_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True, server_default=''))
    op.add_column('usuario', sa.Column('foto_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True, server_default=''))
    op.add_column('usuario', sa.Column('vehiculo_asignado', sqlmodel.sql.sqltypes.AutoString(), nullable=True, server_default=''))


def downgrade() -> None:
    """Downgrade schema: drop the added columns."""
    op.drop_column('usuario', 'vehiculo_asignado')
    op.drop_column('usuario', 'foto_url')
    op.drop_column('usuario', 'cv_url')
    op.drop_column('usuario', 'notas')
    op.drop_column('usuario', 'direccion')
    op.drop_column('usuario', 'telefono')
