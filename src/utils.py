import hashlib
from ast import literal_eval
from datetime import datetime
from pathlib import Path
from typing import Union

import dotenv
import numpy as np

FilePath = Union[Path, str]


def get_hash(file_path: FilePath) -> str:
    """Hash a file using SHA-256."""
    h = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def store_hash(file_path: FilePath) -> None:
    """Hash a file and and store it's SHA-256 hash in the same folder."""
    hash_path = Path(file_path).with_suffix(".sha256")
    digest = get_hash(file_path)
    with open(hash_path, "w") as file:
        file.write(digest)
    return


def check_hash(file_path: FilePath, hash_path: FilePath = None) -> bool:
    """Check that a file and its SHA-256 hash matches.

    `hash_path` is a text file containing the SHA-256 hash. If `None`, it looks for a
    file with in the same folder and name as `file_path`, but with extension `.sha256`
    instead."""
    if not hash_path:
        hash_path = Path(file_path).with_suffix(".sha256")
    with open(hash_path, "r") as file:
        stored_digest = file.readline().strip()
    file_digest = get_hash(file_path)
    return file_digest == stored_digest


def chunks(lst, n):
    """Yield successive n-sized chunks from lst.

    https://stackoverflow.com/a/312464
    """
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def get_api_key():
    env_path = dotenv.find_dotenv(".env")
    if env_path == "":
        raise FileNotFoundError(
            "Could not find .env file in root folder. "
            + "Check .env.example for instructions."
        )
    env = dotenv.dotenv_values(env_path)
    try:
        api_key = env["API_KEY"]
    except KeyError:
        raise KeyError("API_KEY not found in .env file")
    inp = input(
        "You are about to use the Google Maps API key. "
        + "THIS WILL INCUR CHARGES ON YOUR GOOGLE ACCOUNT. "
        + "Enter $$$ to continue, or anything else to quit.\n"
        + "Input: "
    )
    if inp == "$$$":
        return api_key
    else:
        raise ValueError("You must enter $$$ to get the Google Maps API key")


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distrance between two points on Earth, in km.

    lon1, lat1, lon2, lat2 are longitude/latitude in decimal degrees:
        e.g. 100.194903, -6.439888
    Longitudes are between -180 and +180, latitudes are between -90 an +90.
    """
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (np.sin(dlat / 2.0) ** 2) + (
        np.cos(lat1) * np.cos(lat2) * (np.sin(dlon / 2.0) ** 2)
    )

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


def now() -> str:
    """Return the current time as a YYYYMMDD-hhmmss string."""
    t = datetime.now()
    return t.strftime("%Y%m%d-%H%M%S")


def postcode_str(pc: Union[int, str]) -> str:
    """Stringify a postcode, padding with zeros on the left."""
    if int(pc) < 0 or int(pc) > 99999:
        raise ValueError("Postcode must be between 0 and 99999")
    return str(pc).zfill(5)


def parse_coord_tuple(input: str) -> tuple[float, float]:
    result = literal_eval(input)
    if not isinstance(result, tuple):
        raise ValueError("input must be parsable into a tuple")
    for num in result:
        if not isinstance(num, float):
            raise ValueError("inner values of input tuple must be parsable into floats")
    if len(result) != 2:
        raise ValueError("input must have exactly two parsable floats")
    return result  # type: ignore
