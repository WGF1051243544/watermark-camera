水印相机 公网网页版

这个目录是纯静态网页，不需要服务器程序。上传到 GitHub Pages、Cloudflare Pages、Vercel、Netlify、宝塔/Nginx 静态站点、阿里云 OSS、腾讯云 COS 等公网空间后，其他手机可通过链接直接使用。

必须一起上传这些文件：
- index.html
- manifest.json
- sw.js
- camera-icon-template.png
- icon-192.png
- icon-512.png
- .nojekyll

说明：
1. 推荐使用 HTTPS。HTTPS 下手机可以添加到主屏幕，并支持离线缓存。
2. 照片处理在浏览器本地完成，不会上传照片。
3. 自动识别地址会优先读取照片 EXIF GPS；如果没有 GPS，会尝试在浏览器本地 OCR 识别图片中文字，识别不到就不修改地点。
4. 右下角“水印相机”图标使用 camera-icon-template.png，必须和 index.html 放在同一目录。
5. 如果手机打开后仍显示旧图标，请刷新页面，或清除浏览器缓存后重新打开。

GitHub Pages 当前发布地址：
https://wgf1051243544.github.io/watermark-camera/
