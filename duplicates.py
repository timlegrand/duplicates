from dataclasses import dataclass
import hashlib
import os


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
        # return hash(tuple(self))
        return id(self)


entries = {}  # elements are of type Entry
duplicates = {}  # elements are of type Entry.fullpath


def already_recorded(basename):
    for k, v in entries.items():
        if v.basename == basename:
            return v
    return None


def remove(entry):
    print(f"Removing {entry} from disk...")
    if entry in entries:
        print(f"Removing {entry} from database...")  # Should not be in DB
        del entries[entry]


def record_duplicates(a, b):
    if a not in entries:
        print("!Big problem!")
        return
    md5 = entries[a].md5sum
    if md5 not in duplicates:
        duplicates[md5] = {a, b}
    else:
        duplicates[md5] |= {a, b}


def same_size(a, b):
    if os.path.isdir(a) and os.path.isdir(b):
        return same_dir_size(a, b)
    elif os.path.isfile(a) and os.path.isfile(b):
       return same_file_size(a, b)
    else:
        raise AttributeError("Arguments should be of same type, either folder or file")


def same_checksum(a, b):
    """a and b are fully qualified paths"""
    if os.path.isdir(a) and os.path.isdir(b):
        return same_dir_checksum(a, b)
    if os.path.isfile(a) or os.path.isfile(b):
        return same_file_checksum(a, b)
    else:
        raise AttributeError("Arguments should be of same type, either folder or file")


def get_dir_size(path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    # print(">>", path, total_size)
    return total_size


def same_dir_size(a, b):
    return get_dir_size(a) == get_dir_size(b)


def same_file_size(a, b):
    if a not in entries:
        # print(f"Adding {a} to db...")
        entries[a] = Entry(a, os.path.basename(a))
    entries[a].size = os.path.getsize(a)
    if b not in entries:
        # print(f"Adding {b} to db...")
        entries[b] = Entry(b, os.path.basename(b))        
    entries[b].size = os.path.getsize(b)
    return entries[a].size == entries[b].size


def get_dir_checksum(path = '.'):
    md5sums = set()
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                md5sums.add((fp, hashlib.md5(open(fp,'rb').read()).hexdigest()))
    return md5sums


def same_dir_checksum(a, b):
    ma = get_dir_checksum(a)
    # print(a)
    # for p, m in ma:
        # print(">>", p, m)
    mb = get_dir_checksum(b)
    # print(b)
    # for p, m in mb:
        # print(">>", p, m)
    return ma == mb


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
    return entries[a].md5sum == entries[b].md5sum


if __name__ == "__main__":
    for root, dirs, files in os.walk("."):
        for entry_name in dirs + files:
            entry_fullpath = os.path.join(root, entry_name)
            # if "/.git/ref" not in entry_fullpath:
            #     continue
            # print(entry_fullpath)
            if a := already_recorded(entry_name):
                # print(f"{entry_fullpath}: filename already met at {a.fullpath}")
                if same_size(entry_fullpath, a.fullpath):
                    print(f"{entry_fullpath} has same size as {a.fullpath}")
                    if same_checksum(entry_fullpath, a.fullpath):
                        print(f"{entry_fullpath} is identical to {a.fullpath}")
                        # remove(entry_fullpath)
                        record_duplicates(entry_fullpath, a.fullpath)
                        continue
                # print(f"  > not the same file, recording...")

            # print(f"Adding {entry_fullpath} to db...")
            entries[entry_fullpath] = Entry(
                entry_name,
                entry_fullpath,
                is_dir=os.path.isdir(entry_fullpath))  # do not compute anything at this time

    # print("--- Entries ---")
    # print("\n".join(str(e) for k, e in entries.items()))
    print("--- Duplicates ---")
    print("\n".join(str(e) for k, e in duplicates.items()))
