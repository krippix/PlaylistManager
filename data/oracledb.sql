CREATE TABLE USERS (
    id_pkey VARCHAR(22) PRIMARY KEY,
    display_name NVARCHAR2(30) NOT NULL,
    image_url VARCHAR(200),
    api_token VARCHAR(32),
    expires_at NUMBER(20),
    username VARCHAR(30) NOT NULL,
    email VARCHAR(256),
    timestamp NUMBER(20)
);
CREATE TABLE PLAYLISTS (
    id_pkey VARCHAR(22) PRIMARY KEY,
    users_id_fkey VARCHAR(22) NOT NULL,
    FOREIGN KEY (user_id_fkey) REFERENCES USERS(id_pkey),
    name NVARCHAR2(64) NOT NULL,
    description NVARCHAR2(300),
    image_url VARCHAR2(200),
    timestamp NUMBER(20)
);
CREATE TABLE TRACKS(
    id_pkey VARCHAR(22) PRIMARY KEY,
    name NVARCHAR2(64) NOT NULL,
    duration_ms NUMBER(7),
    disc_number NUMBER(2),
    explicit NUMBER(1),
    timestamp NUMBER(20)
);
CREATE TABLE GENRES(
    id_pkey NUMBER(4) PRIMARY KEY,
    name NVARCHAR2(64) NOT NULL
);
CREATE TABLE ALBUMS(
    id_pkey VARCHAR(22) PRIMARY KEY,
    name NVARCHAR2(64) NOT NULL,
    image_url VARCHAR2(200),
    release_date NUMBER(20),
    timestamp NUMBER(20)
);
CREATE TABLE ARTISTS(
    id_pkey VARCHAR(22) PRIMARY KEY,
    name NVARCHAR2(64) NOT NULL,
    image_url VARCHAR(200),
    timestamp NUMBER(20)
);
CREATE TABLE FAVORITES(
    users_id_fkey VARCHAR(22),
    tracks_id_fkey VARCHAR(22),
    PRIMARY KEY (users_id_fkey,tracks_id_fkey),
    FOREIGN KEY (users_id_fkey) REFERENCES USERS(id_pkey),
    FOREIGN KEY (tracks_id_fkey) REFERENCES TRACKS(id_pkey)
);
CREATE TABLE PLAYLIST_CONTENT(
    playlists_id_fkey VARCHAR(22),
    tracks_id_fkey VARCHAR(22),
    PRIMARY KEY (playlists_id_fkey,tracks_id_fkey),
    FOREIGN KEY (playlists_id_fkey) REFERENCES PLAYLISTS(id_pkey),
    FOREIGN KEY (tracks_id_fkey) REFERENCES TRACKS(id_pkey)
);
CREATE TABLE ALBUM_CONTENT(
    albums_id_fkey VARCHAR(22),
    tracks_id_fkey VARCHAR(22),
    PRIMARY KEY (albums_id_fkey,tracks_id_fkey),
    FOREIGN KEY (albums_id_fkey) REFERENCES ALBUMS(id_pkey),
    FOREIGN KEY (tracks_id_fkey) REFERENCES TRACKS(id_pkey)
);
CREATE TABLE TRACK_ARTISTS(
    albums_id_fkey VARCHAR(22),
    tracks_id_fkey VARCHAR(22),
    PRIMARY KEY (albums_id_fkey,tracks_id_fkey),
    FOREIGN KEY (albums_id_fkey) REFERENCES ALBUMS(id_pkey),
    FOREIGN KEY (tracks_id_fkey) REFERENCES TRACKS(id_pkey)
);
CREATE TABLE PLAYLIST_GENRES(
    playlists_id_fkey VARCHAR(22),
    genres_id_fkey NUMBER(4),
    PRIMARY KEY (playlists_id_fkey,genres_id_fkey),
    FOREIGN KEY (playlists_id_fkey) REFERENCES PLAYLISTS(id_pkey),
    FOREIGN KEY (genres_id_fkey) REFERENCES GENRES(id_pkey)
);
CREATE TABLE ARTIST_GENRES(
    artists_id_fkey VARCHAR(22),
    genres_id_fkey NUMBER(4),
    PRIMARY KEY (artists_id_fkey,genres_id_fkey),
    FOREIGN KEY (artists_id_fkey) REFERENCES ARTISTS(id_pkey),
    FOREIGN KEY (genres_id_fkey) REFERENCES GENRES(id_pkey)
);