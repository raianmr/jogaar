"""add images table

Revision ID: 79a6909c612a
Revises: dce10f3771bf
Create Date: 2022-11-22 18:08:19.906902

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "79a6909c612a"
down_revision = "dce10f3771bf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("uploader_id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("filetype", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["uploader_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("images")
    # ### end Alembic commands ###
