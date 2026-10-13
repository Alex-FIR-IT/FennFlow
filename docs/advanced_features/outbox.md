# Outbox

FennFlow writes an event to an **outbox table** whenever a file is inserted, updated or deleted. The table lives in the same database as the backend metadata and is meant for event-driven architectures: a separate consumer reads the events and publishes them to a broker.

!!! note "The outbox is not part of the Saga flow"

    FennFlow never reads the outbox. SSOT and Saga compensation are driven entirely by backend metadata, as described in [Core Concepts — Overview](../overview.md). The outbox is a one-way integration point: FennFlow writes, your infrastructure reads.

The outbox works out of the box and is not configurable: there is nothing to enable and no custom table to supply.

## When events are written

An event is written only when an operation is committed, in the same database session that persists the operation record.

| Situation                                    | Event          |
| -------------------------------------------- | -------------- |
| `create` / `put` committed                   | Yes            |
| `delete` / `delete_prefix` committed         | Yes (one per file) |
| Operation is still pending in the session    | No             |
| Session rolled back (compensation executed)  | No             |
| Read operations (`get`, `list`, presigned URLs) | No          |

Consequently, an event always describes a change that was committed in the backend, and rolled-back work never leaks to consumers.

### Reconciler

The [reconciler](../core_concepts/reconciler.md) also writes events: every file it registers in the backend produces an event, with the operation recorded as already uploaded. With the default `FILL_IF_EMPTY` strategy this happens once, on first start against an existing bucket, so expect a burst of events proportional to the number of files in your storage. Consumers that must distinguish "a user uploaded this" from "FennFlow discovered this" should look at `payload["status"]`.

## Table schema

| Column           | Type                   | Notes                                                                 |
| ---------------- | ---------------------- | --------------------------------------------------------------------- |
| `id`             | `UUID`                 | Primary key, generated per outbox row.                                |
| `event_id`       | `UUID`, unique         | Equals the operation's `operation_id`. Use it to deduplicate.         |
| `aggregate_type` | `VARCHAR(50)`          | Type of entity the event is about.                                    |
| `aggregate_id`   | `VARCHAR(255)`         | Deterministic hash of `scope`, `namespace` and `storage_path`.        |
| `event_type`     | `VARCHAR(50)`          | The operation type that produced the event.                           |
| `payload`        | `JSON`                 | Snapshot of the operation record, see [Payload](#payload).            |
| `status`         | `VARCHAR(63)`, indexed | Delivery status: `pending`, `failed` or `sent`. Defaults to `pending`. |
| `created_at`     | `TIMESTAMPTZ`          | Set on insert (UTC).                                                  |
| `updated_at`     | `TIMESTAMPTZ`          | Set on insert, refreshed on every update (UTC).                       |

`status` is stored as a plain string rather than a native database enum, so adding a status never requires an enum migration.

### Aggregate

An aggregate is one file in one namespace of one scope. `aggregate_id` is a hash of those three values, so it has a fixed length regardless of how long the storage path is. Use it as the partition key when publishing to a broker to keep events for the same file ordered. The readable parts are in the [payload](#payload).

## Payload

The payload is a JSON snapshot of the operation record at the time of writing:

```json
{
  "operation_id": "3f2b8c1e5d7a4e0f9a6b1c2d3e4f5a6b",
  "operation_type": "create",
  "session_id": "9a8b7c6d5e4f30211a2b3c4d5e6f7a8b",
  "scope": "default",
  "namespace": "avatars",
  "storage_path": "user-123/avatar.jpg",
  "status": "uploaded",
  "created_at": "2026-09-30T12:00:00+00:00",
  "expired_at": "2026-09-30T13:00:00+00:00",
  "error": null
}
```
The payload.status can be one of: `pending`, 'uploaded', 'failed', 'compensation_failed', 'deleted'

UUIDs inside the payload are serialized as hex without dashes, while the `event_id` column is a native UUID.

## Delivery status

`status` describes the state of *delivery to your broker*, not of the file operation (that is `payload["status"]`). It is unrelated to the `PENDING` state of operations inside a session.

| Value     | Meaning                                       |
| --------- | --------------------------------------------- |
| `pending` | Written by FennFlow, not yet delivered.       |
| `failed`  | A delivery attempt failed.                    |
| `sent`    | Delivered.                                    |

FennFlow only ever writes `pending`. Moving a row to `sent` or `failed` is the job of whatever consumes the table.

## Event types

Only the following statuses can be put in event_type column of the outbox table: `create`, `put`, `delete`


## Limitations

- FennFlow does not ship a consumer. Retries, dead-lettering and per-row error tracking are not available yet.
- Rows are never deleted by FennFlow. Purge `sent` rows with a scheduled job.
