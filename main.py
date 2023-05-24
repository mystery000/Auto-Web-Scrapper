from flask import *  
from flask_cors import CORS
from flaskwebgui import FlaskUI
import webbrowser
from scraper import scrape_url
import autopost 
app = Flask(__name__,
static_folder='./templates/static')
app.debug = True
CORS(app)    
# ui = FlaskUI(app,fullscreen=True,port=5000)
results = []
@app.route("/")
def hello():  
    return render_template('index.html')

@app.route("/home", methods=['GET'])
def home(): 
    return render_template('some_page.html')

@app.route("/run_scrape", methods=['GET','POST'])
def run_scrape():
    if(request.method == 'POST'):
        global results
        data = json.loads(request.data)
        urls = data['urls']
        urls = urls.strip().split('\n')
        results  = []
        s_count = 0
        f_count = 0
        #try:
        for url in urls:
            result , s, f = scrape_url(url.strip())
            results +=result
            s_count += s
            f_count += f
        if(len(results) > 0):
            return jsonify({'success' : True,'s_count' : s_count , 'f_count' :f_count})
        else:
            return jsonify({'success' : False,'message' : 'No results'})
            #except Exception as e:
            #return jsonify({'success' : False , 'message' : str(e)})

@app.route("/run_post", methods=['GET','POST'])
def run_post():
    if(request.method == 'POST'):
        data = json.loads(request.data)
        username = data['username']
        password = data['password']
        try:
            s_count , f_count = autopost.run_post(username , password , results)
            return jsonify({'success' : True,'s_count' : s_count , 'f_count':f_count})
        except Exception as e:
            return jsonify({'success' : False , 'message' : str(e)})

if __name__ == "__main__":
    # app.run() for debug
    
    webbrowser.open_new('http://localhost:5000')
    app.run()
