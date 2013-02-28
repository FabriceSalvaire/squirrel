#! /usr/bin/env python
# -*- Python -*-

####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import argparse
import sys

###################################################################################################

from Babel.DataBase.WordDataBase import WordDataBase, PartOfSpeechTagRow
from Babel.Tools.ProgramOptions import PathAction
from PartOfSpeechTags import part_of_speech_tags

####################################################################################################
#
# Options
#

argument_parser = argparse.ArgumentParser(description='Make BNC DataBase.')

argument_parser.add_argument('sqlite_file', metavar='FILE.sqlite',
                             action=PathAction,
                             help='SQLite file')

argument_parser.add_argument('--word-count-min',
                             dest='word_count_min',
                             type=int,
                             default=10,
                             help='Minimum word count [10]')


args = argument_parser.parse_args()

####################################################################################################

database = WordDataBase(args.sqlite_file)

part_of_speech_tag_dict = {}
part_of_speech_tag_table = database.part_of_speech_tag_table
for tag, comment in part_of_speech_tags.iteritems():
    part_of_speech_tag_row = PartOfSpeechTagRow(tag=tag, comment=comment)
    part_of_speech_tag_dict[tag] = part_of_speech_tag_row
    part_of_speech_tag_table.add(part_of_speech_tag_row)
part_of_speech_tag_table.commit()

word_count_min = args.word_count_min
word_table = database.word_table
rank = 0
with sys.stdin as file_input:
    for line in file_input:
        word_count, word, tag, file_count = line.split(' ')
        if tag != '!!ANY' and int(word_count) > word_count_min:
            try:
                tag = tag.upper()
                # part_of_speech_tag_row = part_of_speech_tag_table.select_by(tag=tag).one()
                part_of_speech_tag_row = part_of_speech_tag_dict[tag]
                word_table.add_new_row(word=word,
                                       part_of_speech_tag_id=part_of_speech_tag_row.id,
                                       rank=rank,
                                       count=word_count,
                                       file_count=file_count,
                                       )
                rank += 1
                if rank % 10000 == 0:
                    print "Rank %u" % rank
                    word_table.commit()
            except:
                print "Error:", line
word_table.commit()

####################################################################################################
# 
# End
# 
####################################################################################################
