# schema.py
# Banking Management System - Database Schema Definition
#
# This file provides a structural outline for implementing a banking
# management system within FlaskBB. It does NOT include executable code;
# it is reserved for schema design and documentation purposes only.

# ============================================================================
# ACCOUNT ENTITY
# ============================================================================
#
# Account is the central entity representing a user's financial account.
#
# Fields:
#   id            (INTEGER, PRIMARY KEY): Unique identifier for each account.
#   user_id       (INTEGER, FOREIGN KEY -> users.id): Associates the account
#                with a specific FlaskBB user.
#   balance       (DECIMAL(19,4)): Current monetary balance of the account.
#                Uses DECIMAL for exact arithmetic to prevent floating-point
#                rounding errors.
#   currency      (VARCHAR(3) / ENUM): The currency code of the account.
#                Examples: 'USD', 'EUR', 'GBP', 'JPY'.
#   created_at    (TIMESTAMP): Date and time the account was created.
#   updated_at    (TIMESTAMP): Date and time the account was last modified.
#                Should auto-update on any balance change.
#
# Constraints:
