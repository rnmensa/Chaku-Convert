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

    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Read the Excel file
    data = pd.read_excel(file_path)

    # Initialise KML object
    kml = simplekml.Kml()

    # Define a style for polygons
    polystyle = simplekml.Style()
    polystyle.polystyle.color = '7d00ff00'

    pinstyle = simplekml.Style()
    pinstyle.iconstyle.color = 'ff0000ff' 

        # Loop through each row and process polygons and pins
    for index, row in data.iterrows():
        farmer_name = row['full_name']
    

 # Handle geographic boundaries for polygons
        geopins_raw = row.get('geographic_boundaries')
        if pd.notna(geopins_raw):
            coordinates = parse_coordinates(geopins_raw)
            if coordinates:
                pol = kml.newpolygon(name=f"{farmer_name} - Boundary")
                pol.outerboundaryis = coordinates
                pol.style = polystyle
        
        # Handle land coordinates for red pins
        land_coords_raw = row.get('land_coordinates')
        if pd.notna(land_coords_raw):
            land_coords = parse_coordinates(land_coords_raw)
            for coord in land_coords:
                pin = kml.newpoint(name=f"{farmer_name} - Marker", coords=[coord])
                pin.style = pinstyle

    kml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_name}.kml")
    kml.save(kml_file_path)
    return kml_file_path

#Flask route to handle file upload and conversion
@app.route('/', methods =['GET', 'POST'])
def upload_file():

    error_message = None 


    if request.method == 'POST':
        #Get the uploaded file
        uploaded_file = request.files.get('file')

        if uploaded_file is None or uploaded_file.filename == "":
            # Return a message if no file is uploaded
            error_message = "No file uploaded. Please select a file."
            return render_template('index.html', error_message=error_message)
        

        if uploaded_file.filename.endswith('.xlsx'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)


            #Convert to KML
            kml_file_path = convert_excel_to_kml(file_path)

            #Send the KML file back to the user
            return send_file(kml_file_path, as_attachment=True)
        
            # If file is not an Excel file, return an error message
        return "Invalid file format.Please upload a .xlsx file", 400
        
    return render_template('index.html', error_message=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)