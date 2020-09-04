from lib.medicine_database import MedicineDatabase

mm = MedicineDatabase()
for med in mm.db.child("medicine").get().each():
    mm.db.child("medicine").child(med.key()).remove()