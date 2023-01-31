CREATE TABLE users (
    id_pkey VARCHAR(30) PRIMARY KEY,
    display_name NVARCHAR2(256),
    image_url VARCHAR(200),
    followers NUMBER(10),
    access_token VARCHAR(512),
    token_type VARCHAR(20),
    expires_in NUMBER(20),
    expires_at NUMBER(20),
    scope VARCHAR(512),
    refresh_token VARCHAR(512),
    timestamp NUMBER(20)
);
CREATE TABLE playlists (
    id_pkey VARCHAR(22),
    owner_id VARCHAR(30) NOT NULL,
    name NVARCHAR2(256) NOT NULL,
    description NVARCHAR2(300),
    image_url VARCHAR2(512),
    timestamp NUMBER(20),
    PRIMARY KEY (id_pkey)
);
CREATE TABLE albums(
    id_pkey VARCHAR(22) PRIMARY KEY,
    name NVARCHAR2(256),
    image_url VARCHAR2(200),
    release_date VARCHAR(10),
    popularity NUMBER(3),
    timestamp NUMBER(20)
);
CREATE TABLE tracks(
    id_pkey VARCHAR(22) PRIMARY KEY,
    name NVARCHAR2(256) NOT NULL,
    duration_ms NUMBER(7),
    disc_number NUMBER(2),
    track_number NUMBER(3),
    explicit NUMBER(1),
    popularity NUMBER(3),
    timestamp NUMBER(20),
    albums_id_fkey VARCHAR(22),
    FOREIGN KEY (albums_id_fkey) REFERENCES albums(id_pkey)
);
CREATE TABLE genres(
    name NVARCHAR2(64) PRIMARY KEY
);
CREATE TABLE artists(
    id_pkey VARCHAR(22) PRIMARY KEY,
    name NVARCHAR2(256) NOT NULL,
    image_url VARCHAR(200),
    popularity NUMBER(3),
    followers NUMBER(10),
    timestamp NUMBER(20)
);
CREATE TABLE favorites(
    users_id_fkey VARCHAR(30),
    tracks_id_fkey VARCHAR(22),
    PRIMARY KEY (users_id_fkey,tracks_id_fkey),
    FOREIGN KEY (users_id_fkey) REFERENCES users(id_pkey),
    FOREIGN KEY (tracks_id_fkey) REFERENCES tracks(id_pkey)
);
CREATE TABLE album_artists(
    albums_id_fkey VARCHAR(22),
    artists_id_fkey VARCHAR(22),
    PRIMARY KEY (albums_id_fkey,artists_id_fkey),
    FOREIGN KEY (albums_id_fkey) REFERENCES albums(id_pkey),
    FOREIGN KEY (artists_id_fkey) REFERENCES artists(id_pkey)
);
CREATE TABLE playlist_content(
    playlists_id_fkey VARCHAR(22),
    tracks_id_fkey VARCHAR(22),
    PRIMARY KEY (playlists_id_fkey,tracks_id_fkey),
    FOREIGN KEY (playlists_id_fkey) REFERENCES playlists(id_pkey),
    FOREIGN KEY (tracks_id_fkey) REFERENCES tracks(id_pkey)
);
CREATE TABLE track_artists(
    artists_id_fkey VARCHAR(22),
    tracks_id_fkey VARCHAR(22),
    PRIMARY KEY (artists_id_fkey,tracks_id_fkey),
    FOREIGN KEY (artists_id_fkey) REFERENCES artists(id_pkey),
    FOREIGN KEY (tracks_id_fkey) REFERENCES tracks(id_pkey)
);
CREATE TABLE user_playlists(
    playlists_id_fkey VARCHAR(22),
    users_id_fkey VARCHAR(30),
    is_managed NUMBER(1),
    PRIMARY KEY (playlists_id_fkey,users_id_fkey),
    FOREIGN KEY (playlists_id_fkey) REFERENCES playlists(id_pkey),
    FOREIGN KEY (users_id_fkey) REFERENCES users(id_pkey)
);
CREATE TABLE playlist_genres(
    playlists_id_fkey VARCHAR(22),
    playlists_user_fkey VARCHAR(30),
    genres_id_fkey NVARCHAR2(64),
    PRIMARY KEY (playlists_id_fkey,playlists_user_fkey,genres_id_fkey),
    FOREIGN KEY (playlists_id_fkey,playlists_user_fkey) REFERENCES user_playlists(playlists_id_fkey,users_id_fkey),
    FOREIGN KEY (genres_id_fkey) REFERENCES genres(name)
);
CREATE TABLE artist_genres(
    artists_id_fkey VARCHAR(22),
    genres_id_fkey NVARCHAR2(64),
    PRIMARY KEY (artists_id_fkey,genres_id_fkey),
    FOREIGN KEY (artists_id_fkey) REFERENCES artists(id_pkey),
    FOREIGN KEY (genres_id_fkey) REFERENCES genres(name)
);