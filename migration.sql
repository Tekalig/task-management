-- Migration script: creates the Task Management database and tables.
-- Run with: mysql -u root -p < migration.sql

CREATE DATABASE IF NOT EXISTS task_management
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE task_management;

-- ------------------------------------------------------------------
-- Users table
-- ------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id               INT           NOT NULL AUTO_INCREMENT,
    username         VARCHAR(50)   NOT NULL,
    email            VARCHAR(100)  NOT NULL,
    hashed_password  VARCHAR(255)  NOT NULL,
    is_active        TINYINT(1)    NOT NULL DEFAULT 1,
    created_at       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_email    (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------
-- Tasks table
-- ------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    id            INT          NOT NULL AUTO_INCREMENT,
    title         VARCHAR(200) NOT NULL,
    description   TEXT,
    is_completed  TINYINT(1)   NOT NULL DEFAULT 0,
    owner_id      INT          NOT NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                               ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_tasks_owner FOREIGN KEY (owner_id)
        REFERENCES users (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
