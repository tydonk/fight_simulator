import json
from flask impoer Flask, request, render_template, make_response
from form import TestForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "my precious"

extra = ['Product_Type','Geography','Third']

@app.route("/category", methods=["GET", "POST"])
def index():
    """
    Render form and handle form submission
    """
    form = TestForm(request.form)
    form.category_1.choices = [('', 'Select a Category')] + [(x) for x in enumerate(extra,1)]
    chosen_category_1 = None
    chosen_category_2 = None
    chosen_category_3 = None
    return render_template('index.html', form=form)

@app.route("/category/<int:category_1_id>/", methods=["POST"])
def get_request(category_1_id):
    data = [(x) for x in enumerate(extra,1)
        if x[0] != category_1_id]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route("/category/<int:category_1_id>/<int:category_2_id>/", methods=["POST"])
def get_request(category_1_id,category_2_id):
    data = [(x) for x in enumerate(extra,1)
        if x[0] != category_1_id and x[0] != category_2_id]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response    

if __name__ == "__main__":
    app.run(debug=True)