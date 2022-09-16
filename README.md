# spotify_export

Potential second part (for December or so): export the actual audio files retrieved from offline storage (quit a bit more involved though).

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

Code is also not very well written, but works. Could be shrinked, but does its job. Also, could fully automate the authentication of the user.
