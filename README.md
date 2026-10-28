# 小美证件照官网

生产网站：https://xiaomei.appro7.com 。GitHub Pages从gh-pages部署；合并到该分支即更新官网。

## 2026-10-29 尺寸目录

中英文尺寸目录已接入开发2026-10-28提供的新版JSON：

- 中文页：151个国内预设（162条源记录按名称与全部参数合并跨分类重复入口，分类全部保留）及360个国际预设。
- 英文页：360个国际预设。中文国内与国际表分开，保留地区／版本差异，不将国内考试目录伪装成国际版功能。
- 显示源数据的宽×高、单位与DPI，国内另列像素。考试像素采用开发最新版，不再以旧值为准；这些是App预设数据，不是本轮对各报名标准的认证。
- 国际源362条，本次不刊登AR/Visa in USA译名争议条目和JP/Visa渠道未区分条目；不追改App原件。国内日本签证两个尺寸采用新版名称。
- 所有条目为静态HTML；脚本只负责搜索过滤，无JS仍能读取。查询支持空格分词，每个词均需匹配；无结果可清空恢复。没有为每个搜索词生成大量独立页面。
- 数据提供日期与目录更新日期可见；新版参数不表述为已经随App版本上线或官方受理保证。源数据的DPI只是声明值，本轮没有验证App实际导出。
- 用户确认photo_size_hant.json仍在使用。此次开发包缺该文件，不覆盖、不删除、不以tw/hk自动替代。官网当前仅简中／英文，生成器使用国内、hans及en三个文件；hant不在网站生成输入中。

重建：`python3 tools/build_photo_catalog.py --source-dir /path/to/developer/json`。输入文件留在发布目录之外。生成器不修改输入；条目锚点由源语义内容生成，不以数组下标生成身份，也不宣称跨语言逐条永久对应。

源文件SHA256见下方记录。用户提供的其他语言文件不用于生成额外语言网页。

## 入口与已发布基础

- 根网址和没有lang=zh的index.html继续跳英文；index.html?lang=zh显示中文；英文直接地址index_en.html保留。此次不改任何入口、重定向或商店后台网址。
- 2026-10-27后台核验：Google Play网站是index_en.html；iOS营销／支持网址除zh-Hans的?lang=zh外均为根网址。不会将Google Play网址错误记录为根网址。
- 既有导航、制作指南、打印指南、隐私页、下载按钮、canonical、hreflang、robots与App实体标识保持已有实现。此次仅尺寸页及其sitemap更新时间变化。
- 照片全部本地处理；相机拍照／相册选图。Unity／ironSource广告，Firebase Analytics统计、Crashlytics诊断。英文政策名称按美国iOS商店名；平台名称与发布者差异保留。广告／统计等SDK数据不能被“照片不上传”推导为全App零采集。
- 当前产品与SDK事实沿用2026-10-27用户确认；本轮不修改政策、商店内容或App代码。

## 验证边界

具体结果见VALIDATION.md。已授权发布后需核对线上HTML与提交内容一致、响应状态与原有语言入口。

之前本地浏览器预览权限被拒绝，本轮不绕过；没有完成手机／桌面视觉验收。当前未做真实AI回答采样，不宣称收录、AI引用、排名或下载增加。网页搜索不是AI回答采样；无引用不证明训练记忆，有引用不代表排名权重或下载贡献。

本地预览：`python3 -m http.server 8765`，打开http://localhost:8765/photo_sizes_zh.html。

## 生成输入校验值

- `photo_size.json`: `8d30e4caeb1e1a90e95f4cd89b0bc3a7d02d0ab4c70b2e784cf56bd0773163c6`
- `photo_size_hans.json`: `3c3426dac6174ac4cf18202cf156bee48275cccef59936cce3d08b10381c01e9`
- `photo_size_en.json`: `d77a4a56c934abc259f668ac210665ddb3f9bb60f928e2f36bec9a80a5490360`
