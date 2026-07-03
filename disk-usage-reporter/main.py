import os
import sys

# get first argument
target = sys.argv[1]

# Check if target exists
if not os.path.exists(target):
    print(f'Path "{target}" does not exists!')
    sys.exit(1)

total = 0
for root, dirs, files in os.walk(target, followlinks=False):
    for name in files:
        full_path = os.path.join(root, name)
        total += os.path.getsize(full_path)

print(f"Path: {target}")
if (1024**3) > total:
    print(f"Size: {total / (1024**2):.2f} MB")
else:
    print(f"Size: {total / (1024**3):.2f} GB")
