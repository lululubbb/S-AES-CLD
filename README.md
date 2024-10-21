## 1. 系统简介

S-AES是一种简化版的AES(高级加密标准)加密算法。它主要对16位的二进制数据进行加密处理,而标准的AES算法则处理128位(16字节)的数据。

S-AES的设计目的是为了在教学和学习中简化AES算法的复杂性,同时保持其核心的加密原理和结构。

我们提供了16bit加解密、ASCII字符串加解密、文件加解密以及中间相遇攻击等功能。

系统环境配置详情见用户指南.md

## 2.S-AES项目结构
<pre>
<code class="tree">
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

## 3.开发者信息

• 开发团队：卟咯吩

• 开发人员：陈露、罗丹

• 联系方式：1055331355@qq.com
