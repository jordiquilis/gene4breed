# -*- coding: utf-8 -*-

if 0:
    from __init__ import *  # @UnusedWildImport


@auth.requires_membership('manager')
def index():
    return dict()

@auth.requires_membership('manager')
def contact():
    grid = SQLFORM.smartgrid(db.contact)
    return dict(grid=grid)


@auth.requires_membership('manager')
def news():
    grid = SQLFORM.smartgrid(db.news)
    return dict(grid=grid)


@auth.requires_membership('manager')
def species():
    grid = SQLFORM.smartgrid(db.species)
    return dict(grid=grid)


@auth.requires_membership('manager')
def traits():
    grid = SQLFORM.smartgrid(db.traits)
    return dict(grid=grid)
