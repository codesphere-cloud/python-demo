#!/bin/bash
# Simple script to validate data_points table in the database

if [ -z "$DB_CONNECTION_STRING" ]; then
    echo "Error: DB_CONNECTION_STRING environment variable is not set"
    exit 1
fi

echo "=== Data Points Table Validation ==="
echo ""

echo "Row count:"
psql "$DB_CONNECTION_STRING" -t -c "SELECT COUNT(*) FROM data_points;"

echo ""
echo "Latest 10 entries:"
psql "$DB_CONNECTION_STRING" -c "SELECT id, batch_id, value_a, value_b, created_at FROM data_points ORDER BY created_at DESC LIMIT 10;"

echo ""
echo "Batch summary:"
psql "$DB_CONNECTION_STRING" -c "SELECT batch_id, COUNT(*) as points, MIN(created_at) as created FROM data_points GROUP BY batch_id ORDER BY created DESC LIMIT 5;"
