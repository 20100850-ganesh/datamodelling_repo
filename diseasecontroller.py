import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="proto",
    password="password",
    database="ricediseasesdb"
)

class_name_to_db_name = {
    'bacterial_leaf_blight': 'Bacterial Leaf Blight',
    'bacterial_leaf_streak': 'Bacterial Leaf Streak',
    'brown_spot': 'Brown Spot',
    'grassy_stunt_virus': 'Rice Grassy Stunt Virus',
    'narrow_brown_spot': 'Narrow Brown Spot',
    'ragged_stunt_virus': 'Rice Ragged Stunt Virus',
    'rice_blast': 'Rice Blast',
    'rice_false_smut': 'False Smut',
    'sheath_blight': 'Sheath Blight',
    'sheath_rot': 'Sheath Rot',
    'stem_rot': 'Stem Rot',
    'tungro_virus': 'Tungro Virus'
}


def get_disease_info(name):
    if name == 'healthy_rice_plant':
        return {'message': 'Your rice plant is healthy!'}, 200

    db_name = class_name_to_db_name.get(name)
    if not db_name:
        return {'error': 'Disease not found'}, 404

    cursor = db.cursor()

    # Get the disease information from the `diseases` table
    query = "SELECT * FROM diseases WHERE name = %s"
    params = (db_name,)
    cursor.execute(query, params)
    disease = cursor.fetchone()

    if not disease:
        return {'error': 'Disease not found'}, 404

    disease_id, disease_name, disease_description = disease

    # Get the control methods for the disease from the `control_methods` table
    query = "SELECT method FROM control_methods WHERE disease_id = %s"
    params = (disease_id,)
    cursor.execute(query, params)
    control_methods = [method for method, in cursor]

    disease_info = {
        'name': db_name,
        'info': disease_description,
        'control_methods': control_methods
    }

    return disease_info, 200
