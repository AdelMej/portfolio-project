# Auth Database Functions

This document describes the authentication-related PostgreSQL functions exposed under the `app_fcn` schema. All functions are **SECURITY DEFINER** and are intended to be executed by system-level roles (e.g. `app_system`) to bypass RLS where required.

## Overview

| Function                   | Purpose                                          | Returns             | Raises                          |
| -------------------------- | ------------------------------------------------ | ------------------- | ------------------------------- |
| `auth_exists_by_email`     | Check if a user exists for a given email         | `boolean`           | —                               |
| `auth_user_by_email`       | Fetch auth-critical user data by email           | `table`             | —                               |
| `auth_user_by_id`          | Fetch auth-critical user data by user ID         | `table`             | —                               |
| `create_refresh_token`     | Create a refresh token                           | `bigint` (token id) | —                               |
| `rotate_refresh_token`     | Revoke old refresh token and link to new         | `void`              | implicit (no-op if not matched) |
| `get_active_refresh_token` | Fetch a non-revoked refresh token by hash        | `table`             | —                               |
| `register_user`            | Atomic user registration (user + profile + role) | `void`              | `AP001`, `AP002`                |
| `revoke_refresh_token`     | Revoke a single refresh token by hash            | `void`              | —                               |
| `revoke_all_refresh_token` | Revoke all active refresh tokens for a user      | `void`              | —                               |

## Error Codes

| Code    | Meaning             |
| ------- | ------------------- |
| `AP001` | User already exists |
| `AP002` | Unknown role        |

## Notes

* All functions bypass RLS by design.
* Functions that return `void` are intended to be **idempotent**.
* Auth flows are expected to handle empty results ("not found") at the application layer.
* Refresh token state is authoritative in the database; timestamps are DB-owned.
