# spotify_export

Raw data is also kept track in case need to go back and reorder. The formatted csv files use these headers. Saved
albums will not have an added_at entry.
- name
- artist(s)
- album
- added_at
- duration_ms
- explicit

Liked songs, saved albums, and playlists (both private and collaborative).

Not worrying about potential commas in song names, artists, etc. Resolve in the future if needbe. Will have the row
as well, so can always reformat.

Local files are not returned from the saved tracks api endpoint. I have many of these saved, but will need to
reference the Spotify Local Music folder for completeness.

Follow Spotify made playlists to export like Your Top Songs 20XX, On Repeat, Your Summer Rewind, etc.
