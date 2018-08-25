#!/usr/bin/env python
import os
import argparse
import sys
import eyed3
from eyed3.id3 import ID3_V1_1

# Value interpretation
def getTagValue(value, file, tags, newtags, cnt):
    value = value.replace("{title}", newtags['title'] if 'title' in newtags.keys() else str(max(tags.tag.title,"")))
    value = value.replace("{artist}", newtags['artist'] if 'artist' in newtags.keys() else str(max(tags.tag.artist,"")))
    value = value.replace("{album}", newtags['album'] if 'album' in newtags.keys() else str(max(tags.tag.album,"")))
    value = value.replace("{year}", newtags['recording_date'] if 'recording_date' in newtags.keys() else str(max(tags.tag.recording_date,"")))
    value = value.replace("{track}", newtags['track_num'] if 'track_num'in newtags.keys() else str(max(tags.tag.track_num, "")))
    value = value.replace("{cnt}", str(cnt))
    return value

def id3update(tags, files):
    cnt = 1
    total = len(files)
    for file in files:
        file_tags = eyed3.load(file, tag_version=ID3_V1_1)
        file_tags.initTag(version = (2,4,0))
        #try: 
        #    print file_tags.tag.title, file_tags.tag.artist, file_tags.tag.track_num, file_tags.tag.recording_date
        #except: 
        #    file_tags.initTag(version = (2,4,0))
        #    pass
        for k in tags:
            v = getTagValue(tags[k], os.path.basename(file), file_tags, tags, cnt)
            if k == 'title':  file_tags.tag.title          = unicode(v, "utf-8")
            if k == 'artist': file_tags.tag.artist         = unicode(v, "utf-8") 
            if k == 'album':  file_tags.tag.album          = unicode(v, "utf-8")
            if k == 'year':   file_tags.tag.recording_date = unicode(v, "utf-8")
            if k == 'track':  file_tags.tag.track_num = ( v, total )
        file_tags.tag.save()
        cnt += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title',  action="store", type=str, help="Title")
    parser.add_argument('--artist', action="store", help="Artist")
    parser.add_argument('--album',  action="store", help="Album")
    parser.add_argument('--year',   action="store", help="Year")
    parser.add_argument('--track',  action='store', help="Track")
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()
    # Check if files were passed through pipe
    if not args.files:
        if not sys.stdin.isatty():
            args.files = sys.stdin.read().splitlines()
        else:
            parser.print_help()
            sys.exit(1)
    # Remove empty elements: ID3 tags which will not change
    id3tags = {k: v for k, v in vars(args).items() if v and k != 'files'}
    id3update(id3tags, args.files)

if __name__ == "__main__":
    main()