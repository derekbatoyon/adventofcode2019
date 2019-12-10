# usage
#   python part1.py < map.txt

import sys

def load(file):
    orbits = {}
    for orbit in file:
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
    orbits = load(sys.stdin)

    total = 0
    for orbiter in orbits.iterkeys():
        count = orbit_count(orbits, orbiter)
        total = total + count

    print total
