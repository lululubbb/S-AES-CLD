<pre>
<code class="tree">
# S-AES项目结构

│  README.md
│  requirements.txt
│  开发手册.md
│  测试文档.md
│  用户指南.md
│
├─assets                                        - 用户指南中的图片
│
├─S-AES-end                                     - S-AES后端文件
│  │  function.py                               - 实现S-AES算法的函数，包括加密、解密、密钥扩展、CBC工作模式等
│  │  main.py                                   - S-AES后端的主程序，负责处理HTTP请求和响应，连接前端和后端
│  │
│  ├─.idea
│  │
│  └─tmp                                        -  用于存放文件夹解密中涉及的临时文件
│
└─S-AES-front                                   - S-AES前端文件
    │  index.html                               - 前端页面的主文件，用于展示用户界面
    │
    ├─image	                                    - 存放前端页面中使用的图片资源
    │
    ├─scripts	                                - 存放JavaScript脚本文件
    │      script.js
    │
    └─styles	                                - 前端页面的CSS样式定义
            style.css
</code>
</pre>
