# Python-projects

This is my python learning journey. Instead of learning by following the tutorial let's try to get hands on the real life projects:

So far this came to my mind

**Simple**
- Disk usage reporter - Write a script that scans directories and reports disk usage, similar to du but with your own formatting.
  - modules: os
- Log parser - Parse /var/log/syslog or /var/log/auth.log and extract useful info (failed logins, errors, etc.)
  - modules: re

**Intermediate**
- backup script - Backup specified directories, compress them with a timestamp, and optionally clean up old backups. (shutil, tarfile, datetime, argparse)
  - modules: shutil, tarfile, datetime, argparse
- Service Health Monitor - Check if a list of services (nginx, ssh, etc.) are running and send an alert (email or log) if one is down.
  - modules: subprocess, smtplib, cron

**Advanced**
- REST API for System Metrics - Build a small web API using Flask that exposes system metrics (CPU, RAM, disk) as JSON endpoints.
  - modules: Flask, REST concepts, JSON, psutil
- scraping system metric for prometheus
