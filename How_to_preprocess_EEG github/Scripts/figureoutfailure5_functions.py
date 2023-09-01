#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 13:45:33 2022

@author: Kirk
"""


import numpy as np
import mne
from mne.surface import _jit_cross



def surface_check(tri_rrs,fros):
    if len(fros) > 10000:
        spacer = 3000
    elif len(fros) > 4000:
        spacer = 5000
    elif len(fros) > 500:
        spacer = 11000
    else:
        spacer = 25000
    
    tot_angle = np.zeros((len(fros)))
    for ti in range(len(tri_rrs)):
        if ti % spacer == 0 and ti > 0:
            print("Checking surface element " + str(ti) + ' of ' + str(len(tri_rrs)))
        tri_rr = tri_rrs[ti]
        v1 = fros - tri_rr[0]
        v2 = fros - tri_rr[1]
        v3 = fros - tri_rr[2]
        v4 = np.empty((v1.shape[0], 3))
        _jit_cross(v4, v1, v2)
        triple = np.sum(v4 * v3, axis=1)
        l1 = np.sqrt(np.sum(v1 * v1, axis=1))
        l2 = np.sqrt(np.sum(v2 * v2, axis=1))
        l3 = np.sqrt(np.sum(v3 * v3, axis=1))
        s = (l1 * l2 * l3 +
             np.sum(v1 * v2, axis=1) * l3 +
             np.sum(v1 * v3, axis=1) * l2 +
             np.sum(v2 * v3, axis=1) * l1)
        tot_angle -= np.arctan2(triple, s)    

    badispoints = np.abs(tot_angle / (2 * np.pi) - 1.0) > 1e-5
    badindex = [i for i, x in enumerate(badispoints) if x]
    numbadispoints = sum(badispoints)
    
    return badindex, numbadispoints


def adj_surface2(badpoint,inneradj,midx,midy,midz):
    
    v = badpoint - [midx,midy,midz]
    vmag = np.sqrt(v[0]**2+v[1]**2+v[2]**2)
    u = v/vmag
    badpoint2 = badpoint - inneradj*u
    return badpoint2


def adj_surface_alt(badpoint,inneradj,midx,midy,midz):
    
    v = badpoint - [midx,midy,midz]
    vmag = np.sqrt(v[0]**2+v[1]**2+v[2]**2)
    u = v/vmag
    badpoint2 = badpoint + inneradj*u
    return badpoint2


def closest_points(fros,outer_fros):
    closestpoints = []
    for nn in range(len(fros)):
        badpoint = fros[nn] 
        deltas = outer_fros - badpoint
        dist_2 = np.einsum('ij,ij->i', deltas, deltas)
        closestpoint = outer_fros[np.argmin(dist_2)]
        closestpoints.append(closestpoint)
    return closestpoints


def new_combined_surface(output,outersurf,innersurf,inneradj,midx,midy,midz):
    
    badindexlist = []
    
    tri_rrs = outersurf['rr'][outersurf['tris']]
    outer_fros = outersurf['rr'].copy()
    
    fros = innersurf['rr'].copy()
    adjfros = innersurf['rr'].copy()
    
    print('Checking that surface 1 is inside surface 2...')
    badindex, numbadispoints = surface_check(tri_rrs,fros)
    
    badindexlist.append(badindex)
    
    print("There are " + str(numbadispoints) + " inner surface points outside the outer surface")
    
    
    if numbadispoints > 0:
        
        badpoints = adjfros[badindex]
        closestpoints = closest_points(badpoints,outer_fros)
    
        for binum in range(len(badindex)):
            bi = badindex[binum]
            closestpoint = closestpoints[binum]
            adjfros[bi] = adj_surface2(adjfros[bi],inneradj,closestpoint[0],closestpoint[1],closestpoint[2])
            adjfros[bi] = adj_surface2(adjfros[bi],inneradj,midx,midy,midz)
    
        subfros = adjfros[badindex]
        
        subbadindex, numbadispoints2 = surface_check(tri_rrs,subfros)    
        badindex2 = [badindex[x] for x in subbadindex]
    
        counter = 1    
        print("After adjusting/rechecking round " + str(counter) + ", there are " + str(numbadispoints2) + " inner surface points outside the outer surface")
    
        while numbadispoints2 > 0:
    
            badpoints = adjfros[badindex2]
            closestpoints = closest_points(badpoints,outer_fros)
            
            if counter < 90:
                for binum in range(len(badindex2)):
                    bi = badindex2[binum]
                    closestpoint = closestpoints[binum]
                    adjfros[bi] = adj_surface2(adjfros[bi],inneradj,closestpoint[0],closestpoint[1],closestpoint[2])
                    adjfros[bi] = adj_surface2(adjfros[bi],inneradj,midx,midy,midz)
            elif counter < 190:
                for binum in range(len(badindex2)):
                    bi = badindex2[binum]
                    closestpoint = closestpoints[binum]
                    adjfros[bi] = adj_surface2(adjfros[bi],inneradj*0.25,closestpoint[0],closestpoint[1],closestpoint[2])
                    adjfros[bi] = adj_surface2(adjfros[bi],inneradj,midx,midy,midz)    
            else:
                for binum in range(len(badindex2)):
                    bi = badindex2[binum]
                    closestpoint = closestpoints[binum]
                    adjfros[bi] = adj_surface2(adjfros[bi],inneradj,midx,midy,midz)                    
    
            subfros = adjfros[badindex2]
                    
            subbadindex, numbadispoints2 = surface_check(tri_rrs,subfros)    
            badindex2 = [badindex2[x] for x in subbadindex]
            
            counter = counter + 1
    
            print("After adjusting/rechecking round " + str(counter) + ", there are " + str(numbadispoints2) + " inner surface points outside the outer surface")
    
    
    mne.write_surface(output, adjfros, innersurf['tris'], overwrite=True)
    
    
    
def new_within_surface(output,outersurf,innersurf,closersurf,inneradj,midx,midy,midz):
    
    badindexlist = []
    
    tri_rrs = outersurf['rr'][outersurf['tris']]
    
    fros = innersurf['rr'].copy()
    adjfros = innersurf['rr'].copy()
    
    closer_fros = closersurf['rr'].copy()
    
    
    print('Checking that surface 1 is inside surface 2...')
    badindex, numbadispoints = surface_check(tri_rrs,fros)
    
    badindexlist.append(badindex)
    
    print("There are " + str(numbadispoints) + " inner surface points outside the outer surface")
    
    
    if numbadispoints > 0:
        
        badpoints = adjfros[badindex]
        closestpoints = closest_points(badpoints,closer_fros)
    
        for binum in range(len(badindex)):
            bi = badindex[binum]
            closestpoint = closestpoints[binum]
            adjfros[bi] = adj_surface2(adjfros[bi],inneradj,closestpoint[0],closestpoint[1],closestpoint[2])
            adjfros[bi] = adj_surface2(adjfros[bi],inneradj,midx,midy,midz)
    
        subfros = adjfros[badindex]
        
        subbadindex, numbadispoints2 = surface_check(tri_rrs,subfros)    
        badindex2 = [badindex[x] for x in subbadindex]
    
        counter = 1    
        print("After adjusting/rechecking round " + str(counter) + ", there are " + str(numbadispoints2) + " inner surface points outside the outer surface")
    
        while numbadispoints2 > 0:
    
            badpoints = adjfros[badindex2]
            closestpoints = closest_points(badpoints,closer_fros)
        
            for binum in range(len(badindex2)):
                bi = badindex2[binum]
                closestpoint = closestpoints[binum]
                adjfros[bi] = adj_surface2(adjfros[bi],inneradj,closestpoint[0],closestpoint[1],closestpoint[2])
                adjfros[bi] = adj_surface2(adjfros[bi],inneradj,midx,midy,midz)
    
            subfros = adjfros[badindex2]
                    
            subbadindex, numbadispoints2 = surface_check(tri_rrs,subfros)    
            badindex2 = [badindex2[x] for x in subbadindex]
            
            counter = counter + 1
    
            print("After adjusting/rechecking round " + str(counter) + ", there are " + str(numbadispoints2) + " inner surface points outside the outer surface")
    
    
    mne.write_surface(output, adjfros, innersurf['tris'], overwrite=True)

















    