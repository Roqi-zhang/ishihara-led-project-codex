# Ishihara LED 公网部署包

这份包已经按“尽量少改动”的方式准备好，**最省事的上线方案是整包直接部署到 Render**。  
因为 `app.py` 会同时提供：

- `https://你的域名/` → 用户上传与生成页
- `https://你的域名/display` → LED 展示页
- `https://你的域名/health` → 健康检查
- `https://你的域名/upload_generated` → 接收前端生成好的 PNG
- `https://你的域名/next_image` → 展示页轮播读取接口
- `https://你的域名/mark_shown` → 展示完成标记接口

## 你最应该用的方式：只部署到 Render
这样 **前端和后端天然同域**，不需要手动改地址，也不用额外处理前端调用哪个后端的问题。

### Render 部署步骤
1. 注册 / 登录 Render。
2. 把整个文件夹上传到 GitHub 仓库。
3. 在 Render 里选择 **New + -> Web Service**。
4. 连接你的 GitHub 仓库。
5. Render 会自动识别 `render.yaml`。
6. 点击创建，等待部署完成。
7. 部署成功后，访问：
   - `/`：观众上传页
   - `/display`：LED 展示页

## 如果你一定要把前端单独放 Vercel
这也可以，但这时前端不再和后端同域。  
你不需要改代码，只需要在页面顶部的“后端地址”输入框里填入你的 Render 域名一次，例如：

`https://你的后端.onrender.com`

页面会把这个地址保存在浏览器本地，下次自动使用。

## 当前文件
- `app.py`
- `index.html`
- `display.html`
- `requirements.txt`
- `render.yaml`
- `data/queue.json`

## 本地运行（可选）
虽然你现在主要要公网部署，但本地测试也可以：
```bash
pip install -r requirements.txt
python app.py
```
然后打开：
- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/display`
