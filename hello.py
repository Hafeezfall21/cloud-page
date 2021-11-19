import os
from flask import Flask, render_template_string, request
from flask.templating import render_template

app = Flask(__name__)
@app.route("/fun", methods = ["POST"])
def fun():
    f = request.form.get("selectedfile")
    fn = f
    f = open('./logs/'+f, 'r')
    log = f.read()
    f.close()
    
    hrs = 0
    mins = 0
    log = log.splitlines()
    
    for l in log:
        if 'am' in l or 'pm' in l:
            f = 0
            for i in range(len(l)):
                if f > 2:
                    break
                if f == 0 and (l[i:i+2]=='am' or l[i:i+2] == 'pm'):
                    st = l[i-5:i]
                    f += 1
                elif f == 1 and (l[i:i+2]=='am' or l[i:i+2] == 'pm'):
                    en = l[i-5:i]
                    f += 1
                elif f == 2:
                    m_st = int(st[-2:])
                    m_end = int(en[-2:])
                    h_st = int(st[:2].strip())
                    h_end = int(en[:2].strip())
                    
                    mi = 0
                    hr = 0
                    
                    if m_st > m_end:
                        mi = 60 - (m_st-m_end)
                        hr = hr - 1
                    else:
                        mi = m_end - m_st

                    if h_st > h_end:
                        hr = hr + (12 - (h_st - h_end))
                    else:
                        hr = hr + h_end - h_st
                    
                    hrs += hr
                    mins += mi
                    
                    f = 0
                    break
            
    hrs += (mins//60)
    mins = (mins%60)
    return render_template_string("""
    <br>
    <br>
    <br>
    <br>
    <center>Time taken for {f}:{t}</center>
    """).format(f=fn, t = str(str(hrs)+' hours'+ str(mins)+' minutes'))


@app.route("/")
def hello_world():

    files = os.listdir(".//logs")
    print(files)

    return render_template('A.html', files = files)

if __name__ == '__main__':
    app.run(debug=True)