"""First version

Revision ID: 994b36bc48c9
Revises: 
Create Date: 2018-03-10 14:47:34.119147

"""

####################################################################################################

from alembic import op
import sqlalchemy as sa

import Babel

####################################################################################################

# revision identifiers, used by Alembic.
revision = '994b36bc48c9'
down_revision = None
branch_labels = None
depends_on = None

####################################################################################################

def upgrade():

    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('record_creation_date', sa.DateTime(), nullable=True),
        sa.Column('record_update_date', sa.DateTime(), nullable=True),
        sa.Column('shasum', sa.String(length=64), nullable=True),
        sa.Column('has_duplicate', sa.Boolean(), nullable=True),
        sa.Column('path', Babel.DataBase.DocumentDataBase.Types.FileType(), nullable=True),
        sa.Column('inode', sa.Integer(), nullable=True),
        sa.Column('author', sa.String(), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=True),
        sa.Column('number_of_pages', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('keywords', sa.String(), nullable=True),
        sa.Column('star', sa.Integer(), nullable=True),
        sa.Column('dewey', sa.Float(), nullable=True),
        sa.Column('indexation_date', sa.DateTime(), nullable=True),
        sa.Column('indexed_until', sa.Integer(), nullable=True),
        sa.Column('indexation_status', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('path')
    )

    op.create_table(
        'document_words',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('language', sa.Integer(), nullable=True),
        sa.Column('word', sa.String(), nullable=True),
        sa.Column('count', sa.Integer(), nullable=True),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_document_words_document_id'), 'document_words', ['document_id'], unique=False)

####################################################################################################

def downgrade():

    op.drop_index(op.f('ix_document_words_document_id'), table_name='document_words')
    op.drop_table('document_words')
    op.drop_table('documents')
