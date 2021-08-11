
import pyodbc
from testphase.settings import DB_NAME, SERVER_NAME


def makeConnectionStatement(Server_Name: str, Database_Name: str) -> str:
    CONNECTION = 'DRIVER={ODBC Driver 17 for SQL Server}; \
                    SERVER=' + Server_Name + ';\
                    DATABASE=' + Database_Name + ';\
                    Trusted_Connection=yes;'
    return CONNECTION


class Database():
    def __init__(self, SERVER: str, DATABASE: str) -> None:
        self._SERVER = SERVER
        self._DATABASE = DATABASE
        self._ConnectionStatement = makeConnectionStatement(
            self._SERVER, self._DATABASE)
        self._connection = pyodbc.connect(self._ConnectionStatement)
        self._cursor = self._connection.cursor()

    @property
    def server(self):
        return self._SERVER

    @property
    def database(self):
        return self._DATABASE

    @property
    def cursor(self):
        return self._cursor

    def close(self):
        self._cursor.close()
        self._connection.close()
        return


def create_DB():
    return Database(SERVER_NAME, DB_NAME)


def fetchVehicleData(VehicleNo: str):
    db = create_DB()
    db.cursor.execute("select * from Vehicles where vehicleNo=?", VehicleNo)
    row = db.cursor.fetchone()
    db.close()
    if row:
        return row
    return None


def fetchServiceData(VehicleNo: str):
    db = create_DB()
    db.cursor.execute(
        "select * from Services where vehicleNo=? Order by ServiceID DESC", VehicleNo)
    if db.cursor:
        return db.cursor
    else:
        return False


def extractVehicleData(VehicleNo: str) -> dict:
    """extractVehicleData will look for vehile in database and return dict if found
    """
    row = fetchVehicleData(VehicleNo)

    if row:
        vehicle_no, brand, model = row
        return {
            "vehicleno": vehicle_no,
            "brand": brand,
            "model": model,
            "services": extractServicesData(vehicle_no)
        }
    else:
        return None


def extractServicesData(VehicleNo: str) -> list:
    data = fetchServiceData(VehicleNo)
    if data:
        serices_list = list()
        for row in data:
            service_id, service_type, _ = row
            serices_list.append([service_id, service_type])
        data.close()
        return serices_list
    else:
        return None


def updateVehileData(vehicalDict: dict):
    try:
        db = create_DB()
        brand = vehicalDict["brand"]
        model = vehicalDict["model"]
        Vehicle_NO = vehicalDict["vehicleno"]
        db.cursor.execute(
            "Update vehicles set brand=? ,model=? where VehicleNo=?", brand, model, Vehicle_NO)
        db.cursor.commit()
        db.close()
        return True
    except:
        raise Exception


def updateServiceData(serviceDict: dict):
    try:
        db = create_DB()
        service_id = serviceDict["serviceid"]
        service_type = serviceDict["servicetype"]
        db.cursor.execute(
            "update services set ServiceType =? where ServiceID=?", service_type, service_id)
        db.cursor.commit()
        db.close
        return True
    except:
        db.close()
        return False


def addVehical(vehicleDict: dict):
    try:
        vehicle_no = vehicleDict["vehicleno"]
        brand = vehicleDict["brand"]
        model = vehicleDict["model"]
        db = create_DB()
        db.cursor.execute(
            "insert into vehicles(vehicleNo,Brand,Model) Values(?,?,?)", vehicle_no, brand, model)
        db.cursor.commit()
        db.close()
        return True
    except:                             # noqa: E722
        return False


def get_service(serviceid: str):
    db = create_DB()
    db.cursor.execute("select * from services where serviceid=?", serviceid)
    if row := db.cursor.fetchone():
        return row
    return None


def add_Service(serviceDict: dict):
    try:
        service_type = serviceDict["servicetype"]
        vehicle_no = serviceDict["vehicleno"]
        db = create_DB()
        db.cursor.execute("insert into services(servicetype,vehicleNo) Values(?,?)",
                          service_type, vehicle_no)
        db.cursor.commit()
        db.close()
        return True
    except:                             # noqa: E722
        db.close()
        return False


def removeVehicle(vehicalNo: str):
    removeService(vehicalNo)
    db = create_DB()
    db.cursor.execute('delete from vehicles where vehicleNo=?', vehicalNo)
    db.cursor.commit()
    db.close()
    return


def removeService(vehicleNo: str):
    db = create_DB()
    db.cursor.execute('delete from services where vehicleNo=?', vehicleNo)
    db.cursor.commit()
    db.close()
    return


def deleteService(serviceid: str):
    try:
        db = create_DB()
        db.cursor.execute('delete from services where ServiceID=?', serviceid)
        db.cursor.commit()
        db.close()
        return True
    except:
        db.close()
        return False


# data = {
#     "vehicleno": '111',
#     "brand": "AB123",
#     "model": "201912"
# }

# updateVehileData(data)
# print(extractVehicleData("12345"))
# addVehical(vehicle_data)
