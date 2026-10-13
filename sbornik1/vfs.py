import zipfile
import os


class VFS:
    """Виртуальная файловая система на основе ZIP-архива.
    Все операции производятся в памяти."""

    def __init__(self, archive_path=None):
        self.files = {}
        self.dirs = {'/'}
        self.name = "default_vfs"

        if archive_path is not None:
            self._load_zip(archive_path)
        else:
            self._create_default()

    def _load_zip(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"VFS не найден: {path}")
        if not zipfile.is_zipfile(path):
            raise ValueError(f"Неверный формат VFS: {path}")

        with zipfile.ZipFile(path, 'r') as zf:
            for info in zf.infolist():
                name = info.filename
                if name.endswith('/'):
                    clean = '/' + name.rstrip('/')
                    self.dirs.add(clean)
                    self._add_parents(name.rstrip('/'))
                else:
                    data = zf.read(name)
                    self.files['/' + name] = data
                    self._add_parents(name)

        self.name = os.path.basename(path).rsplit('.', 1)[0]

    def _add_parents(self, path):
        parts = path.split('/')
        for i in range(1, len(parts)):
            parent = '/' + '/'.join(parts[:i])
            self.dirs.add(parent)

    def _create_default(self):
        self.files['/readme.txt'] = b"Default VFS (no archive provided)\n"
        self.dirs.add('/')
        self.name = "default_vfs"

    def exists(self, path):
        return path in self.files or path in self.dirs

    def is_dir(self, path):
        return path in self.dirs

    def list_dir(self, path):
        if not path.endswith('/'):
            path = path + '/'
        prefix = path if path != '//' else '/'
        entries = set()
        for f in self.files:
            if f.startswith(prefix):
                rest = f[len(prefix):]
                if rest:
                    entries.add(rest.split('/')[0])
        for d in self.dirs:
            if d.startswith(prefix) and d != prefix.rstrip('/'):
                rest = d[len(prefix):]
                if rest:
                    entries.add(rest.split('/')[0])
        return sorted(entries)

    def read_file(self, path):
        if path not in self.files:
            raise FileNotFoundError(f"Файл не найден: {path}")
        return self.files[path]

    def normalize_path(self, current_dir, path):
        if path.startswith('/'):
            result = path
        elif current_dir == '/':
            result = '/' + path
        else:
            result = current_dir + '/' + path

        parts = []
        for p in result.split('/'):
            if p == '' or p == '.':
                continue
            if p == '..':
                if parts:
                    parts.pop()
            else:
                parts.append(p)
        return '/' + '/'.join(parts) if parts else '/'
