import json
import os

import tensorflow as tf

import numpy as np

import utils.transformations as transformations

CONFIG = {}


def setup(root_path, seq_max_len, num_exercises, num_flag_bs):
    CONFIG['ROOT_PATH'] = root_path

    setting_path = os.path.join(CONFIG['ROOT_PATH'], 'src', 'settings')
    CONFIG['ALL_REGIONS'] = json.load(open(os.path.join(setting_path, 'all_regions.json')))
    CONFIG['REGIONS'] = json.load(open(os.path.join(setting_path, 'pois_region.json')))
    CONFIG['BASES'] = json.load(open(os.path.join(setting_path, 'pois_base.json')))
    
    CONFIG['SEQ_MAX_LEN'] = seq_max_len

    CONFIG['NUM_EXERCISES'] = num_exercises
    CONFIG['NUM_FLAG_BS'] = num_flag_bs

    return CONFIG

def feature_engineering_sequence(poi, isrebase=False, poi_name='', pois={}, settings={}):
    new_sequences = []    
    
    if isrebase:
        xs = transformations.rebase(poi['xs'], 'xs', poi_name, pois, CONFIG['BASES'])
        ys = transformations.rebase(poi['ys'], 'ys', poi_name, pois, CONFIG['BASES'])
        zs = transformations.rebase(poi['zs'], 'zs', poi_name, pois, CONFIG['BASES'])
    else:
        xs = poi['xs']
        ys = poi['ys']
        zs = poi['zs']
        
    #original
    if settings['coordinates'] or isrebase:
        new_sequences.append(xs)
        new_sequences.append(ys)
        new_sequences.append(zs)

    if not isrebase or settings['transformation_to_rebase']:
        #normalize by start
        if settings['normalize_by_start']:
            new_sequences.append(transformations.normalize_by_start(xs)) 
            new_sequences.append(transformations.normalize_by_start(ys))
            new_sequences.append(transformations.normalize_by_start(zs))
        #normalize    
        if settings['normalize']:
            new_sequences.append(transformations.normalize(xs)) 
            new_sequences.append(transformations.normalize(ys))
            new_sequences.append(transformations.normalize(zs))
        #direction
        if settings['direction']:
            new_sequences.append(transformations.direction_angles(xs, ys, zs))
        #distance
        if settings['distance']:
            new_sequences.append(transformations.distance(xs, ys, zs))
    
    return new_sequences

def build_region(pois, region, settings):
    exercise_sequence_region = []
    
    for poi_name in sorted(CONFIG['REGIONS'].keys()):
        if CONFIG['REGIONS'][poi_name] == region or region == 'global':
            sequences = pois[poi_name]
            exercise_sequence_region.extend(feature_engineering_sequence(sequences, isrebase=False, settings=settings))
            exercise_sequence_region.extend(feature_engineering_sequence(sequences, isrebase=True, poi_name=poi_name, pois=pois, settings=settings))
    

    exercise_sequence_region = tf.keras.preprocessing.sequence.pad_sequences(
        exercise_sequence_region,
        padding="pre",
        maxlen=CONFIG['SEQ_MAX_LEN'],
        dtype='float32')
    
    return exercise_sequence_region


def build_meta(exercise, settings):
    meta  = []
    exercise_one_hot = [0] * CONFIG['NUM_EXERCISES']

    exercise_id = int(exercise['meta']['id']) - 1
    exercise_one_hot[exercise_id] = 1
    meta = exercise_one_hot
    
    #surgery_one_hot = [0] * CONFIG['NUM_FLAG_BS']
    #surgery_one_hot[exercise['meta']['flag_before_surgery']] = 1
    #meta = meta + surgery_one_hot
    
    #length of exercise; 
    if settings['extended_meta']:
        exercise_length = len(exercise['pois']['LefteyeMidbottom']['xs'])
            #list(CONFIG['REGIONS'].keys())[0]
            #print(f'Exercise lenth {exercise_length}')
        meta.append(exercise_length)

    #overall distance pois traveled, cumulative distance and normalized
    if settings['extended_meta']:
        poi_distnaces = []
        poi_distnaces_normalized = []
        for poi_name in sorted(CONFIG['REGIONS'].keys()):
            sequences = exercise['pois'][poi_name]
            distances = transformations.distance(sequences['xs'],sequences['ys'], sequences['zs'])
            distance = sum(distances)
            poi_distnaces.append(distance)
            poi_distnaces_normalized.append(distance/exercise_length)
                #print(f'There are {len(distances)} distances their sum is {distance}, normalized {distance/exercise_length}')

        meta = meta + poi_distnaces + poi_distnaces_normalized

    return meta


def exercise_to_input(file_path, settings):
    exercise = json.load(open(file_path, 'r'))

    # build regions 
    exercise_sequence_global_region = build_region(exercise['pois'], 'global', settings)
    exercise_sequence_frontal_region = build_region(exercise['pois'], 'frontal', settings)
    exercise_sequence_oral_region = build_region(exercise['pois'], 'oral', settings)
    exercise_sequence_orbital_region = build_region(exercise['pois'], 'orbital', settings)
        
    # build meta
    exercise_meta = build_meta(exercise, settings)

    evaluation = 0
    if exercise['meta']['evaluation'] != 'None':
        evaluation = int(exercise['meta']['evaluation']) - 1

    return [
            exercise_meta, 
            exercise_sequence_global_region, 
            exercise_sequence_frontal_region,
            exercise_sequence_oral_region,
            exercise_sequence_orbital_region,
            evaluation
           ]
