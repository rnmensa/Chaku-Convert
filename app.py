from flask import Flask,render_template, request, send_file
import pandas as pd
import simplekml
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def parse_coordinates(coordinates_str):
    geopins = []
    if isinstance(coordinates_str, str):
        for coord in coordinates_str.split(';'):
            parts = coord.strip().split()
            if len(parts) >= 2:
                try:
                    latitude = float(parts[0])
                    longitude = float(parts[1])
                    geopins.append((longitude, latitude))
                except ValueError:
                    print(f"Skipping invalid coordinate: {coord}")
    return geopins

def convert_excel_to_kml(file_path):
    # Read the Excel file
    data = pd.read_excel(file_path)

    # Initialise KML object
    kml = simplekml.Kml()

    # Define a style for polygons
    polystyle = simplekml.Style()
    polystyle.polystyle.color = '7d00ff00'

    # Loop through each row and create a polygon for each farm
    for index, row in data.iterrows():
        farmer_name = row['full_name']
        geopins_raw = row['geographic_boundaries']
        coordinates = parse_coordinates(geopins_raw)

        if coordinates:
            pol = kml.newpolygon(name = farmer_name)
            pol.outerboundaryis = coordinates
            pol.style = polystyle


    kml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "somanya_farms.kml")
    kml.save(kml_file_path)
    return kml_file_path

#Flask route to handle file upload and conversion
@app.route('/', methods =['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #Get the uploaded file
        uploaded_file = request.files.get('file')

        if uploaded_file is None:
            # Return a message if no file is uploaded
            return "No file uploaded. Please select a file.", 400
        

        if uploaded_file.filename.endswith('.xlsx'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)


            #Convert to KML
            kml_file_path = convert_excel_to_kml(file_path)

            #Send the KML file back to the user
            return send_file(kml_file_path, as_attachment=True)
        
            # If file is not an Excel file, return an error message
        return "Invalid file format.Please upload a .xlsx file", 400
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)