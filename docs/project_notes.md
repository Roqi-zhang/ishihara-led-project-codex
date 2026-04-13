\# Ishihara LED System — Project Notes



\---



\## 阶段一：基本环境构建



\### Supabase

Project URL:

https://brpfhccvaptsksignnhh.supabase.co



Anon/Public Key:

yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJycGZoY2N2YXB0c2tzaWdubmhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU4MzM3MTYsImV4cCI6MjA5MTQwOTcxNn0.UtxZH0T0keMNVVYJ21fZHab2GQK2KfKourxJmWBoNzg



Database Password:

（已设置）



Service\_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJycGZoY2N2YXB0c2tzaWdubmhoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTgzMzcxNiwiZXhwIjoyMDkxNDA5NzE2fQ.I-d\_um8F17GAdQCPOpCmA7Jhhg4Tj9YXQ2Bc49MakgA

\---



\### Render（后端）

Backend URL:

（部署后填写）



\---



\### Vercel（前端）

Frontend URL:

（部署后填写）



\---



\### Stripe（支付）

Publishable Key:

sb\_publishable\_pbuZJOfwAAlOh0k25hgv-g\_XUg8AkU9



Secret Key:

sb\_secret\_dIg9N-ERJ1RhBQA0WU59hw\_Satal\_7q



当前模式：Sandbox（测试环境）



\---



\## 阶段二：数据结构设计



\---



\### 核心对象



1\. 用户提交记录 submission

2\. 展示队列 display queue

3\. 打印行为 print

4\. 留言 message



\---



\### 数据表方案



当前采用 2 张表：



1\. submissions（主数据表）

2\. display\_queue（LED展示队列）



\---



\## submissions 表（核心数据）



\### 表作用



每一位用户上传图片并生成图谱后，对应一条记录。



用于保存完整用户行为数据，包括：



\- 上传

\- 图像生成

\- LED展示

\- 留言

\- 打印

\- 支付状态



\---



\### 字段设计



\#### 基础信息



\- id

&#x20; 类型：uuid

&#x20; 说明：主键



\- upload\_order

&#x20; 类型：integer

&#x20; 说明：第几位上传者（全局递增）



\- uploaded\_at

&#x20; 类型：timestamp

&#x20; 说明：上传时间（精确到秒）



\---



\#### 图片数据



\- original\_image\_url

&#x20; 类型：text

&#x20; 说明：原图地址（Supabase Storage）



\- generated\_image\_url

&#x20; 类型：text

&#x20; 说明：生成图谱地址



\- symbol

&#x20; 类型：text

&#x20; 说明：图谱数字（例如 75）



\---



\#### 展示状态



\- display\_status

&#x20; 类型：text

&#x20; 说明：pending / showing / shown



\---



\#### 留言（在展示之后）



\- message

&#x20; 类型：text

&#x20; 说明：用户留言内容



\---



\#### 打印与支付



\- printed

&#x20; 类型：boolean

&#x20; 说明：是否打印



\- print\_count

&#x20; 类型：integer

&#x20; 说明：打印数量（默认 0）



\- print\_code

&#x20; 类型：text

&#x20; 说明：打印编号（001, 002…）



\- payment\_status

&#x20; 类型：text

&#x20; 说明：unpaid / paid



\---



\#### 系统字段



\- created\_at

&#x20; 类型：timestamp

&#x20; 说明：记录创建时间



\---



\## display\_queue 表（LED展示）



\### 表作用



用于控制 LED 屏幕的播放顺序。



每次点击“传输到LED”时生成一条记录。



\---



\### 字段设计



\- id

&#x20; 类型：uuid



\- submission\_id

&#x20; 类型：uuid

&#x20; 说明：关联 submissions



\- generated\_image\_url

&#x20; 类型：text

&#x20; 说明：展示图地址



\- queue\_order

&#x20; 类型：integer

&#x20; 说明：顺序编号（递增）



\- status

&#x20; 类型：text

&#x20; 说明：pending / showing / shown



\- created\_at

&#x20; 类型：timestamp

&#x20; 说明：进入队列时间



\- shown\_at

&#x20; 类型：timestamp

&#x20; 说明：展示完成时间



\---



\## Supabase Storage 结构



\### Bucket



1\. original-images

用于存储用户上传原图



2\. generated-images

用于存储生成的色盲图谱



\---



\### 文件命名规则



使用 submission\_id 作为唯一标识：



original-images/{submission\_id}.jpg

generated-images/{submission\_id}.png



\---



\## 展示队列规则（核心逻辑）



1\. 用户点击“传输到LED”后，创建一条 display\_queue 记录



2\. 展示页读取规则：



\- status = 'pending'

\- 按 created\_at 升序

\- 若时间相同 → 按 queue\_order 升序

\- 取第一条



3\. 展示流程：



\- 开始展示 → status = showing

\- 展示结束 → status = shown



4\. 系统循环执行，实现自动轮播



\---



\## 顺序判定规则（关键）



顺序 = created\_at + queue\_order



说明：



\- created\_at 保证时间顺序

\- queue\_order 作为兜底，防止并发冲突



\---



\## 打印编号规则



打印编号独立递增：



001

002

003

...



规则：



\- 只有点击“打印”才生成编号

\- 按打印顺序累加



\---



\## upload\_order 与 print\_code 区别



upload\_order = 第几位上传者

print\_code = 第几位打印者



两者完全独立



\---



\## 留言规则（已更新）



留言发生在“上传到LED之后”，打印之前



流程：



1\. 上传图片

2\. 生成图谱

3\. 点击“传输到LED”

4\. 创建 submission + queue

5\. 进入留言界面

6\. 用户填写留言

7\. 写入 submissions.message

8\. 进入打印流程



说明：



\- 每个 submission 对应一条留言

\- 留言是作品表达的一部分



\---



\## 支付规则



payment\_status：



\- unpaid（默认）

\- paid（支付完成）



当前使用 Stripe Sandbox



\---



\## 作品交互逻辑（艺术层）



系统交互顺序：



生成 → 展示 → 表达 → 留存 → 物化



对应关系：



\- LED 展示 = 被看见

\- 留言 = 表达

\- 打印 = 带走



\---



\## 阶段二完成确认



\- submissions 表结构已确定

\- display\_queue 表结构已确定

\- storage 结构已确定

\- 队列规则已确定

\- 打印编号规则已确定

\- 留言流程已确定



\## 当前正式接口（阶段四前冻结）



POST /upload\_generated

GET /queue

GET /next\_image

POST /mark\_shown



\### /upload\_generated

请求体：

{

&#x20; imageBase64: string,

&#x20; symbol: string,

&#x20; sourceName: string,

&#x20; originalImageBase64?: string

}



返回：

{

&#x20; ok: boolean,

&#x20; submission: object,

&#x20; item: {

&#x20;   id: string,

&#x20;   submission\_id: string,

&#x20;   image\_url: string,

&#x20;   status: string

&#x20; },

&#x20; queue\_length: number

}

