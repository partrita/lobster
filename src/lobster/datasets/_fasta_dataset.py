import os
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
        # Security: Remove shell=True entirely to prevent command injection
        file_path = str(self.root)
        file_size = str(os.path.getsize(file_path))

        # Build bytes_offsets pipeline
        p1 = subprocess.Popen(["cat", file_path], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["tqdm", "--bytes", "--total", file_size], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["grep", "--byte-offset", "^>", "-o"], stdin=p2.stdout, stdout=subprocess.PIPE)
        p4 = subprocess.Popen(["cut", "-d:", "-f1"], stdin=p3.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p2.stdout.close()
        p3.stdout.close()
        bytes_offsets = p4.communicate()[0]

        # Build fasta_lengths pipeline
        p1_len = subprocess.Popen(["cat", file_path], stdout=subprocess.PIPE)
        p2_len = subprocess.Popen(
            ["tqdm", "--bytes", "--total", file_size], stdin=p1_len.stdout, stdout=subprocess.PIPE
        )
        p3_len = subprocess.Popen(
            ["awk", '/^>/ {print "";next;} { printf("%s",$0);}'], stdin=p2_len.stdout, stdout=subprocess.PIPE
        )
        p4_len = subprocess.Popen(["tail", "-n+2"], stdin=p3_len.stdout, stdout=subprocess.PIPE)
        p5_len = subprocess.Popen(["awk", "{print length($1)}"], stdin=p4_len.stdout, stdout=subprocess.PIPE)
        p1_len.stdout.close()
        p2_len.stdout.close()
        p3_len.stdout.close()
        p4_len.stdout.close()
        fasta_lengths = p5_len.communicate()[0]

        return (
            numpy.fromstring(
                bytes_offsets,
                dtype=numpy.int64,
                sep=" ",
            ),
            numpy.fromstring(
                fasta_lengths,
                dtype=numpy.int64,
                sep=" ",
            ),
        )
