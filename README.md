# ROS profiling

## python 将 ROS 的 LOG 转化为JSON

直接运行就能转换

```Shell
python ./pyscript/pygatt.py
```

默认的输入文件夹是 ```'data/inputlog/'```，输出文件是 ```'data/outputdata/outputlog_test.json'```。

## 可视化JSON文件

进入 profiling 文件夹

双击 custom-profile.html 打开浏览器，在文件选择界面选择生成的JSON文件，即可可视化。