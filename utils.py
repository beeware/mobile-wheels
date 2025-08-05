import datetime as dt
import json
import requests_cache


BASE_URL = "https://pypi.org/pypi"

DEPRECATED_PACKAGES = {
    "BeautifulSoup",
    "bs4",
    "distribute",
    "django-social-auth",
    "nose",
    "pep8",
    "pycrypto",
    "pypular",
    "sklearn",
}

PLATFORMS = ["android", "ios"]

# Keep responses for one hour
SESSION = requests_cache.CachedSession("requests-cache", expire_after=60 * 60)


def get_json_url(package_name):
    return BASE_URL + "/" + package_name + "/json"


def annotate_wheels(packages, to_chart: int) -> list[dict]:
    print("Getting wheel data...")
    num_packages = len(packages)
    total = 0
    keep = []
    for index, package in enumerate(packages):
        print(f"{total + 1}/{to_chart} {index + 1}/{num_packages} {package['name']}")
        if package["name"] in DEPRECATED_PACKAGES:
            continue

        available_platforms = set()
        url = get_json_url(package["name"])
        response = SESSION.get(url)
        if response.status_code != 200:
            print(" ! Skipping " + package["name"])
            continue

        data = response.json()

        for download in data["urls"]:
            if download["packagetype"] == "bdist_wheel":
                # The wheel filename is:
                # {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
                # https://packaging.python.org/en/latest/specifications/binary-distribution-format/#file-name-convention
                platform_tag = download["filename"].removesuffix(".whl").split("-")[-1]
                available_platforms.add(platform_tag.split("_")[0])

        if available_platforms == {"any"}:
            # Don't show packages with only pure Python wheels.
            continue
        else:
            for platform in PLATFORMS:
                package[platform] = (
                    "success"
                    if platform in available_platforms
                    else "pure-py" if "any" in available_platforms else "warning"
                )

        keep.append(package)
        total += 1
        if total == to_chart:
            break

    return keep


def get_top_packages():
    print("Getting packages...")

    with open("top-pypi-packages.json") as data_file:
        packages = json.load(data_file)["rows"]

    # We only need the names.
    for package in packages:
        name = package.pop("project")
        package.clear()
        package["name"] = name

    return packages


def save_to_file(packages, file_name):
    now = dt.datetime.now(tz=dt.timezone.utc)
    with open(file_name, "w") as f:
        f.write(
            json.dumps(
                {
                    "data": packages,
                    "last_update": now.strftime("%A, %d %B %Y, %X %Z"),
                },
                indent=1,
            )
        )
