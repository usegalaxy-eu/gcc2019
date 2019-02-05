#!/usr/bin/env python

import argparse
import numpy
import pandas as pd
import re

from pathlib import Path


my_path = Path(__file__).resolve() # resolve to get rid of any symlinks


def get_training(l):
    '''Get the trainings for a cell'''
    return [x.split('(http://')[0].strip() for x in str(l).split('), ')]


def get_topic(training):
    '''Get topic for a training
    
    # Proteomics/Metabolomics
    # Epigenetics
    # Admin/Dev
    # Metagenomics/Assembly
    # Diverse Communities
    # Transcriptomics/Genome Variation
    '''
    split_training = training.split(' - ')
    if len(split_training) > 1:
        if split_training[1].startswith('step'):
            topic = 'Admin/Dev'
        else:
            topic = split_training[1]
            if 'Assembly' in topic:
                topic = 'Metagenomics/Assembly'
            elif re.search(r'(RNA|variant)', topic):
                topic = 'Transcriptomics/Genome Variation'
            elif 'Proteomics' in topic:
                topic = 'Proteomics/Metabolomics'
    elif re.search(r'(Trainer|Jupyter|open source project|Machine|Complex|HTS Data)', training):
        topic = 'Misc'
    elif re.search(r'(Code|BioBlend|Kubernetes|Galaxy Tool|WGS|Interactive|Visualisation development)', training):
        topic = 'Admin/Dev'
    elif re.search(r'(biodiversity|RADseq)', training):
        topic = 'Diverse Communities'
    elif 'Metabolomics' in training:
        topic = 'Proteomics/Metabolomics'
    elif re.search(r'(Introduction|Beyond the|Quality control)', training):
        topic = 'Introduction'
    elif 'Metatranscriptomics' in training:
        topic = 'Metagenomics/Assembly'
    else:
        topic = ''
    return topic
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Aggregate training votes')
    parser.add_argument('--input', help='path to CSV file containing votes from the Google form')
    parser.add_argument('--output', help='path to the output CSV file containing aggregated votes')
    args = parser.parse_args()

    # extract dataframe, keep only interesting columns and remove the test line
    vote_df = (pd.read_csv(Path(args.input))
                 .iloc[:,3:7])
    # get list of topics
    topics = set([item for l in vote_df.values.flatten().tolist() for item in get_training(l)])
    # create the aggregated vote dataframe 
    aggregated_votes_df = pd.DataFrame(0, index=topics, columns=['topics', 'raw counts', 'normalized counts'])
    aggregated_votes_df['topics'] = [get_topic(x) for x in aggregated_votes_df.index]
    # fill the aggregated vote dataframe
    for index, row in vote_df.iterrows():
        voted_trainings = get_training(', '.join(row.dropna().tolist()))
        if 'ChIP-seq data analysis, Hi-C analysis, Galaxy for proteogenomics, Train the Galaxy Trainer' in voted_trainings:
            continue
        aggregated_votes_df.loc[voted_trainings, 'raw counts'] += 1
        aggregated_votes_df.loc[voted_trainings, 'normalized counts'] += 1/len(voted_trainings)
    aggregated_votes_df = (aggregated_votes_df.sort_values(['topics', 'raw counts'], ascending=False)
                                              .iloc[:-1])
    # save it to csv
    aggregated_votes_df.to_csv(Path(args.output))
