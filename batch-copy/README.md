# Mass copy

A small CLI script that makes multiple named copies of a single template file.

Given a source file and a list of names (one per line), it creates one copy of the source file per name, using that name plus the source file's original extension.

## Usage
```
python main.py <source_file> <name_list_file>
```
- `source_file` — the file to duplicate.
- `name_list_file` — a text file with one name per line.

## Example
Source file `text.txt`, and a name list `macs.txt`:
```text
aabbcc
mmnnoo
```

Run:
```
python main.py text.txt macs.txt
```
Result: `aabbcc.txt` and `mmnnoo.txt` are created, each an identical copy of `text.txt`.
