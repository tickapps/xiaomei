# 小美证件照官网

官网：https://xiaomei.appro7.com 。生产分支为 `gh-pages`，GitHub Pages负责部署；`main`不是网站发布分支。

## 当前实现

- 中文首页：`index.html?lang=zh`；英文首页：`index_en.html`。根地址及没有 `lang=zh` 的中文入口继续默认跳英文，保留商店入口行为。
- “支持哪些证件照类型 / Supported photo types”直接位于两首页的 `#supported-photos` 段落，现有App JSON-LD与可见类型介绍一致。
- 中文按国内用途整理；英文按开发提供的 `photo_size_en.json` 原有 `category` 和 `country` 名称整理。英文不能通过翻译中文考试名称补齐；两份数据有真实差异。
- 英文已覆盖2026-10-28开发版数据的83个不同类型名称。这里只统计源名称，不是83套唯一官方标准，也不是受理保证。
- 官网只介绍支持的类型和用途，不提供具体参数表、独立尺寸目录、原始JSON、App代码或目录生成脚本。App内自定义尺寸能力仍可正常介绍。
- 制作与打印指南、隐私政策、下载链接和原有图片保留。照片本地处理；广告、统计与诊断数据另按政策说明，不宣传全App零采集。

源数据在网站仓库之外维护。官网发布不代表App的新版尺寸或商店版本已上线，不从网站部署推断商店状态。

## 维护与预览

静态HTML、CSS与少量原生JavaScript，无包管理器或前端构建依赖。本地运行 `python3 -m http.server 8765`，访问 `http://127.0.0.1:8765/index.html?lang=zh#supported-photos` 或 `http://127.0.0.1:8765/index_en.html#supported-photos`。

首页为产品入口，`prepare_photo_*`与`print_photos_*`为指南，`privacypolicy*`为政策，`en/`与根目录图片为既有媒体。`robots.txt`与`sitemap.xml`服务抓取。`index_old.html`、`index_en_old.html`是本轮之前已有的旧文件，未删除、未作为现役入口。

维护约束见 [AGENTS.md](AGENTS.md)，验证边界见 [VALIDATION.md](VALIDATION.md)。这三份维护文档由 `_config.yml` 排除在网站发布内容之外，仍在Git仓库中供协作阅读；此排除不删除Git历史，也不把仓库变为私有。

## 当前状态

类型内容通过 [PR #8](https://github.com/tickapps/xiaomei/pull/8) 合并；2026-10-29已核对部署成功及线上首页与提交内容一致。详细复核与未验证项见VALIDATION。当前没有新的真实AI回答采样，不能声称AI提及、引用或下载已提升。
