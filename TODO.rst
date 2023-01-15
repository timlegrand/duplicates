TODO List
=========

- [ ] create package
- [x] add a CLI options parser
- [x] add a --exclude option in CLI
- [ ] create a Pytest testing suite and environment
- [ ] create a testing data generator (no versioning of testing data)
- [ ] make ``duplicates`` able to match *almost equivalents* directories::

    Folder 'A' and 'B' are 98% similar:
      Only in 'B':
        - pipo.txt
        - random/molo.txt
      Only in 'A':
        - popi.rst
      File content differs:
        - path/to/truncated.file
