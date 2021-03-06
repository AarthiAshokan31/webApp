from flask import Flask, render_template, request
import mysql.connector
import psycopg2
import datetime

application = Flask(__name__)
app = application
@app.route("/", methods=['GET', 'POST'])
def home_page():
    if (request.method == 'POST'):
        if (request.form['database'] == 'mysql'):
            if (request.form['dataset'] == 'instacart'):
                connection = mysql.connector.connect(host='mysql2021.c7wtal8gxuuf.us-east-2.rds.amazonaws.com',
                                                     database='instacart',
                                                     user='mysql2021',
                                                     password='mysql2021')
            elif (request.form['dataset'] == 'instacart_normalized'):
                connection = mysql.connector.connect(host='mysql2021.c7wtal8gxuuf.us-east-2.rds.amazonaws.com',
                                                     database='instacart_normalized',
                                                     user='mysql2021',
                                                     password='mysql2021')
        elif (request.form['database'] == 'redshift'):
            connection = psycopg2.connect(host='redshift2021.cxixtqv0g2ru.us-east-2.redshift.amazonaws.com',
                                          database='dev',
                                          user='redshift2021',
                                          password='Redshift2021',
                                          port="5439")
        cursor = connection.cursor()
        query = request.form['query']
        init_time = datetime.datetime.now()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        end_time = datetime.datetime.now()
        time_elapsed = end_time - init_time
        return render_template('index.html', data=results, time=time_elapsed, selection=request.form)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)