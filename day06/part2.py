# usage
#   python part2.py [file ...]
#
# The file operands are processed in command-line order.  If file is a single
# dash (`-') or absent, reads from the standard input.

import fileinput

def load(fh):
    orbits = {}
    for orbit in fh:
        (orbitee, orbiter) = orbit.split(")", 1)
        orbiter = orbiter.strip()
        orbitee = orbitee.strip()
        orbits[orbiter] = orbitee
    return orbits

def orbit_count(orbits, orbiter, common = "COM"):
    count = 0
    while orbiter != common:
        count = count + 1
        orbiter = orbits[orbiter]
    return count

if __name__ == "__main__":
    orbits = load(fileinput.input())

    point1 = orbits["YOU"]
    point2 = orbits["SAN"]

    minimum_transfers = orbit_count(orbits, point1) + orbit_count(orbits, point2)
    minimum_common = "COM"

    for common in orbits.iterkeys():
        if common in ("YOU", "SAN", point1, point2):
            continue

        try:
            transfers = orbit_count(orbits, point1, common) + orbit_count(orbits, point2, common)
            if transfers < minimum_transfers:
                minimum_transfers = transfers 
                minimum_common = common

        except KeyError:
            pass

    print minimum_transfers
