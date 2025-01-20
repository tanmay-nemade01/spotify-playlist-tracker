CREATE TABLE IF NOT EXISTS SPOTIFY.PLAYLISTS.CDC_{{ table_name }} LIKE SPOTIFY.PLAYLISTS.STA_{{ table_name }};
ALTER TABLE SPOTIFY.PLAYLISTS.CDC_{{ table_name }} ADD COLUMN IF NOT EXISTS OP STRING;
ALTER TABLE SPOTIFY.PLAYLISTS.CDC_{{ table_name }} ADD COLUMN IF NOT EXISTS UPDATE_DATETIME TIMESTAMP;
CREATE TABLE IF NOT EXISTS SPOTIFY.PLAYLISTS.{{ table_name }} LIKE SPOTIFY.PLAYLISTS.STA_{{ table_name }};

ALTER TASK IF EXISTS SPOTIFY.PLAYLISTS.TS_INSERT_{{ table_name }} RESUME;

CREATE OR REPLACE TASK SPOTIFY.PLAYLISTS.TS_INSERT_{{ table_name }}
WAREHOUSE = COMPUTE_WH
SCHEDULE = '60 Minutes'
AS
INSERT INTO SPOTIFY.PLAYLISTS.CDC_{{ table_name }}
select 
src.name, 
src.artist, 
src.album, 
src.url, 
'I' as OP,
current_timestamp() as UPDATE_DATETIME 
from 
SPOTIFY.PLAYLISTS.STA_{{ table_name }} src 
full outer join 
SPOTIFY.PLAYLISTS.{{ table_name }} tgt 
on src.name = tgt.name and src.artist = tgt.artist 
where tgt.name is null and tgt.artist is null;


CREATE OR REPLACE TASK SPOTIFY.PLAYLISTS.TS_DELETE_{{ table_name }}
WAREHOUSE = COMPUTE_WH
after SPOTIFY.PLAYLISTS.TS_INSERT_{{ table_name }}
AS
INSERT INTO SPOTIFY.PLAYLISTS.CDC_{{ table_name }}
select 
tgt.name, 
tgt.artist, 
tgt.album, 
tgt.url, 
'D' as OP,
current_timestamp() as UPDATE_DATETIME 
from 
SPOTIFY.PLAYLISTS.STA_{{ table_name }} src 
full outer join 
SPOTIFY.PLAYLISTS.{{ table_name }} tgt 
on src.name = tgt.name and src.artist = tgt.artist 
where src.name is null and src.artist is null;

CREATE OR REPLACE TASK SPOTIFY.PLAYLISTS.TS_UPDATE_TABLE_{{ table_name }}
WAREHOUSE = COMPUTE_WH
after SPOTIFY.PLAYLISTS.TS_DELETE_{{ table_name }}
AS
INSERT OVERWRITE INTO SPOTIFY.PLAYLISTS.{{ table_name }} 
select * from SPOTIFY.PLAYLISTS.STA_{{ table_name }}; 

ALTER TASK SPOTIFY.PLAYLISTS.TS_UPDATE_TABLE_{{ table_name }} RESUME;
ALTER TASK SPOTIFY.PLAYLISTS.TS_DELETE_{{ table_name }} RESUME;
ALTER TASK SPOTIFY.PLAYLISTS.TS_INSERT_{{ table_name }} RESUME;