# Backup script

Python program that will backup all important data on my production VPS

Script will backup:
- vaulwarden data
- knowledge base

Script consists of functions. Each of them does one of the following task
- backup vaulwarden
- backup dt-kb
- deletes old backup
- set correct permissions and owner for the backup file
