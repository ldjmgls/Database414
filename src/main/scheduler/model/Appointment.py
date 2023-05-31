import sys
sys.path.append("../db/*")
from db.ConnectionManager import ConnectionManager
import pymssql


class Appointment:
    def __init__(self):
        pass

    def search_schedule(self, date):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        # Assumed that each caregiver has access to all available vaccines, and the 
        # Vaccines table contains the current count of available doses for each vaccine 
        search_schedule = "SELECT C.username, V.name, V.doses \
                           FROM Caregivers C \
                           JOIN Availabilities A ON C.username = A.username \
                           JOIN Vaccines V ON 1=1 \
                           WHERE A.time = %s \
                           ORDER BY C.username"
        try:
            cursor.execute(search_schedule, date)
            print("'caregiver' 'vaccine_name' 'available_doses'")
            for row in cursor:
                print(f"{row[0]} {row[1]} {row[2]}")
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()        

    def check_availability(self, date, vaccine):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        avail_caregiver = None
        avail_dose = None

        get_caregiver = "SELECT C.username \
                         FROM Caregivers C \
                         JOIN Availabilities A ON C.username = A.username \
                         WHERE A.time = %s \
                         ORDER BY C.username"
        get_doses = "SELECT doses FROM Vaccines WHERE name = %s"

        try:
            cursor.execute(get_caregiver, date)
            row = cursor.fetchone()
            if row is None:
                print("No caregiver is available.")
                return None, None
            else:
                avail_caregiver = row[0]

            cursor.execute(get_doses, vaccine)
            row = cursor.fetchone()
            if row is None:     # vaccine name misspelled or not in database
                print("No such vaccine is available.")
                return None, None
            else:               # vaccine doses = 0
                if row[0] == 0:
                    print("Not enough available doses.")
                    return None, None
                else:
                    avail_dose = row[0]
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()  
        
        return avail_caregiver, avail_dose

    # A patient make an appointment with a caregiver
    def save_to_db(self, date, vaccine, caregiver, p_user):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        make_appointment = "INSERT INTO Appointments \
                                (time, vaccine_name, cname, pname) \
                            VALUES (%s , %s, %s, %s)"
        get_this_appointment = "SELECT id FROM Appointments WHERE time = %s AND cname = %s"
        try:
            cursor.execute(make_appointment, (date, vaccine, caregiver, p_user))
            conn.commit()
            cursor.execute(get_this_appointment, (date, caregiver))
            row = cursor.fetchone()
            print(f"Appointment ID: {row[0]}, Caregiver username: {caregiver}")
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()

    def update_availability(self, date, caregiver):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        update_availability = "DELETE FROM Availabilities \
                               WHERE time = %s \
                                 AND username = %s"
        try:
            cursor.execute(update_availability, (date, caregiver))
            # print("Caregiver's availabilities updated")
            conn.commit()
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()

    # Output the scheduled appointments for the current user, either patient or caregiver  
    def show(self, user_flag, username):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        get_appt_4c = "SELECT id, vaccine_name, time, pname FROM Appointments WHERE cname = %s ORDER BY id"
        get_appt_4p = "SELECT id, vaccine_name, time, cname FROM Appointments WHERE pname = %s ORDER BY id"
        try:
            if user_flag == "caregiver":
                cursor.execute(get_appt_4c, username)
                row = cursor.fetchone()
                if row is None:
                    print("No appointments.")
                else:
                    print("'appointment_ID' 'vaccine_name' 'date' 'patient_name'")
                    while row:
                        print(f"{row['id']} {row['vaccine_name']} {row['time']} {row['pname']}")
                        row = cursor.fetchone()
            elif user_flag == "patient":
                cursor.execute(get_appt_4p, username)
                row = cursor.fetchone()
                if row is None:
                    print("No appointments.")
                else:
                    print("'appointment_ID' 'vaccine_name' 'date' 'caregiver_name'")
                    while row:
                        print(f"{row['id']} {row['vaccine_name']} {row['time']} {row['cname']}")
                        row = cursor.fetchone()
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()