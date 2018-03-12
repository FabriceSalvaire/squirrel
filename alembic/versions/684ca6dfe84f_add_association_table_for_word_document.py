"""Add assiocation table for document word

Revision ID: 684ca6dfe84f
Revises: 994b36bc48c9
Create Date: 2018-03-10 19:35:21.670675

"""

####################################################################################################

from alembic import op
import sqlalchemy as sa

####################################################################################################

# revision identifiers, used by Alembic.
revision = '684ca6dfe84f'
down_revision = '994b36bc48c9'
branch_labels = None
depends_on = None

####################################################################################################

def upgrade():

    op.create_table(
        'words',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('word', sa.String(), nullable=True),
        sa.Column('language', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.execute('INSERT INTO words(id, word, language) SELECT document_words.id, document_words.word, document_words.language FROM document_words')

    # document_words update
    with op.batch_alter_table('document_words') as batch_op:
        # batch_op.add_column(sa.Column('word_id', sa.Integer(), nullable=False))
        batch_op.alter_column('id', new_column_name='word_id')

        # document_words.word_id -> words.id
        batch_op.create_foreign_key('fk_word', 'words', ['word_id'], ['id'])

        batch_op.drop_column('language')
        batch_op.drop_column('word')
        # batch_op.drop_column('id')

    op.create_index(batch_op.f('ix_document_words_word_id'), 'document_words', ['word_id'], unique=False)

####################################################################################################

def downgrade():

    op.add_column('document_words', sa.Column('language', sa.INTEGER(), nullable=True))
    op.add_column('document_words', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('document_words', sa.Column('word', sa.VARCHAR(), nullable=True))
    op.drop_constraint(None, 'document_words', type_='foreignkey')
    op.drop_index(op.f('ix_document_words_word_id'), table_name='document_words')
    op.drop_column('document_words', 'word_id')
    op.drop_table('words')
