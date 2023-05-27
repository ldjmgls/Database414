import sys
sys.path.append("../db/*")
from db.ConnectionManager import ConnectionManager
import pymssql


class Appointment:
    def __init__(self, date, vaccine):
        self.date = date
        self.vaccine = vaccine

    # A patient make an appointment with a caregiver
    def save_to_db(self, id, caregiver, p_user):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        make_appointment = "INSERT INTO Appointments VALUES (%d, %s , %s, %s, %s)"
        try:
            cursor.execute(make_appointment, (id, self.date, self.vaccine, caregiver, p_user))
            conn.commit()
        except pymssql.Error:
            # print("Error occurred when making appointment")
            raise
        finally:
            cm.close_connection()

    # Output the scheduled appointments for the current user, either patient or caregiver  
    def get(self, user, name):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        get_appt_4c = "SELECT id, vaccine_name, time, pname FROM Appointments WHERE cname = %s ORDER BY id"
        get_appt_4p = "SELECT id, vaccine_name, time, cname FROM Appointments WHERE pname = %s ORDER BY id"
        try:
            if user == "caregiver":
                cursor.execute(get_appt_4c, name)
                print("'appointment_ID' 'vaccine_name' 'date' 'patient_name'")
                for row in cursor:
                    print(f"{row['id']} {row['vaccine_name']} {row['time']} {row['pname']}")
                # return self
            elif user == "patient":
                cursor.execute(get_appt_4p, name)
                print("'appointment_ID' 'vaccine_name' 'date' 'caregiver_name'")
                for row in cursor:
                    print(f"{row['id']} {row['vaccine_name']} {row['time']} {row['cname']}")
                # return self
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()
        return None        