from dataclasses import dataclass
from difflib import SequenceMatcher
import hashlib
import os
import sys


@dataclass
class Entry:
    """Class for keeping track of a filesystem entry."""
    basename: str
    fullpath: str  # path (either absolute or relative) including basename
    md5sum: str = ""
    size: int = -1
    is_dir: bool = False

    def __repr__(self) -> str:
        size_txt = f"{self.size} bytes" if self.size != -1 else ""
        md5_txt = f"{self.md5sum}" if self.md5sum else ""
        isdir_txt = "directory" if self.is_dir else ""
        metadata = [d for d in [size_txt, md5_txt, isdir_txt] if d]
        metadata_txt = " (" + ", ".join(metadata) + ")"
        return f"{self.fullpath}{metadata_txt if metadata else ''}"

    def __hash__(self):
        return id(self)


basenames = set()  # basename str
entries = {}  # k: checksum, v: Entry
duplicates = {}  # k: checksum, v: Entry.fullpath


def basename_already_recorded(basename):
    if basename in basenames:
        for k, v in entries.items():
            if v.basename == basename:
                return v
    return None


def remove(entry):
    print(f"Removing {entry} from disk...")
    if entry in entries:
        print(f"Removing {entry} from database...")
        del entries[entry]


def record_duplicates(a, b, checksum):
    if a not in entries and b not in entries:
        print("!Big problem!")
        return
    if checksum not in duplicates:
        duplicates[checksum] = {a, b}
    else:
        duplicates[checksum] |= {a, b}

    # Remove either entry from duplucates if they are part of a greater duplicate
    for checksum_a, pa in [(checksum, a), (checksum, b)]:
        to_delete = []  # Postpone deletion to prevent deleting while iterating
        for checksum_b, paths_b in duplicates.items():
            for pb in paths_b:
                if pa == pb:
                    continue
                if pa.startswith(pb):
                    deeper_path, other_path = pa, pb
                    deeper_checksum = checksum_a
                elif pb.startswith(pa):
                    deeper_path, other_path = pb, pa
                    deeper_checksum = checksum_b
                else:
                    continue
                to_delete.append((deeper_path, deeper_checksum, other_path))
        # Perform deletion of redundant entries
        for deeper_path, deeper_checksum, other_path in to_delete:
            print(deeper_path, "included in", other_path, "and will be optimized out")
            if deeper_path in duplicates[deeper_checksum]:
                duplicates[deeper_checksum].remove(deeper_path)


def same_size(a, b):
    """a and b are fully qualified paths and have same type"""
    if os.path.isdir(a):
        return same_dir_size(a, b)
    elif os.path.isfile(a):
       return same_file_size(a, b)
    else:
        raise AttributeError("Arguments should be either folder or file")


def same_checksum(a, b):
    """a and b are fully qualified paths and have same type"""
    if os.path.isdir(a):
        return same_dir_checksum(a, b)
    elif os.path.isfile(a):
        return same_file_checksum(a, b)
    else:
        raise AttributeError("Arguments should be either folder or file")


def get_dir_size(path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path, followlinks=False):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not os.path.islink(filepath):
                total_size += os.path.getsize(filepath)
    return total_size


def same_dir_size(a, b):
    # TODO: store dir size in 'entries'
    return get_dir_size(a) == get_dir_size(b)


def same_file_size(a, b):
    if a not in entries:
        entries[a] = Entry(a, os.path.basename(a))
    entries[a].size = os.path.getsize(a)
    if b not in entries:
        entries[b] = Entry(b, os.path.basename(b))        
    entries[b].size = os.path.getsize(b)
    return entries[a].size == entries[b].size


def get_dir_checksums(path):
    md5sums = set()
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                md5sums.add((fp, hashlib.md5(open(fp,'rb').read()).hexdigest()))
    return md5sums


def same_dir_checksum(a, b):
    entries_a = sorted(get_dir_checksums(a))
    entries_b = sorted(get_dir_checksums(b))
    unique_entries_a = set()
    unique_entries_b = set()
    for (pa, checksum_a), (pb, checksum_b) in zip(entries_a, entries_b):
        if os.path.basename(pa) != os.path.basename(pb):
            return False
        match = SequenceMatcher(None, pa, pb).find_longest_match()
        # TODO: prevent from matching partial words!
        common_path = pa[match.a:match.a + match.size].lstrip("/")
        unique_entries_a.add((common_path, checksum_a))
        unique_entries_b.add((common_path, checksum_b))
    if unique_entries_a == unique_entries_b:
        dir_sums = "".join([i for entry in sorted(unique_entries_a) for i in entry])
        dir_sum = hashlib.md5(dir_sums.encode()).hexdigest()
        return dir_sum
    else:
        return False


def same_file_checksum(a, b):
    if a not in entries:
        entries[a] = Entry(a, os.path.basename(a))
    elif not entries[a].md5sum:
        # print(f"Computing md5sum for {a}...")
        a_sum = hashlib.md5(open(a,'rb').read()).hexdigest()
        entries[a].md5sum = a_sum
    if b not in entries:
        entries[b] = Entry(b, os.path.basename(b))        
    elif not entries[b].md5sum:
        # print(f"Computing md5sum for {b}...")
        b_sum = hashlib.md5(open(b,'rb').read()).hexdigest()
        entries[b].md5sum = b_sum
    if entries[a].md5sum == entries[b].md5sum:
        return entries[a].md5sum
    else:
        return False


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) == 2 else "."
    for root, dirs, files in os.walk(path, followlinks=False):
        for entry_name in dirs + files:
            entry_fullpath = os.path.join(root, entry_name)
            if entry_name.startswith("."):
                continue
            if any(i in entry_fullpath for i in [".Spotlight", ".pyi"]):
                continue  # For testing purposes only
            if ".git/" in entry_fullpath:
                continue
            if os.path.islink(entry_fullpath):
                continue
            if a := basename_already_recorded(entry_name):
                if not os.path.isdir(a.fullpath) == os.path.isdir(entry_fullpath):
                    continue
                if same_size(entry_fullpath, a.fullpath):
                    if checksum := same_checksum(entry_fullpath, a.fullpath):
                        print(f"{entry_fullpath} is identical to {a.fullpath}")
                        record_duplicates(a.fullpath, entry_fullpath, checksum)
                        continue

            # print(f"Adding {entry_fullpath} to db...")
            basenames.add(entry_name)
            entries[entry_fullpath] = Entry(
                entry_name,
                entry_fullpath,
                is_dir=os.path.isdir(entry_fullpath))

    # print("--- Entries ---")
    # print("\n".join(str(e) for k, e in entries.items()))
    print("--- Duplicates ---")
    print("\n".join(f"{k}: {sorted(e)}" for k, e in sorted(duplicates.items()) if e))
