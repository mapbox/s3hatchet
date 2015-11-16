# s3hatchet
Split + summarize big s3 ls logs

## Usage

```
cat {log} | s3hatchet load {dump} -et '(\d+)-(\d+)-(\d+)-([a-zA-Z0-9_]+)-\d+-[a-zA-Z0-9_]+.tif' '["z=int", "x=int", "y=int", "source=S256"]' -s source size
```
