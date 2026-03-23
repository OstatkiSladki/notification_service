CREATE SCHEMA IF NOT EXISTS "notification";

CREATE TABLE IF NOT EXISTS "notification"."notifications" (
    "id" BIGSERIAL PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    "title" VARCHAR(255),
    "message" TEXT NOT NULL,
    "data_json" JSONB DEFAULT '{}',
    "is_read" BOOLEAN DEFAULT FALSE,
    "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "read_at" TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS "notifications_idx_user"
    ON "notification"."notifications" ("user_id", "is_read");

CREATE INDEX IF NOT EXISTS "notifications_idx_created"
    ON "notification"."notifications" ("created_at");
