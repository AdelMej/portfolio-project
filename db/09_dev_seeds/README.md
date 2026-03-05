# Development Seeds (Optional)

This directory is reserved for **optional, non-production seed data**
used during local development and business-flow testing.

## Important notes

- Scripts in this directory:
  - are **NOT required**
  - are **NOT executed in production**
  - may be **non-deterministic**
- Dev seeds may:
  - be run manually
  - be replaced frequently
  - be deleted without notice

## Philosophy

Development seeds exist to:
- speed up local testing
- simulate realistic workflows
- avoid repetitive manual setup

They must **never** be relied upon for:
- application correctness
- schema validation
- invariant enforcement

The database schema, constraints, RLS, and triggers remain the
single source of truth.

## Usage

Run manually, or via ad-hoc scripts such as:

```bash
psql app < 05_dev_seeds/some_seed.sql

