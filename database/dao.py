from database.DB_connect import DBConnect
from model.state import State

class DAO:
    @staticmethod
    def get_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
        select distinct s_datetime
        from sighting
        where s_datetime >= '1910-01-01 00:00:00' and s_datetime <= '2014-12-31 00:00:00' 
        order by s_datetime asc
        """

        cursor.execute(query)

        for row in cursor:
            if row['s_datetime'].year not in result: # se l'anno non è presente nella lista, lo aggiungo
                result.append(row['s_datetime'].year)
            # di conseguenza se è presente, non lo aggiungo
            # in questo modo ottengo una lista in cui l'anno compare una sola volta

        cursor.close()
        conn.close()
        return result # lista di oggetti datetime

    @staticmethod
    def get_shapes(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
        select distinct shape
        from sighting 
        where year(s_datetime)=%s
        order by shape
        """

        cursor.execute(query,(year,))

        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
        select *
        from state 
        """

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result # lista di oggetti stato

    @staticmethod
    def get_stati_vicini():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
        select distinct state1, state2
        from neighbor 
        where state1 < state2
        """

        cursor.execute(query)

        for row in cursor:
            result.append((row['state1'].upper(), row['state2'].upper()))

        cursor.close()
        conn.close()
        return result  # lista di tuple

    @staticmethod
    def get_edges_weight(year, shape):
        conn = DBConnect.get_connection()

        result_id_map = {}

        cursor = conn.cursor(dictionary=True)

        query="""
        select distinct state, count(*) as num_avvistamenti
        from sighting
        where year(s_datetime)=%s and shape=%s
        group by state
        """
        cursor.execute(query,(year,shape))
        for row in cursor:
            result_id_map[row['state'].upper()] = row['num_avvistamenti']

        cursor.close()
        conn.close()
        return result_id_map