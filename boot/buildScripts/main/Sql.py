import pymysql

class SqlCls:

    itemList = {}

    def __init__(self) -> None:
        pass

    @staticmethod
    def mainDo():
        conn = pymysql.connect(host='localhost'
                            # 用户名
                            , user='root'
                            # 密码
                            , passwd='161432'
                            # 端口，默认为3306
                            , port=3306
                            # 数据库名称
                            , db='minecraft'
                            # 字符编码
                            , charset='utf8'
                            )

        cur = conn.cursor()  # 生成游标对象

        # 清空表数据
        sql = "truncate table item"
        cur.execute(sql)  # 执行SQL语句

        for k, v in SqlCls.itemList.items():
            sql = "insert into item(strID, name) values('" + k + "', '" + v + "')"
            cur.execute(sql)  # 执行SQL语句
            conn.commit()
            # data = cur.fetchall()  # 通过fetchall方法获得数据

        cur.close()  # 关闭游标
        conn.close()  # 关闭连接
