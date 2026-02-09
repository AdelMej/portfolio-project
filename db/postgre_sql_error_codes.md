# PostgreSQL Domain Errors

This document lists database functions that intentionally raise domain errors and the SQLSTATE they use.

---

## Domain SQLSTATE

| SQLSTATE | Meaning |
|--------|---------|
| P0001 | Domain-level rejection raised intentionally by database logic |

---

## Functions

| Function | Raises | Error meaning |
|---------|--------|---------------|
| `app_fcn.user_exists_by_email` | — | Pure lookup, never raises |
| `app_fcn.auth_user_by_email` | — | Authentication data lookup, never raises |
| `app_fcn.issue_refresh_token` | — | Issues a new refresh token, never raises |
| `app_fcn.rotate_refresh_token` | P0001 | Refresh token not found, revoked, or invalid |

---

## Notes

- SQLSTATE is the contract
- Messages are informational only
- All new domain errors must use `P0001`

