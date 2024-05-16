from flask import render_template

# Import the blueprint instance
from . import drinker_blueprint

# Define routes
@drinker_blueprint.route('/')
def index():
    return render_template('drinker/index.html')
