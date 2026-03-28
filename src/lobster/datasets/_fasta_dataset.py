import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

import numpy
from beignet.datasets._sized_sequence_dataset import SizedSequenceDataset
from beignet.io import ThreadSafeFile

T = TypeVar("T")


class FASTADataset(SizedSequenceDataset):
    def __init__(
        self,
        root: str | Path,
        *,
        transform: Callable | None = None,
        use_text_descriptions: bool = True,
    ) -> None:
        if isinstance(root, str):
            root = Path(root)

        self.root = root

        self.root = self.root.resolve()

        if not self.root.exists():
            raise FileNotFoundError

        self._use_text_descriptions = use_text_descriptions

        self.data = ThreadSafeFile(self.root, open)

        offsets = Path(f"{self.root}.offsets.npy")

        if offsets.exists():
            self.offsets, sizes = numpy.load(f"{offsets}")
        else:
            self.offsets, sizes = self._build_index()

            numpy.save(f"{offsets}", numpy.stack([self.offsets, sizes]))

        self.transform = transform

        super().__init__(self.root, sizes)

    def __getitem__(self, index: int) -> tuple[str, str]:
        x = self.get(index)
        if self.transform:
            x = self.transform(x)

        return x

    def __len__(self) -> int:
        return self.offsets.size

    def get(self, index: int) -> tuple[str, str]:
        self.data.seek(self.offsets[index])

        if index == len(self) - 1:
            data = self.data.read()
        else:
            data = self.data.read(self.offsets[index + 1] - self.offsets[index])

        description, *sequence = data.split("\n")

        sequence = "".join(sequence)

        if self._use_text_descriptions:
            return sequence, description

        return sequence

    def _build_index(self) -> tuple[numpy.ndarray, numpy.ndarray]:
        p1 = subprocess.Popen(["cat", str(self.root)], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "--byte-offset", "^>", "-o"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["cut", "-d:", "-f1"], stdin=p2.stdout, stdout=subprocess.PIPE)
        out1, _ = p3.communicate()

        p4 = subprocess.Popen(["cat", str(self.root)], stdout=subprocess.PIPE)
        p5 = subprocess.Popen(["awk", '/^>/ {print "";next;} { printf("%s",$0);}'], stdin=p4.stdout, stdout=subprocess.PIPE)
        p6 = subprocess.Popen(["tail", "-n+2"], stdin=p5.stdout, stdout=subprocess.PIPE)
        p7 = subprocess.Popen(["awk", "{print length($1)}"], stdin=p6.stdout, stdout=subprocess.PIPE)
        out2, _ = p7.communicate()

        return (
            numpy.fromstring(out1, dtype=numpy.int64, sep=" "),
            numpy.fromstring(out2, dtype=numpy.int64, sep=" "),
        )
