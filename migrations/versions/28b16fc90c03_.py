"""empty message

Revision ID: 28b16fc90c03
Revises: 32cca66098a5
Create Date: 2022-05-10 22:36:31.464246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28b16fc90c03'
down_revision = '32cca66098a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('poke_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('base_experience', sa.Integer(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('defense', sa.Integer(), nullable=True),
    sa.Column('ability', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('poke_id')
    )
    op.create_table('pokemon_user',
    sa.Column('poke_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['poke_id'], ['pokemon.poke_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('poke_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon_user')
    op.drop_table('pokemon')
    # ### end Alembic commands ###
