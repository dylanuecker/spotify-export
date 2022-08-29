# spotify_export

Works as of now, but is very poorly documented and I will probably forget how to run this a week from now. Should be
using better path names. Authentication is not automatic at all, but for my personal use of exporting my music data it
is good enough. Also, not doing a good enough job of sanitizing the data used in the csv files, as I am sure some song
name as a comma in it. Consider using | as a delimiter instead.

Code is also not very well written, but works. Could be shrinked, but does its job. 

**Follow Spotify made playlists to export like Your Top Songs 20XX, On Repeat, etc.**

Raw data is also kept track in case need to go back and reorder. The formatted csv files use these headers. Saved
albums will not have an added_at entry.
- name
- artist(s)
- album
- added_at
- duration
- explicit

Liked songs, saved albums, and playlists (both private and collaborative).

Not worrying about potential commas in song names, artists, etc. Resolve in the future if needbe. Will have the row
as well, so can always reformat.

Local files are not returned from the saved tracks api endpoint. I have many of these saved, but will need to
reference the Spotify Local Music folder for completeness.
