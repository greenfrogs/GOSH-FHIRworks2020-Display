from fhir_parser import FHIR
import serial
from time import sleep

fhir = FHIR()

current_patient = None
observations = None
cur_ob = 0

with serial.Serial('COM7', 9600, timeout=10) as ser:
    ser.flush()
    sleep(1)
    ser.write(b"!FHIR Hackathon!")
    ser.write(b"Waiting....")
    print("Finished starting")
    current_uuid = '8f789d0b-3145-4cf2-8504-13159edaa747'
    while True:
        value = ser.readline().decode('ASCII')
        print(value)
        if value.startswith("PATIENT:"):
            uuid = value.split(":")[1]
            uuid = uuid[:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:]
            try:
                current_patient = fhir.get_patient(uuid)
                current_uuid = uuid
            except ConnectionError:
                pass
            observations = None
            ser.write((current_patient.name.prefix + current_patient.name.given).ljust(16).encode('ASCII'))
            ser.write((current_patient.name.family).ljust(16).encode('ASCII'))
        if value.startswith("SELECT"):
            sleep(0.2)
            print("SELECT pressed")
            uuid = '8f789d0b-3145-4cf2-8504-13159edaa747'
            current_uuid = uuid
            current_patient = fhir.get_patient(current_uuid)
            observations = None
            ser.write((current_patient.name.prefix + current_patient.name.given).ljust(16).encode('ASCII'))
            ser.write((current_patient.name.family).ljust(16).encode('ASCII'))
        if value.startswith("RIGHT"):
            print("RIGHT pressed")
            sleep(0.2)
            ser.write((current_patient.birth_date.isoformat()).ljust(16).encode('ASCII'))
            ser.write((' '.join(current_patient.communications.languages)).ljust(16).encode('ASCII'))
        if value.startswith("LEFT"):
            print("LEFT pressed")
            sleep(0.2)
            ser.write((str(current_patient.marital_status)).ljust(16).encode('ASCII'))
            ser.write(((current_patient.telecoms[0].number)).ljust(16).encode('ASCII'))
        if value.startswith("UP"):
            print("UP pressed")
            sleep(0.2)
            if observations is None:
                observations = fhir.get_patient_observations(current_patient.uuid)
                cur_ob = 0
            if cur_ob != 0:
                cur_ob -= 1
            ser.write((str(observations[cur_ob].components[0].display)).ljust(16).encode('ASCII'))
            ser.write(((str(observations[cur_ob].components[0].quantity()))).ljust(16).encode('ASCII'))
        if value.startswith("DOWN"):
            print("DOWN pressed")
            sleep(0.2)
            if observations is None:
                observations = fhir.get_patient_observations(current_patient.uuid)
                cur_ob = 0
            if cur_ob < len(observations):
                cur_ob += 1
            ser.write((str(observations[cur_ob].components[0].display)[:16] if len(observations[cur_ob].components[0].display) > 16 else observations[cur_ob].components[0].display).ljust(16).encode('ASCII'))
            print(observations[cur_ob].components[0].quantity())
            ser.write(((str(observations[cur_ob].components[0].quantity()))).ljust(16).encode('ASCII'))