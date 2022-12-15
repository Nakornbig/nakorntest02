from flask import Flask, render_template, request
import pymysql
app = Flask(__name__)

#################################################################################################################
#################################################################################################################

def getConnection ():
    return pymysql.connect(
        host = 'localhost',
        db = 'games',
        user = 'root',
        password = '',
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
		)

#################################################################################################################

def game_view():
	connection = getConnection()
	sqlgame = "SELECT * FROM game "
	cursor = connection.cursor()
	cursor.execute(sqlgame)
	rows = cursor.fetchall()
	return rows

def topuser_view():
	connection = getConnection()
	sqlgame = "SELECT * FROM topuser "
	cursor = connection.cursor()
	cursor.execute(sqlgame)
	rows = cursor.fetchall()
	return rows

def order_check_view():
	connection = getConnection()
	sqlgame = "SELECT * FROM order_check "
	cursor = connection.cursor()
	cursor.execute(sqlgame)
	rows = cursor.fetchall()
	return rows

def order_complete_view():
	connection = getConnection()
	sqlgame = "SELECT * FROM order_complete "
	cursor = connection.cursor()
	cursor.execute(sqlgame)
	rows = cursor.fetchall()
	return rows

def order_fail_view():
	connection = getConnection()
	sqlgame = "SELECT * FROM order_fail "
	cursor = connection.cursor()
	cursor.execute(sqlgame)
	rows = cursor.fetchall()
	return rows

def game_view_ASC():
	connection = getConnection()
	sqlgame = "SELECT namegame, age, price, amount FROM game ORDER BY amount ASC"
	cursor = connection.cursor()
	cursor.execute(sqlgame)
	rows = cursor.fetchall()
	return rows

#################################################################################################################

@app.route('/')
def games():
	rows = game_view()
	return render_template('games.html',rows=rows)

@app.route('/topuser')
def topuser():
	connection = getConnection()

	sql1 = "SELECT * FROM order_complete ORDER BY timeocp DESC"
	cursor1 = connection.cursor()
	cursor1.execute(sql1)
	rows1 = cursor1.fetchall()

	sql2 = "SELECT nameuser ,sum(priceall), MAX(timelu) FROM topuser GROUP BY nameuser ORDER BY sum(priceall) DESC,timelu DESC"
	cursor2 = connection.cursor()
	cursor2.execute(sql2)
	rows2 = cursor2.fetchall()

	sql3 = "SELECT nameuser ,sum(amountall), MAX(timelu) FROM topuser GROUP BY nameuser ORDER BY sum(amountall) DESC ,timelu DESC"
	cursor3 = connection.cursor()
	cursor3.execute(sql3)
	rows3 = cursor3.fetchall()

	return render_template('topuser.html',rows1=rows1, rows2=rows2, rows3=rows3)

#################################################################################################################

@app.route('/checkorders')
def checkorders():
	rows1 = order_check_view()
	rows2 = order_complete_view()
	rows3 = order_fail_view()
	return render_template('checkorders.html', rows1=rows1, rows2=rows2, rows3=rows3)

#################################################################################################################

@app.route('/result', methods=['POST'])
def search():
	findgames = request.form['inputtext']
	connection = getConnection()
	sql = f"SELECT * FROM game WHERE namegame LIKE '%{findgames}%'"
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	return render_template('games.html', rows=rows)

@app.route('/resultselect', methods=['POST'])
def selectoptions():
	selectoption = request.form['optionselect']
	str(selectoption)
	if(selectoption == "selectedall"):
		rows = game_view()
		return render_template('games.html',rows=rows)
	elif(selectoption == "selectedph"):
		connection = getConnection()
		sql = "SELECT * FROM game ORDER BY price DESC"
		cursor = connection.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		return render_template('games.html',rows=rows)
	elif(selectoption == "selectedpl"):
		connection = getConnection()
		sql = "SELECT * FROM game ORDER BY price ASC"
		cursor = connection.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		return render_template('games.html',rows=rows)
	elif(selectoption == "selectedmh"):
		connection = getConnection()
		sql = "SELECT * FROM game ORDER BY amount DESC"
		cursor = connection.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		return render_template('games.html',rows=rows)
	elif(selectoption == "selectedml"):
		connection = getConnection()
		sql = "SELECT * FROM game ORDER BY amount ASC"
		cursor = connection.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		return render_template('games.html',rows=rows)

#################################################################################################################

@app.route('/orderselect/<namegame>', methods=['POST'])
def order(namegame):
	ordergame = request.form['ordergame']
	zero_check = request.form['amount']
	zero = int(zero_check)
	connection = getConnection()
	rows = game_view()
	if (zero==0):
		msg = 'ห้ามซื้อเกมที่เป็น 0 !!!'
		return render_template('games.html',msg=msg, rows=rows)
	else:
		sql = f"SELECT namegame, namepf , nametype , amount, price, linkimg FROM game INNER JOIN typegame ON game.typegame = typegame.idtg  INNER JOIN platform ON game.platform = platform.idpf WHERE namegame = '{ordergame}'"
		cursor = connection.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		return render_template('order.html', rows=rows)

@app.route('/insertorder',methods = ['POST', 'GET'])
def insertorder_check():
	nameuser = request.form['usernameuser']
	checkname = str(nameuser)
	if(nameuser == ''):
		nameuser = 'ไม่ได้ระบุ'
	namegame = request.form['namegame']
	price = request.form['price']
	status_order = request.form['status_order']
	idg = request.form['idg']
	connection = getConnection()
	sql = "INSERT INTO order_check (nameuser, namegame, price, status_order, timeoc, checkidg) VALUES ('%s','%s','%s','%s',now(),'%s')" % (nameuser, namegame, price, status_order, idg)
	sql2 = "UPDATE game SET amount = amount-1 WHERE namegame = '%s' AND amount !=0" % namegame
	cursor = connection.cursor()
	sql = sql.encode('utf-8')
	cursor.execute(sql)
	cursor.execute(sql2)
	connection.commit()
	return games()

