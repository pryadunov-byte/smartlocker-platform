"""Initial database schema."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("geo_lat", sa.Float(), nullable=True),
        sa.Column("geo_lon", sa.Float(), nullable=True),
        sa.Column("status_online", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("firmware", sa.String(length=128), nullable=True),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("addr", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("baud", sa.Integer(), nullable=False, server_default="19200"),
        sa.Column("max_boards", sa.Integer(), nullable=False, server_default="16"),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default=sa.text("'{}'::jsonb")),
    )

    op.create_table(
        "scenarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False, unique=True),
        sa.Column("params_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role", sa.Enum("administrator", "operator", "technician", "courier", "analyst", "client", name="userrole"), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
    )

    op.create_table(
        "locker_cells",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("device_id", sa.Integer(), sa.ForeignKey("devices.id", ondelete="CASCADE")),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("size", sa.String(length=32), nullable=False),
        sa.Column("status", sa.Enum("free", "occupied", "fault", "dirty", "open", name="lockercellstatus"), nullable=False, server_default="free"),
        sa.Column("cooled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("needs_repair", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("open", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("flags", postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default=sa.text("'{}'::jsonb")),
        sa.Column("services_enabled", postgresql.ARRAY(sa.String()), nullable=False, server_default=sa.text("'{}'::text[]")),
    )

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("device_id", sa.Integer(), sa.ForeignKey("devices.id", ondelete="CASCADE")),
        sa.Column("severity", sa.Enum("info", "warning", "critical", name="alertseverity"), nullable=False),
        sa.Column("kind", sa.Enum("offline", "lock_fault", "overheat", "dirty", "capacity", "other", name="alertkind"), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("public_uid", sa.String(length=64), nullable=False, unique=True),
        sa.Column("device_id", sa.Integer(), sa.ForeignKey("devices.id")),
        sa.Column("cell_id", sa.Integer(), sa.ForeignKey("locker_cells.id"), nullable=True),
        sa.Column("type", sa.Enum("delivery", "return", "rent", "storage", name="ordertype"), nullable=False),
        sa.Column("status", sa.Enum("created", "awaiting_pickup", "picked_up", "overdue", "returned", "cancelled", name="orderstatus"), nullable=False, server_default="created"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("picked_up_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("returned_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scenario_id", sa.Integer(), sa.ForeignKey("scenarios.id"), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default=sa.text("'{}'::jsonb")),
    )

    op.create_table(
        "access_codes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id", ondelete="CASCADE"), unique=True),
        sa.Column("pin_hash", sa.String(length=128), nullable=False),
        sa.Column("qr_token", sa.String(length=256), nullable=False),
        sa.Column("attempts_left", sa.Integer(), nullable=False, server_default="3"),
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id", ondelete="CASCADE")),
        sa.Column("channel", sa.Enum("sms", "email", "telegram", name="notificationchannel"), nullable=False),
        sa.Column("template_key", sa.String(length=50), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.Enum("sent", "failed", "queued", name="notificationstatus"), nullable=False, server_default="queued"),
        sa.Column("cost", sa.Float(), nullable=True),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("entity", sa.String(length=128), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("notifications")
    op.drop_table("access_codes")
    op.drop_table("orders")
    op.drop_table("alerts")
    op.drop_table("locker_cells")
    op.drop_table("users")
    op.drop_table("scenarios")
    op.drop_table("devices")
