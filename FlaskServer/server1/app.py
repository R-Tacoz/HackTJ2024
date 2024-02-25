from flask import Flask, render_template, request, url_for, redirect
import logging as log
import time
log.basicConfig(level=log.DEBUG)
app = Flask(__name__)

gabe_data = {
    'george': "dumb",
    'james': "smart",
    'jenry': "red",
}
temp_data = {'time': 'none'}
red_data = {'time': 'redirecting...'}

@app.route('/')
def home():
    log.info("Someone is landing on the root page")
    time.sleep(2)
    return render_template('index.html', data=gabe_data)

@app.route('/gabe', methods=['GET', 'POST'])
def gabe():
    log.info("Someone landed on gabe")
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template("step.html", data=temp_data)

@app.route('/redirected', methods=['GET', 'POST'])
def redirected():
    log.info("Someone is about to get redirected")
    if request.method == 'POST':
        return redirect(url_for('gabe'))
    
    return render_template('tictactoe.html')

app.debug = True
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)