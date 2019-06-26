import pymysql
import MySQLdb
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from DBUtils.PooledDB import PooledDB

app = Flask(__name__)

app.config['SECRET_KEY'] = 'laowangaigebi'  # 设置session加密的密钥

pymysql.install_as_MySQLdb()
# 设置连接数据库的URL
pool = MySQLdb.connect(MySQLdb, 5, host='localhost', user='root', passwd='abcd1234', db='f1_User', port=3306)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:abcd1234@127.0.0.1:3306/f1_User'

# 数据库和模型类同步修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
# 控制在连接池达到最大值后可以创建的连接数
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5
# 绑定数据库到app配置文件
db = SQLAlchemy(app)


# 创建模型类型
class Type(db.Model):
    # 表名
    __tablename__ = 'tbl_types'

    # 字段
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(8), unique=True)  # 唯一

    # 反向查找 数据库中不会存在
    heros = db.relationship('Hero', backref='type')


class Hero(db.Model):
    # 表名
    __tabliname__ = 'tbl_heros'

    # 字段
    id = db.Column(db.Integer, primary_key=True)
    heroname = db.Column(db.String(16), unique=True)
    gender = db.Column(db.String(16))
    type_id = db.Column(db.Integer, db.ForeignKey('tbl_types.id'))


@app.route('/')
def types():
    typel = Type.query.all()
    return render_template('type.html', type=typel)


@app.route('/hero/')
def hero():
    id = request.args.get('id')
    type = Type.query.get(id)
    hero = type.heros

    return render_template('hero.html', hero=hero)


if __name__ == '__main__':
    app.run(debug=True)
    # db.drop_all()  # 清除所有数据库中的表
    # db.create_all()  # 创建表
    #
    # type1 = Type(name='射手')
    # db.session.add(type1)  # 添加到对话
    #
    # type2 = Type(name='法师')
    # type3 = Type(name='坦克')
    # type4 = Type(name='刺客')
    # type5 = Type(name='辅助')
    # db.session.add_all([type2,type3,type4,type5])  # 添加多个
    # db.session.commit()
    #
    # hero1 = Hero(heroname='后羿', gender='男', type_id=type1.id)
    # hero2 = Hero(heroname='程咬金', gender='男', type_id=type3.id)
    # hero3 = Hero(heroname='王昭君', gender='女', type_id=type2.id)
    # hero4 = Hero(heroname='安琪拉', gender='女', type_id=type2.id)
    # hero5 = Hero(heroname='兰陵王', gender='男', type_id=type4.id)
    # hero6 = Hero(heroname='李白', gender='男', type_id=type4.id)
    # hero7 = Hero(heroname='韩信', gender='男', type_id=type4.id)
    #
    #
    # db.session.add_all([hero1,hero2,hero3,hero4,hero5,hero6,hero7])  # 添加多个
    # db.session.commit()