#################################################################################################################

@app.route('/admin',methods = ['POST', 'GET'])
def adminlogin ():
	msg = ''
	username = request.form['username']
	password = request.form['password']
	connection = getConnection()
	cursor = connection.cursor()
	cursor.execute(f"SELECT username, password FROM account_admin WHERE username = '{username}' AND password = '{password}'")
	gg = cursor.fetchone()
	rows = order_check_view()
	rows2 = game_view_ASC()
	if gg :
		username = gg['username']
		password = gg['password']
		return render_template('adminedit.html',rows=rows, rows2=rows2)
	else :
		msg = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง !!!'
		msg2 = '(สำหรับ ADMIN เท่านั้น)'
		return render_template('games.html',msg=msg, msg2=msg2)
		

@app.route('/อัพเดตสถานะผู้ใช้name=<nameuser>เสร็จสิ้น',methods = ['POST', 'GET'])
def updateorder (nameuser):
	idoc = request.form['idoc']
	connection = getConnection()
	sql = f"UPDATE order_check SET status_order = 'กำลังตรวจสอบ' WHERE idoc LIKE '%{idoc}%' "
	cursor = connection.cursor()
	cursor.execute(sql)
	connection.commit()
	rows = order_check_view()
	return render_template('adminedit.html',rows=rows)

@app.route('/อัพเดะผู้ใช้<nameuser>ไปยังorderที่มีปัญหาแล้ว',methods = ['POST', 'GET'])
def inser_order_fail(nameuser):
	namegame = request.form['namegame']
	nameuser = request.form['nameuser']
	notefail = request.form['nf']
	idoc = request.form['idoc']
	idg = request.form['idg']
	connection = getConnection()
	sql = f"INSERT INTO order_fail(nameuser, namegame, notefail, timeof) VALUES('{namegame}','{nameuser}', '{notefail}',now())"
	sql2 = "DELETE FROM order_check WHERE idoc = '%s'" % idoc
	sql3 = "UPDATE game SET amount = amount+1 WHERE idg = '%s'" % idg
	cursor = connection.cursor()
	sql = sql.encode('utf-8')
	cursor.execute(sql)
	cursor.execute(sql2)
	cursor.execute(sql3)
	connection.commit()
	rows = order_check_view()
	return render_template('adminedit.html',rows=rows)


@app.route('/ทำรายการเสร็จสิ้นname=<nameuser>',methods = ['POST', 'GET'])
def inser_order_complete(nameuser):
	namegame = request.form['namegame']
	nameuser = request.form['nameuser']
	idoc = request.form['idoc']
	price = request.form['price']
	connection = getConnection()

	sql = f"INSERT INTO order_complete(nameuser, namegame, timeocp) VALUES('{namegame}','{nameuser}', now())"
	sql2 = "DELETE FROM order_check WHERE idoc = '%s'" % idoc
	sql3 = f"INSERT INTO topuser(nameuser, priceall, amountall, timelu) VALUES('{nameuser}',{int(price)}, {int(1)}, now())"
	cursor = connection.cursor()
	sql = sql.encode('utf-8')
	cursor.execute(sql)
	cursor.execute(sql2)
	cursor.execute(sql3)
	connection.commit()
	rows = order_check_view()
	return render_template('adminedit.html',rows=rows)

@app.route('/เพิ่มเกมใหม่ไปยังระบบแล้ว',methods = ['POST', 'GET'])
def insertgame():
	namegame = request.form['namegame']
	typegame = request.form['typegame']
	age = request.form['age']
	platform = request.form['platform']   
	price = request.form['price']
	amount = request.form['amount']
	linkimg = request.form['linkimg']
	connection = getConnection()
	sql = f"INSERT INTO game(namegame, typegame, age, platform , price, amount, linkimg) VALUES('{namegame}',{int(typegame)},{int(age)},{int(platform)},{int(price)},{int(amount)},'{linkimg}')"
	cursor = connection.cursor()
	sql = sql.encode('utf-8')
	cursor.execute(sql)
	connection.commit()
	rows = order_check_view()
	return render_template('adminedit.html',rows=rows)

@app.route('/อัพเดตจำนวนเกม<namegame>เป็น<amount>เสร็จสิ้น',methods = ['POST', 'GET'])
def updateamount(namegame, amount):
	namegame = request.form['namegame']
	amount = request.form['amount']
	price = request.form['price']
	connection = getConnection()
	sql = "UPDATE game set amount = '%s' WHERE namegame = '%s' AND price = '%s'" % (amount, namegame, price)
	cursor = connection.cursor()
	cursor.execute(sql)
	connection.commit()
	rows = order_check_view()
	rows2 = game_view()
	rows3 = game_view_ASC()
	return render_template('adminedit.html', rows=rows, rows2=rows2, rows3=rows3)

@app.route('/ลบเกม<namegame>แล้ว',methods = ['POST', 'GET'])
def deletegame(namegame):
	namegame = request.form['namegame']
	price = request.form['price']
	amount = request.form['amount']
	connection = getConnection()
	cursor = connection.cursor()
	sql = "DELETE FROM game WHERE namegame = '%s' AND price = '%s' AND amount = '%s'" % (namegame, price, amount)
	cursor.execute(sql)
	connection.commit()
	rows = order_check_view()
	rows2 = game_view()
	rows3 = game_view_ASC()
	return render_template('adminedit.html', rows=rows, rows2=rows2, rows3=rows3)


#################################################################################################################

if __name__ == '__main__':
   app.run(debug = True)

#################################################################################################################