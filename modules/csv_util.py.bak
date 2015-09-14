import os
import csv


def parse_traits(traits_csv_file):
    traits_reader = csv.DictReader(traits_csv_file, delimiter=';')
    traits = [row for row in traits_reader]
    return traits


def parse_markers(markers_csv_file):
    markers_reader = csv.DictReader(markers_csv_file, delimiter=';')
    markers = [row for row in markers_reader]
    return markers
