水印相机 公网网页版

这个目录是纯静态网页，不需要服务器程序。
把本目录里的文件上传到任意公网静态网站空间后，任何手机都可以通过网址访问。

必须满足：
1. 上传到公网网站，例如 GitHub Pages、Cloudflare Pages、Vercel、Netlify、宝塔/Nginx 网站目录、阿里云 OSS、腾讯云 COS。
2. 推荐使用 HTTPS。HTTPS 下手机可以添加到主屏幕，并支持离线缓存。
3. 手机打开网址后，照片处理在手机浏览器本地完成，不会上传照片。

最简单部署方式：
1. 把 index.html、manifest.json、sw.js、icon-192.png、icon-512.png 全部上传到网站根目录。
2. 打开网站域名，例如 https://你的域名/index.html。
3. 把这个网址发给其他手机。

如果用宝塔/Nginx：
1. 新建一个静态站点。
2. 上传本目录全部文件到站点根目录。
3. 绑定域名并开启 HTTPS。

如果用 GitHub Pages：
1. 新建仓库。
2. 上传本目录全部文件。
3. 在仓库 Settings > Pages 开启 GitHub Pages。
4. 等待生成 https://账号.github.io/仓库名/ 网址。
