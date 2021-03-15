import typing
from pathlib import Path
import re
import PyPDF2
from PyPDF2.utils import PdfReadError
from PIL import Image
import pytesseract


"""
Форматы файлов PDF Jpeg
Шаблоны данных: Разные N
Извлекаемых данных на 1 файл: N
Искомый шаблон: Заводской {} номер {} {извлекаемые данные}
все извлекаемые данные eng
"""

"""
DB:
- Пути к файлам
- Извлеченные данные
- Ошибки (если ничего не нашли, битые файлы)
"""


def pdf_image_extract(pdf_path: Path, images_path: Path) -> typing.List[Path]:
    result = []
    with pdf_path.open("rb") as file:
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
        except PdfReadError as exc:
            print(exc)  # tODo записать ошибку в DB
            return result

        for page_num, page in enumerate(pdf_file.pages, 1):
            image_file_name = f"{pdf_path.name}_{page_num}"
            img_data = page["/Resources"]["/XObject"]["/Im0"]._data
            image_path = images_path.joinpath(image_file_name)
            image_path.write_bytes(img_data)
            result.append(image_path)

    return result


def get_serial_number(image_path: Path) -> typing.List[str]:
    result = []
    image = Image.open(image_path)
    text_rus = pytesseract.image_to_string(image, "rus")
    pattern = re.compile(r"(заводской.*[номер|№])")
    matchs = len(re.findall(pattern, text_rus))
    if matchs:
        text_eng = pytesseract.image_to_string(image, "eng").split("\n")
        for idx, line in enumerate(text_rus.split("\n")):
            if re.match(pattern, line):
                result.append(text_eng[idx].split()[-1])
            if len(result) == matchs:
                break
    # TODO: если номер не найден, записать ошибку
    return result


if __name__ == "__main__":
    IMAGES_PATH = Path(__file__).parent.joinpath("images")
    if not IMAGES_PATH.exists():
        IMAGES_PATH.mkdir()

    pdf_file_temp = Path(__file__).parent.joinpath("8416_4.pdf")
    images = pdf_image_extract(pdf_file_temp, IMAGES_PATH)

    numbers = list(map(get_serial_number, images))
    print(1)
