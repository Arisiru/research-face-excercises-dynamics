import math
import numpy as np

def rescale(value, minimum, maximum):
    return (value - minimum) / (maximum - minimum)

def normalize(s):
    s_minimum = min(s)
    s_maximum = max(s)
    
    if (s_maximum - s_minimum) == 0:
        return s
    
    return [rescale(x, s_minimum, s_maximum) for x in s]

def unit_vector(vector):
    if np.linalg.norm(vector) == 0:
        return np.nan
    
    return vector / np.linalg.norm(vector)

def angle_between_two_points(p1, p2):
    p1_u = unit_vector(p1)
    p2_u = unit_vector(p2)
    result = np.arccos(np.clip(np.dot(p1_u, p2_u), -1.0, 1.0))
    return 0.0 if np.isnan(result) else result

def direction_angles(xs, ys, zs):
    angles = [0]
    for i in range(1, len(xs)):
        angles.append(angle_between_two_points([xs[i-1], ys[i-1], zs[i-1]], [xs[i], ys[i], zs[i]]))
        
    return angles

def normalize_by_start(s):
    return [x - s[0] for x in s]

def distance(xs, ys, zs):
    distance = [0]
    for i in range(1, len(xs)):
        distance.append(math.dist([xs[i-1], ys[i-1], zs[i-1]], [xs[i], ys[i], zs[i]]))
    
    return distance

def rebase(s, s_name, poi_name, pois, bases):
    base_name = bases[poi_name]
    base_s = pois[base_name][s_name]
    return[x - bx for x, bx in zip(s, base_s)]

def symetry_diff(orig_s, ax_name, orig_poi_name, pois, symetries):
    #print(f'orig_poi_name {orig_poi_name}')
    #print(symetries)
    #print(f'symetry_poi_name {symetries[orig_poi_name]}')

    symetry_poi_name = symetries[orig_poi_name]
    if symetry_poi_name == "None":
        return [0]*len(orig_s)
    
    symetry_s = pois[symetry_poi_name][ax_name]
    return[abs(x - bx) for x, bx in zip(orig_s, symetry_s)]