"""update exercise logs for progression engine

Revision ID: 21efe6226f7e
Revises: e2a9c24b5be5
Create Date: 2026-07-08 16:04:06.653711

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "21efe6226f7e"
down_revision: Union[str, Sequence[str], None] = "e2a9c24b5be5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Planned workout
    op.add_column(
        "exercise_logs",
        sa.Column(
            "planned_sets",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "exercise_logs",
        sa.Column(
            "planned_reps",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "exercise_logs",
        sa.Column(
            "planned_weight",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    # Exercise status
    op.add_column(
        "exercise_logs",
        sa.Column(
            "completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.add_column(
        "exercise_logs",
        sa.Column(
            "skipped",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    # Notes
    op.add_column(
        "exercise_logs",
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
        ),
    )

    # Audit timestamps
    op.add_column(
        "exercise_logs",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.add_column(
        "exercise_logs",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # Remove temporary defaults
    op.alter_column(
        "exercise_logs",
        "planned_sets",
        server_default=None,
    )

    op.alter_column(
        "exercise_logs",
        "planned_reps",
        server_default=None,
    )

    op.alter_column(
        "exercise_logs",
        "planned_weight",
        server_default=None,
    )

    op.alter_column(
        "exercise_logs",
        "completed",
        server_default=None,
    )

    op.alter_column(
        "exercise_logs",
        "skipped",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("exercise_logs", "updated_at")
    op.drop_column("exercise_logs", "created_at")
    op.drop_column("exercise_logs", "notes")
    op.drop_column("exercise_logs", "skipped")
    op.drop_column("exercise_logs", "completed")
    op.drop_column("exercise_logs", "planned_weight")
    op.drop_column("exercise_logs", "planned_reps")
    op.drop_column("exercise_logs", "planned_sets")