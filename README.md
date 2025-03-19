# 版本支持情况

经过测试，此项目的（master分支）运行要求是 `>= Python 3.8` ，推荐使用 `Python 3.9`。

> **💡提示** 由于 Flask 中使用的 Werkzeug 模块更新，Flask 官方并未进行更新，所以可能会出现 ImportError 。
> 此类情况的出现可以通过正确安装 `requirements.txt` 中的模块（以及其对应版本）解决。

# 项目结构

## 应用结构

```应用结构
Pear Admin Flask
├─applications  # 应用
│  ├─extensions  # 注册插件
│  ├─models  # 数据模型
│  ├─static  # 静态资源文件
│  ├─templates  # 静态模板文件
│  └─views  # 视图部分
│     ├─admin  # 后台管理视图模块
│     └─index  # 前台视图模块
├─docs  # 文档说明
├─migrations  # 迁移文件记录
├─requirement  # 依赖文件
└─.env # 项目的配置文件
```

## 资源结构

```资源结构
Pear Admin Flask
├─static    # 项目设定的 Flask 资源文件夹
│  ├─admin    # pear admin flask 的后端资源文件（与 pear admin layui 同步）
│  ├─index    # pear admin flask 的前端资源文件
│  └─upload     # 用户上传保存目录
└─templates # 项目设定的 Flask 模板文件夹
  ├─admin   # pear admin flask 的后端管理页面模板
  │  ├─admin_log    # 日志页面
  │  ├─common       # 基本模板页面（头部模板与页脚模板）
  │  ├─console      # 系统监控页面模板
  │  ├─dept         # 部门管理页面模板
  │  ├─dict         # 数据自动页面模板
  │  ├─mail         # 邮件管理页面模板
  │  ├─photo        # 图片上传页面模板
  │  ├─power        # 权限（菜单）管理页面模板
  │  ├─role         # 角色管理页面模板
  │  ├─task         # 任务设置页面模板
  │  └─user         # 用户管理页面模板
  ├─errors  # 错误页面模板
  └─index   # 主页模板
```

# 项目安装

# 使用 pip 安装
pip install -r requirements.txt
```

## 直接安装项目

```bash
# 使用 pip 安装
pip install -r requirements.txt
# 同时你可以选择以模块的方式调用 pip
python -m pip install -r requirements.txt
```

# 运行项目

+ 一般情况运行项目

```bash
# 初始化数据库
flask db init
flask db migrate
flask db upgrade
flask admin init

# 运行项目
flask --app app.py run -h 0.0.0.0 -p 8000 --debug

# 或者直接调用 app.py
python app.py
```



# 其他说明

## 项目初始用户以及其密码

默认用户为 `admin` ，密码默认为 `123456` 。

## 其他开发说明链接

+ Pear Admin Flask [目录结构](list.md) 章节     
+ Pear Admin Flask [开发函数](function.md) 章节 
+ Pear Admin Flask [插件开发](plugin.md) 章节   
                                         


