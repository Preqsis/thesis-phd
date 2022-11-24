import os
from PyPDF2 import (
    PdfReader, 
    PdfWriter, 
    PageObject
)
from argparse import ArgumentParser


ChapterList = list[dict[str, int | str]]


def split_chapters(reader: PdfReader, outdir: str, chapters: ChapterList) -> None:
    for ch in chapters:
        writer = PdfWriter()
        for n in range(ch["start"], ch["end"]+1):
            writer.add_page(reader.getPage(n))
        with open(f"{outdir}/{ch['name']}.pdf", "wb") as f:
            writer.write(f)


def get_page_number(reader: PdfReader, page: PageObject) -> int:
    i = 0
    for p in reader.pages:
        if p == page:
            return i
        i += 1
    return -1


def get_chapters(reader: PdfReader) -> ChapterList:
    chapters, i = [], 1
    for o in reader.outlines:
        if not isinstance(o, list):
            n = get_page_number(reader, o["/Page"])
            if n != -1:
                chapters.append({"start": n, "name": f"{i:02} - {o['/Title']}"})
            i += 1
    for i in range(0, len(chapters)-1, 1):
        chapters[i]["end"] = chapters[i+1]["start"]-1
    chapters.insert(0, {"start":0, "end": chapters[0]["start"]-1, "name": "00 - PREFACE"})
    chapters[-1]["end"] = reader.getNumPages()-1
    return chapters


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--infile", type=str)
    parser.add_argument("--outdir", type=str, default="./splits")
    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)

    reader = PdfReader(args.infile)
    split_chapters(reader, args.outdir, get_chapters(reader))


if __name__ == "__main__":
    main()
