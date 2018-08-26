## Simple ID3 tag/mp3 file name changing utility

### Usage: 
```
python core.py --title "{artist}: {album}-{cnt}" --album "My new album" --artist "Una persona" --year "2018" mp3_filenames
```
It is possible to pipe list of mp3 files to the app i.e.
```
find ../data -name "*.mp3" | python core.py --artist "Una Persona" --album "My great music" --name "{artist}: {album}-{cnt}"
```
### Application macros/parameters:
- artist    - mp3 tag 'artist'
- album     - mp3 tag 'album'
- title     - mp3 tag 'title'
- year      - mp3 tag 'recording_date'
- track     - mp3 tag 'track_num'
- name      - mp3 file name