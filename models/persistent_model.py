from db.db import get_connection

class DatabaseError(Exception):
    pass
class PersistentModel:
    table_name = None # to be defined by the subclasses
    table_fields = [] # to be defined by the subclasses
    def __init__(self, id=None):
        self.id = id

    def save(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            field_values = tuple(getattr(self, field) for field in self.table_fields)
            if self.id is None:
                placeholders = ",".join("?" for _ in self.table_fields)
                fields = ",".join(self.table_fields)
                query = f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
                cursor.execute(query, field_values)
                self.id = cursor.lastrowid
            else:
                set_clause = ", ".join(f"{field}=?" for field in self.table_fields)
                query = f"UPDATE {self.table_name} SET {set_clause} WHERE id=?"
                cursor.execute(query, field_values + (self.id,))
            conn.commit()
            return self
        except Exception as e:
            raise DatabaseError(f"Error en Base de datos {e}") from e
        finally:
            conn.close()

    def delete(self):
        if self.id is None:
            return
        conn =self.get_connection()
        cursor = conn.cursor()
        try:
            query = f"DELETE FROM {self.table_name} WHERE id=?"
            cursor.execute(query, (self.id,))
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Error en Base de datos {e}") from e
        finally:
            conn.close()

    @classmethod
    def get_one(cls, field=None, value=None): 
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            fields = ",".join(cls.table_fields)
            if field:
                query = f"SELECT id, {fields} FROM {cls.table_name} WHERE {field}=?"
                cursor.execute(query, (value,))
                row = cursor.fetchone()
        except Exception as e:
            raise DatabaseError(f"Error en Base de datos {e}") from e
        finally:
            conn.close()
        if row:
            field_data = {field: row[i + 1] for i, field in enumerate(cls.table_fields)}
            return cls( **field_data, id=row[0])
        return cls()

    @classmethod
    def get_all(cls, field=None, value=None): # returns Objects list or []
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            fields = ",".join(cls.table_fields)
            if field:
                query = f"SELECT id, {fields} FROM {cls.table_name} WHERE {field}=?"
                cursor.execute(query, (value,))
            else:
                query = f"SELECT id, {fields} FROM {cls.table_name}"
                cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Error en Base de datos {e}") from e
        finally:
            conn.close()
        all_data = []
        for row in rows:
            field_data = {field: row[i + 1] for i, field in enumerate(cls.table_fields)}
            all_data.append(cls(**field_data, id=row[0]))
        return all_data

    @classmethod
    def get_connection(cls):
        try:
            return get_connection()
        except Exception as e:
            raise DatabaseError(f"Error en Base de datos {e}") from e

