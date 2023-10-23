from app import app
@app.route("/minutes")
def minutes():
    return "This is minutes contorller"