#!/bin/bash

python tools/migrate_legacy/migrate.py run \
  --dry-run false \
  --overwrite false \
  --page-types get_started.index,get_started.system_requirements,teachers.quick_start,students.first_steps

