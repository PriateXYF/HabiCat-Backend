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

# 初始化 GitHub
def init_github_project():
	GitHubLC = leancloud.Object.extend("Projects")
	github_lc = GitHubLC()
	github_lc.set("category", "网页端")
	github_lc.set("habitName", "github")
	github_lc.set("isOpen", True)
	github_lc.set("isShow", True)
	github_lc.set("name", "GitHub")
	github_lc.set("password", "123456")
	github_lc.set("path", "github")
	github_lc.save()

# 初始化 Reading
def init_reading_project():
	ReadingLC = leancloud.Object.extend("Projects")
	reading_lc = ReadingLC()
	reading_lc.set("category", "小应用")
	reading_lc.set("habitName", "reading")
	reading_lc.set("isOpen", True)
	reading_lc.set("isShow", True)
	reading_lc.set("name", "读书记录")
	reading_lc.set("password", "123456")
	reading_lc.set("path", "reading")
	reading_lc.save()

# 初始化 Course
def init_course_project():
	CourseLC = leancloud.Object.extend("Projects")
	course_lc = CourseLC()
	course_lc.set("category", "小应用")
	course_lc.set("habitName", "course")
	course_lc.set("isOpen", True)
	course_lc.set("isShow", True)
	course_lc.set("name", "网课记录")
	course_lc.set("password", "123456")
	course_lc.set("path", "course")
	course_lc.save()