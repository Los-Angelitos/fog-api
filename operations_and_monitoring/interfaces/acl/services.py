from flasgger import swag_from

from inventory.domain.entities import Rfid
from operations_and_monitoring.domain.entities import Thermostat, SmokeSensor
from operations_and_monitoring.infrastructure.repositories import MonitoringRepository
from iam.domain.entities import Device
import requests
from shared.infrastructure.hotelconfig import   BACKEND_URL, HOTEL_ID


class MonitoringFacade:
    def __init__(self):
        self.repository = MonitoringRepository()

    def get_preferences_by_room_id(self, room_id: str) -> dict:
        if room_id == None or room_id == "":
            raise Exception("room_id parameter is necessary")

        #primero hace la solicitud de bookings por room id
        url = f"{BACKEND_URL}/booking/get-all-bookings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._get_auth_token()}"
        }
        params = {
            "hotelId": HOTEL_ID
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching bookings: {response.status_code}")
        bookings = response.json()
        if not bookings:
            print(f"[MonitoringFacade] No bookings found for HOTEL_ID={HOTEL_ID}")
            return {}
        #los que coincidan con el room_id, agarra el ultimo booking y pide preferences
        bookings = [booking for booking in bookings if booking.get("roomId") == room_id]
        booking = bookings[-1] if bookings else None
        print(f"[MonitoringFacade] Last booking for room_id={room_id}: {booking}")
        preference_id = booking.get("preferenceId")
        if not preference_id:
            print(f"[MonitoringFacade] No guest_id found in booking for room_id={room_id}")
            return {}
        #ahora hace la solicitud de preferences por guest_id
        url = f"{BACKEND_URL}/guest-preferences/{preference_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._get_auth_token()}"  # Asegúrate de que el token sea válido
        }
        response = requests.get(url, headers=headers)
        print(f"[MonitoringFacade] guest-preferences response status: {response.status_code}")
        print(f"[MonitoringFacade] guest-preferences raw response: {response.text}")

        if response.status_code != 200:
            raise Exception(f"Error fetching preferences: {response.status_code}")
        preference = response.json()
        if not preference:
            print(f"[MonitoringFacade] No preferences found for preference={preference_id}")
            return {}
        return preference.get("temperature")



    def get_devices_by_room_id(self, room_id: str) -> list[Device]:
        if room_id == None or room_id == "":
            raise Exception("room_id parameter is necessary")

        thermostats = self.repository.get_thermostats()
        smoke_sensors = self.repository.get_smoke_sensors()
        rfid_devices = self.repository.get_rfid()

        devices = thermostats + smoke_sensors + rfid_devices
        
        return [device for device in devices if device.room_id == room_id]

    def get_rfid_by_room_id(self, room_id) -> list[Rfid]:
        print(f"[MonitoringFacade] Entrando a get_rfid_by_room_id con room_id={room_id}")

        if not room_id:
            raise Exception("room_id parameter is necessary")

        #rfids = self.repository.get_rfid()
        #print(f"[MonitoringFacade] Total RFID in DB: {len(rfids)}")

        #result = [r for r in rfids if r.room_id == room_id]
        #print(f"[MonitoringFacade] Found {len(result)} RFID for room_id={room_id}")

        #if result:
            #print("[MonitoringFacade] Returning local RFID readers.")
            #return result

        print("[MonitoringFacade] No local RFID readers found. Fetching from backend...")

        # Paso 1: Obtener token
        token = self._get_auth_token()
        if not token:
            raise Exception("Authentication with backend failed")

        # Paso 2: Obtener RFID readers del backend
        try:
            url = f"{BACKEND_URL}/rfid-card/hotel/{HOTEL_ID}"  # ✅ insertar hotelId en la URL

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            response = requests.get(url, headers=headers)

            print(f"[MonitoringFacade] Backend responded with status code: {response.status_code}")
            if response.status_code != 200:
                raise Exception(f"Error fetching RFID readers: {response.status_code}")

            data = response.json()
            print(f"[MonitoringFacade] Received {len(data)} items from backend.")
            print(f"[MonitoringFacade] Backend raw response text: {response.text}")
            print(f"[MonitoringFacade] Backend parsed JSON: {data}")

            for item in data:
                print(f"[MonitoringFacade] Saving RFID item: {item}")
                self.repository.save_rfid(item)

            # Luego de guardar, consultar nuevamente en local
            rfids = self.repository.get_rfid()
            print(f"[MonitoringFacade] Filtrando por room_id={room_id} (type={type(room_id)})")
            for r in rfids:
                print(f" - RFID room_id={r.room_id} (type={type(r.room_id)})")

            final_result = [r for r in rfids if int(r.room_id) == int(room_id)]
            return final_result

        except Exception as e:
            print(f"[MonitoringFacade] Failed to fetch RFID readers: {e}")
            return []

    def get_thermostats_by_room_id(self, room_id) -> list[Thermostat]:
        if not room_id:
            raise Exception("room_id parameter is necessary")

        thermostats = self.repository.get_thermostats()

        result = [t for t in thermostats if t.room_id == room_id]

        #if result:
        #    return result

        # Si no hay termostatos en la base local, hacer fetch al backend
        print("[MonitoringFacade] No local thermostats found. Fetching from backend...")

        # Paso 1: Obtener token
        token = self._get_auth_token()
        if not token:
            raise Exception("Authentication with backend failed")

        # Paso 2: Obtener termostatos del backend
        try:
            url = f"{BACKEND_URL}/thermostat/get-all-thermostats"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            params = {
                "hotelId": HOTEL_ID
            }
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                raise Exception(f"Error fetching thermostats: {response.status_code}")

            data = response.json()
            for item in data:
                #print(f"[DEBUG] Procesando item: {item}")
                #preference_temp = self.get_preferences_by_room_id(item.get("roomId"))
                #temperature = preference_temp if preference_temp is not None else item.get("temperature", "0")
                #print(f"[DEBUG] Temperatura seleccionada: {temperature}")
                #item["temperature"] = temperature
                #print(f"[DEBUG] Item final antes de guardar: {item}")
                self.repository.save_thermostat(item)

            # Ahora sí los buscas otra vez localmente
            thermostats = self.repository.get_thermostats()
            return [t for t in thermostats if t.room_id == room_id]

        except Exception as e:
            print(f"[MonitoringFacade] Failed to fetch thermostats: {e}")
            return []

    def _get_auth_token(self) -> str:
        """Obtiene el token de autenticación para acceder al backend"""
        try:
            auth_url = f"{BACKEND_URL}/authentication/sign-in"
            payload = {
                "email": "iot@manager.com",
                "password": "string",
                "roleId": 1
            }
            response = requests.post(auth_url, json=payload)
            print(f"[Auth] Status: {response.status_code}, Response: {response.text}")

            if response.status_code != 200:
                print(f"[Auth] Error al autenticar: {response.status_code}")
                return None

            token = response.json().get("token")
            print(f"[Auth] Token recibido: {token}")
            return token
        except Exception as e:
            print(f"[Auth] Excepción durante la autenticación: {e}")
            return None
