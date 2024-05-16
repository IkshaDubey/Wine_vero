import pickle5 as pickle
from flask import Flask, request, jsonify, render_template, redirect, url_for,send_from_directory,session
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler  # Import the necessary scaler (e.g., StandardScaler)
 
app = Flask(__name__)
# Color dictionary with RGB values for different categories
app.secret_key = 'your_secret_key_here'  # Required for session use
color_dict = {
    1: (102, 0, 0),  # Pinotage: Deep red
    2: (153, 0, 51),  # Mencía: Ruby red
    3: (204, 102, 102)  # Schiava: Light ruby red
}
 
# Load the model and scaler
Quality_model = pickle.load(open('quality.pkl', 'rb'))
Quality_scaler = pickle.load(open('quality_scalling.pkl', 'rb'))  
Color_model = pickle.load(open('color.pkl', 'rb'))
Color_scaler = pickle.load(open('color_scalling.pkl', 'rb'))  
Taste_model = pickle.load(open('taste.pkl', 'rb'))
Taste_scaler= pickle.load(open('taste_scalling.pkl', 'rb'))  
# Load the scaler used for preprocessing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/drinker')
def drinker():
    return render_template('drinker.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
# @app.route('/drinker/index')
# def drinker_index():
#     return send_from_directory('drinker','index.html')


# @app.route('/quality_FAQ')
# def quality_FAQ():
#     return render_template('quality_FAQ.html')

@app.route('/home')
def home():
    
    return render_template('home.html')
 
@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1, -1))
    # Apply the loaded scaler to transform the new data
    new_data = scaler.transform( np.array(list(data.values())).reshape(1, -1))
    output1 = model.predict(new_data)
    print(output1[0])
    return jsonify({'prediction':int(output1[0])})

# @app.route('/predict',methods=['POST'])
# def predict():
#     data=[float(x) for x in request.form.values()]
#     final_input=scaler.transform(np.array(data).reshape(1,-1))
#     print(final_input)
#     output1=model.predict(final_input)[0]
#     # output2=model2.predict(final_input)[0]
#     # output3=model3.predict(final_input)[0]
#     return render_template("home.html",prediction_text_quality="The predicted quality is: {}".format(output1))
    

# Define a mapping of feature names for each model
feature_mapping = {
    'quality': ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides', 'free_sulphur_dioxide', 'total_sulphur_dioxide','density','pH','sulphates','alcohol'],
    'color': ['pH','citric_acid','fixed_acidity'],
    'taste': ['residual_sugar', 'citric_acid', 'chlorides']
}

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from form
    data = {key: float(value) for key, value in request.form.items()}
    # Save the form data in the session
    session['form_data'] = data

    # Quality prediction
    # Extract features for Quality_model according to the mapping
    quality_features = np.array([data[name] for name in feature_mapping['quality']]).reshape(1, -1)
    # Transform quality features using Quality_scaler
    quality_input = Quality_scaler.transform(quality_features)
    # Predict quality using Quality_model
    quality_output = Quality_model.predict(quality_input)[0]

    # Color prediction
    # Color prediction
    color_features = np.array([data[name] for name in feature_mapping['color']]).reshape(1, -1)
    color_input = Color_scaler.transform(color_features)
    color_output = Color_model.predict(color_input)[0]

    # Get RGB values from the color dictionary
    color_rgb = color_dict.get(color_output, (255, 255, 255))  # Default to white if not found
    
    # Convert RGB tuple to CSS-friendly string
    color_hex = f'#{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}'
    # Extract features for Color_model according to the mapping
    color_features = np.array([data[name] for name in feature_mapping['color']]).reshape(1, -1)
    # Transform color features using Color_scaler
    color_input = Color_scaler.transform(color_features)
    # Predict color using Color_model
    color_output = Color_model.predict(color_input)[0]

    # Taste prediction
    # Extract features for Taste_model according to the mapping
    taste_features = np.array([data[name] for name in feature_mapping['taste']]).reshape(1, -1)
    # Transform taste features using Taste_scaler
    taste_input = Taste_scaler.transform(taste_features)
    # Predict taste using Taste_model
    taste_output = Taste_model.predict(taste_input)[0]
    

    # Combine the predictions and render the template with the results
    prediction_text = f"The predicted quality is: {quality_output}\n" \
                      f"The predicted color is: {color_hex}\n" \
                      f"The predicted taste is: {taste_output}"
    
    return redirect(url_for('results', quality=quality_output, color=color_hex, taste=taste_output))

# @app.route('/results')

# def results():
#     # Retrieve "quality" parameter from the request arguments and ensure it's an integer
#     quality_str = request.args.get('quality', '0')  # Default to '0' if not provided
#     try:
#         quality = int(quality_str)  # Convert to integer
#     except ValueError:
#         quality = 0  # If invalid, default to 0

#     # Render the results page with the quality value
#     return render_template('gauge.html', quality=quality)
@app.route('/results',methods=['GET'])
def results():
    # Retrieve prediction data from the request arguments (query string)
    quality = request.args.get('quality')
    color = request.args.get('color', '#ffffff')  # Default to white
    #color = request.args.get('color')
    taste = request.args.get('taste')
     # Retrieve the form data from the session
    form_data = session.get('form_data', {})  # Default to empty dictionary if not found
    
    # Render the results page with the predictions
    return render_template('gauge.html', quality=quality, color=color, taste=taste,form_data=form_data)





if __name__ == "__main__":
    app.run(debug=True)