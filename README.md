# 米游社,原神自动签到。
基于Python3的米游社自动签到项目

# 获取米游社Cookie

1. 打开你的浏览器,进入**无痕/隐身模式**

2. 由于米哈游修改了bbs可以获取的Cookie，导致一次获取的Cookie缺失，所以需要增加步骤

3. 打开`http://bbs.mihoyo.com/ys/`并进行登入操作

4. 在上一步登入完成后新建标签页，打开`http://user.mihoyo.com/`并进行登入操作 (如果你不需要自动获取米游币可以忽略这个步骤，并把`bbs_Global`改为`false`即可)

5. 按下键盘上的`F12`或右键检查,打开开发者工具,点击Console

6. 输入下面内容 回车执行，并在确认无误后点击确定。
    ```javascript
   var cookie=document.cookie;var ask=confirm('Cookie:'+cookie+'\n\nDo you want to copy the cookie to the clipboard?');if(ask==true){copy(cookie);msg=cookie}else{msg='Cancel'}
   ```

# 使用
1. 下载本项目

2. 解压本项目压缩包,在解压目录中**Shift+右键** 打开你的命令提示符cmd或powershell

3. 执行 `pip install -r requirements.txt` 安装模块

4. 打开目录中的**config.py**文件，填写**mihoyo_bbs**，**YsRewardCookie**2个cookie。

5. 运行**index.py**文件。

# 使用腾讯云函数运行

1. 打开并登录[云函数控制台](https://console.cloud.tencent.com/scf/list)。

2. 新建云函数 - 自定义创建，函数类型选`事件函数`，部署方式选`代码部署`，运行环境选 `Python3.6`.

3. 提交方法选`本地上传文件夹`，并在下方的函数代码处上传整个项目文件夹。

4. 执行方法填写 `index.main_handler`.

5. 展开高级配置，将执行超时时间修改为 `300 秒`，其他保持默认。

6. 展开触发器配置，选中自定义创建，触发周期选择`自定义触发周期`，并填写表达式`0 0 7 * * * *`（此处为每天上午 7 时运行一次，可以自行修改）

7. 完成