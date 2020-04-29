import sqlite3

from fastapi import APIRouter, HTTPException, Response
from models.tracks import Album

router = APIRouter()


@router.on_event("startup")
async def startup():
    router.db_connection = sqlite3.connect("chinook.db")
    router.db_connection.row_factory = sqlite3.Row


@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()


@router.get("/tracks")
async def tracks(page: int = 0, per_page: int = 10):
    cursor = router.db_connection.cursor()
    tracks = cursor.execute(
        "SELECT * FROM tracks ORDER BY trackid LIMIT ? OFFSET ?",
        (per_page, per_page * page),
    ).fetchall()
    return tracks


@router.get("/tracks/composers")
async def tracks_composers(composer_name: str):
    cursor = router.db_connection.cursor()
    cursor.row_factory = lambda cursor, row: row[0]
    songs_names = cursor.execute(
        "SELECT name FROM tracks WHERE composer = ? ORDER BY name", (composer_name,)
    ).fetchall()
    if len(songs_names) == 0:
        raise HTTPException(status_code=404, detail={"error": "Not Found"})
    return songs_names


@router.post("/albums")
async def albums(response: Response, album: Album):
    cursor = router.db_connection.cursor()
    cursor.row_factory = lambda cursor, row: row[0]
    artist = cursor.execute(
        "SELECT artistid FROM artists WHERE artistid = ?", (album.artist_id,)
    ).fetchone()
    if not artist:
        raise HTTPException(status_code=404, detail={"error": "Not Found"})

    album = cursor.execute(
        "INSERT INTO albums (title, artistid) VALUES (?,?)",
        (album.title, int(artist),),
    )
    router.db_connection.commit()
    new_album = album.lastrowid
    album = router.db_connection.execute(
        "SELECT albumid, title, artistid FROM albums WHERE albumid = ?", (new_album,),
    ).fetchone()
    response.status_code = 201
    return album


@router.get("/albums/{album_id}")
async def album(album_id):
    cursor = router.db_connection.cursor()
    album = cursor.execute(
        "SELECT albumid, title, artistid FROM albums WHERE albumid = ?", (album_id,),
    ).fetchone()
    if not album:
        raise HTTPException(status_code=404, detail={"error": "Not Found"})
    return album
