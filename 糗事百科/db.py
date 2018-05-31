import pymysql.cursors
import configure

conn = None

# 简单封装一下两个MOD
def __DMLExecutionMod(sql):
	global conn

	try:
		with conn.cursor() as cursor:
			cursor.execute(sql)
		conn.commit()
	except Exception as e:
		conn.rollback()
		print ("DB Exception: %s", e)

def __DQLExecutionMod(sql):
	global conn

	try:
		with conn.cursor() as cursor:
			cursor.execute(sql)
			res = cursor.fetchall()
		conn.commit()
	except Exception as e:
		conn.rollback()
		print ("DB Exception: %s", e)
	
	return res

# Connect
def DBconnect():
	global conn

	config = {
		'host':configure.DB_HOST,
		'port':configure.DB_PORT,
		'user':configure.DB_USER,
		'password':configure.DB_PASSWORD,
		'db':configure.DB_DBNAME,
		'charset':configure.DB_CHARSET,
		'cursorclass':pymysql.cursors.DictCursor,
		}

	if conn == None:
		conn = pymysql.connect(**config)

	# init table
	sql = "CREATE TABLE IF NOT EXISTS `qiushibaike`  (\
			`id` int(11) NOT NULL AUTO_INCREMENT,\
			`isread` int(11) NULL DEFAULT 0,\
			`url` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL COMMENT 'url_md5 = md5(url)',\
			`url_md5` binary(64) NOT NULL,\
			`author` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,\
			`fun` int(255) NULL DEFAULT NULL,\
			`comment` int(255) NULL DEFAULT NULL,\
			`content` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,\
			`img_url` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,\
			PRIMARY KEY (`id`) USING BTREE,\
			UNIQUE INDEX `idx_id`(`id`) USING BTREE,\
			UNIQUE INDEX `idx_url_md5`(`url_md5`) USING BTREE\
			) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;\
		"	

	__DMLExecutionMod(sql)

# Add ONE record into the table
def DBupdate(url, md5, author, fun, comment, content, img_urls=None):
	global conn

	if img_urls == None:
		img_urls = 'null'
	else:
		img_urls = "'" + img_urls + "'"

	sql = "INSERT INTO `qiushibaike`\
			(`url`, `url_md5`, `author`, `fun`, `comment`, `content`, `img_url`)\
			VALUES\
			('{0:s}', HEX('{1:s}'), '{2:s}', {3:d}, {4:d}, '{5:s}', \
			{6:s});".format(url, md5, author, fun, comment, content, img_urls).replace('	', '')

	__DMLExecutionMod(sql)

	return True

# Retrieve ONE random record
def DBquery():
	global conn

	sql = "SELECT `id`, `url`, `author`, `fun`, `comment`, `content`, `img_url`\
				FROM `qiushibaike` WHERE isread = 0 \
				ORDER BY `id` DESC LIMIT 1;".replace('	', '')

	res = __DQLExecutionMod(sql)


	sql = "UPDATE `qiushibaike` SET isread = 1 WHERE id = {0:d};".format(res[0]['id'])
	__DMLExecutionMod(sql)

	return res

# 获取总数
def DBTotal():
	global conn;
	sql = "SELECT count(*) as `total` FROM `qiushibaike`;"

	res = __DQLExecutionMod(sql)

	return res[0]['total']

# duplication check
def DuplicationCheck(md5):
	global conn
	sql = "SELECT count(*) AS `num` FROM `qiushibaike` WHERE url_md5 = HEX('{0:s}');".format(md5)

	res = __DQLExecutionMod(sql)

	if res[0]['num']:	
		return True
	else:
		return False

# Drop this table
def DBdrop():
	global conn
	__DMLExecutionMod("DROP TABLE `qiushibaike`;")

	return True

# close
def DBclose():
	global conn
	if conn is not None:
		conn.close()

def DBtest():
	DBconnect()

	assert True == DBupdate('http://www.google.com', 'ed646a3334ca891fd3467db131372140', 'ethan', 12, 13, 'aaaa', None), 'update fail - 1'
	assert True == DBupdate('http://www.google.com', 'ed646a3334ca891fd3467db131372141', 'ethan', 12, 14, 'aaaa', 'http://a;http://b;'), 'update fail - 2'
	assert True == DBupdate('http://www.google.com', 'ed646a3334ca891fd3467db131372142', 'ethan', 12, 15, 'aaaa', None), 'update fail - 3'

	res = DBquery()
	assert 1 == len(res), 'query fail - 11'
	assert 15 == res[0]['comment'], 'query fail - 12'

	res = DBquery()
	assert 1 == len(res), 'query fail - 21'
	assert 14 == res[0]['comment'], 'query fail - 22'

	assert 3 == DBTotal(), 'query fail - 31'

	assert True == DuplicationCheck('ed646a3334ca891fd3467db131372142'), 'duplicate fail - 1'
	assert False == DuplicationCheck('11111111111111111111111111111111'), 'duplicate fail - 2'

	assert True == DBdrop(), 'drop fail'
	DBclose()

# test
if __name__ == '__main__':
	DBtest()