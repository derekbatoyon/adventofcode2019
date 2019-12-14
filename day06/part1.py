# usage
#   python part1.py [file ...]
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

def orbit_count(orbits, orbiter):
    count = 0
    while orbiter != "COM":
        count = count + 1
        orbiter = orbits[orbiter]
    return count

if __name__ == "__main__":
    orbits = load(fileinput.input())

    total = 0
    for orbiter in orbits.iterkeys():
        count = orbit_count(orbits, orbiter)
        total = total + count

    print total
