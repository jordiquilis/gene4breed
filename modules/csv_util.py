import os
import csv


def parse_traits(traits_csv_file):
    traits_reader = csv.DictReader(traits_csv_file, delimiter=';')
    traits = [row for row in traits_reader]
    return traits
