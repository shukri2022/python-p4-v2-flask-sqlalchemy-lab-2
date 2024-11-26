"""Make customer_id and item_id nullable in Review

Revision ID: 56b6bc638bb4
Revises: 5077fea76be9
Create Date: 2024-11-26 18:01:18.991393

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "56b6bc638bb4"
down_revision = "5077fea76be9"
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table with the updated schema
    op.create_table(
        "new_reviews",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("comment", sa.String, nullable=False),
        sa.Column(
            "customer_id", sa.Integer, sa.ForeignKey("customers.id"), nullable=True
        ),
        sa.Column("item_id", sa.Integer, sa.ForeignKey("items.id"), nullable=True),
    )

    # Copy data from the old table to the new table
    op.execute(
        "INSERT INTO new_reviews (id, comment, customer_id, item_id) SELECT id, comment, customer_id, item_id FROM reviews"
    )

    # Drop the old table
    op.drop_table("reviews")

    # Rename the new table to replace the old table
    op.rename_table("new_reviews", "reviews")


def downgrade():
    # Reverse the changes in downgrade
    op.create_table(
        "old_reviews",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("comment", sa.String, nullable=False),
        sa.Column(
            "customer_id", sa.Integer, sa.ForeignKey("customers.id"), nullable=False
        ),
        sa.Column("item_id", sa.Integer, sa.ForeignKey("items.id"), nullable=False),
    )

    # Copy data back from the new table to the old table
    op.execute(
        "INSERT INTO old_reviews (id, comment, customer_id, item_id) SELECT id, comment, customer_id, item_id FROM reviews"
    )

    # Drop the new table
    op.drop_table("reviews")

    # Rename the old table back to its original name
    op.rename_table("old_reviews", "reviews")
