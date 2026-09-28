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
3. 水印模板支持三个版本：
   - 左下角经典模板：时间、日期、天气、地点在左下角，右下角显示“水印相机”。
   - 居中简洁模板：时间居中偏下，日期/星期/地点在下一行居中，右下角显示相机图标和“水印相机”。
   - 对角信息模板：左上角显示时间与日期星期，右下角显示姓名和地点；不显示品牌字，也不绘制天气。
4. 姓名、时间、地点均可手动填写；对角信息模板会使用姓名字段。
5. 自动识别地址会优先读取照片 EXIF GPS；如果没有 GPS，会尝试在浏览器本地 OCR 识别图片中文字，识别不到就不修改地点。
6. 右下角“水印相机”图标使用 camera-icon-template.png，必须和 index.html 放在同一目录。
7. 如果手机打开后仍显示旧图标，请刷新页面，或清除浏览器缓存后重新打开。

GitHub Pages 当前发布地址：
https://wgf1051243544.github.io/watermark-camera/
