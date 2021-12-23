import leancloud

# 初始化 不背单词
def init_BBDC_project():
	BBDCLC = leancloud.Object.extend("Projects")
	bbdc_lc = BBDCLC()
	bbdc_lc.set("category", "移动端")
	bbdc_lc.set("habitName", "BBDC")
	bbdc_lc.set("isOpen", True)
	bbdc_lc.set("isShow", True)
	bbdc_lc.set("name", "不背单词")
	bbdc_lc.set("password", "123456")
	bbdc_lc.set("path", "bbdc")
	bbdc_lc.save()
# 初始化 Forest
def init_forest_project():
	ForestLC = leancloud.Object.extend("Projects")
	forest_lc = ForestLC()
	forest_lc.set("category", "移动端")
	forest_lc.set("habitName", "forest")
	forest_lc.set("isOpen", True)
	forest_lc.set("isShow", True)
	forest_lc.set("name", "Forest")
	forest_lc.set("password", "123456")
	forest_lc.set("path", "forest")
	forest_lc.save()