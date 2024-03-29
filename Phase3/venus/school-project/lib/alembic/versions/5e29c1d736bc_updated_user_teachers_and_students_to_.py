"""Updated User, Teachers and Students to use inheritance from User class

Revision ID: 5e29c1d736bc
Revises: 999c4e4a66a7
Create Date: 2024-03-29 05:10:21.225732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e29c1d736bc'
down_revision: Union[str, None] = '999c4e4a66a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Drop the existing temp_students table if it exists
    op.drop_table('temp_students')

    # Recreate temp_students table
    op.create_table('temp_students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('roll_number', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    
    # ### commands auto generated by Alembic - please adjust! ###
    # Drop the existing temp_teachers table if it exists
    op.drop_table('temp_teachers')

    # Recreate temp_teachers table
    op.create_table('temp_teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    # Copy data from existing tables to temporary tables
    op.execute('INSERT INTO temp_students (id, name, roll_number) SELECT id, name, roll_number FROM students')
    op.execute('INSERT INTO temp_teachers (id, name, email) SELECT id, name, email FROM teachers')

    # Drop existing tables
    op.drop_table('students')
    op.drop_table('teachers')

    # Rename temporary tables to original names
    op.rename_table('temp_students', 'students')
    op.rename_table('temp_teachers', 'teachers')
    # ### end Alembic commands ###
