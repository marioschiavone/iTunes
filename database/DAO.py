from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    @staticmethod
    def getAlbums(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = '''select a.*,sum(t.Milliseconds) as durataA
                    from album a, track t 
                    where t.AlbumId = a.AlbumId
                    group by a.AlbumId
                    having durataA>%s'''
        cursor.execute(query, (durata,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = '''select distinctrow t1.AlbumId as a1, t2.AlbumId as a2
                    from playlisttrack p1, track t1, track t2, playlisttrack p2
                    where p2.PlaylistId= p1.PlaylistId /*prendo le coppie di canzoni*/
                    and p2.TrackId = t2.TrackId 
                    and p1.TrackId = t1.TrackId
                    and t1.AlbumId<t2.AlbumId'''
        cursor.execute(query)

        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:  # nodi gia filtrati
                result.append((idMap[row["a1"]], idMap[row["a2"]]))

        cursor.close()
        conn.close()
        return result
