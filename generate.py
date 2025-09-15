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
    if os.path.exists(POT_FILE):
        with open(POT_FILE, "r") as pot:
            old_pot_contents = pot.read()
    else:
        old_pot_contents = None
    pot_gen = [
        "html2po",
        "--pot",
        "index.html",
        POT_FILE,
    ]
    subprocess.run(pot_gen)
    if old_pot_contents is not None:
        with open(POT_FILE, "r") as pot:
            pot_contents = pot.read()
        # The below checks for only one differing line.  The creation
        # date of the POT is always changed, and that change shall
        # be reverted if it's the only change, since that results
        # in a no-op commit.
        if (
            sum(
                a != b
                for a, b in zip(
                    pot_contents.splitlines(), old_pot_contents.splitlines()
                )
            )
            + abs(len(pot_contents.splitlines()) - len(old_pot_contents.splitlines()))
            == 1
        ):
            with open(POT_FILE, "w") as pot:
                pot.write(old_pot_contents)
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
