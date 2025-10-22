#!/bin/bash

echo "========================================"
echo "  Running Financial Bot Tests"
echo "========================================"
echo

python -m pytest tests/ -v --tb=short

echo
echo "========================================"
echo "  Tests Complete!"
echo "========================================"
