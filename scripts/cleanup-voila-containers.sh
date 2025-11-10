#!/bin/bash
# Cleanup script to remove old voila containers before starting services
# This prevents stale network configuration issues

echo "Cleaning up old voila containers..."
docker ps -a --filter "name=nomad_oasis_north-.*--voila" --format "{{.ID}}" | xargs -r docker rm -f
echo "Cleanup complete!"
