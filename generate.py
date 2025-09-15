from svg_wheel import generate_svg_wheel
from utils import (
    PLATFORMS,
    annotate_wheels,
    get_top_packages,
    save_to_file,
)
import csv
import subprocess
import os

TO_CHART = 360

POT_FILE = "mobile-wheels.pot"


def main(to_chart: int = TO_CHART) -> None:
    packages = get_top_packages()
    packages = annotate_wheels(packages, to_chart)
    save_to_file(packages, "results.json")
    for platform in PLATFORMS:
        generate_svg_wheel(packages, to_chart, platform)

    LANGUAGES = []
    with open("languages.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            LANGUAGES.append(row["code"])
    pot_gen = [
        "html2po",
        "--pot",
        "index.html",
        POT_FILE,
    ]
    subprocess.run(pot_gen)
    for language in LANGUAGES:
        if language == "en":
            continue
        if not os.path.exists(f"{language}.po"):
            po_gen = [
                "msginit",
                f"--input={POT_FILE}",
                f"--output-file={language}.po",
                f"--locale={language}",
                "--no-translator",
            ]
            subprocess.run(po_gen)
        else:
            po_merge = [
                "msgmerge",
                f"{language}.po",
                POT_FILE,
                f"--output-file={language}.po",
            ]
            subprocess.run(po_merge)
        html_gen = [
            "po2html",
            f"--input={language}.po",
            "--template=index.html",
            f"--output=index_{language}.html",
            "--fuzzy",
        ]
        subprocess.run(html_gen)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-n", "--number", type=int, default=TO_CHART, help="number of packages to chart"
    )
    args = parser.parse_args()

    main(args.number)
