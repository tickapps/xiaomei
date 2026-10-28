"""Render crawlable preset tables from developer JSON; no runtime data fetches.

Usage: python3 tools/build_photo_catalog.py --source-dir /path/to/developer/json
The source bundle stays outside the public website. This script never edits it.
"""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-29"
CSS = """.catalog-scroll{overflow-x:auto;margin:20px 0}table{border-collapse:collapse;width:100%;font-size:.9rem}caption{text-align:left;font-weight:600;padding:8px 0}th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid #dce2eb}th{background:#edf2fa}td:nth-last-child(2){white-space:nowrap}.catalog-group{margin-top:30px}[hidden]{display:none!important}.catalog-links{display:flex;gap:20px;flex-wrap:wrap}"""
SCRIPT = """const input=document.getElementById('topic-search');
const rows=[...document.querySelectorAll('[data-preset]')];
const groups=[...document.querySelectorAll('[data-catalog-group]')];
const count=document.getElementById('result-count');
function normalize(text){return text.normalize('NFKC').toLocaleLowerCase().replace(/(\\d)\\s*[×x*]\\s*(?=\\d)/g,'$1x');}
function filterCatalog(){
 const terms=normalize(input.value.trim()).split(/\\s+/).filter(Boolean);
 let visible=0;
 rows.forEach(row=>{const text=normalize(row.textContent);row.hidden=!terms.every(term=>text.includes(term));if(!row.hidden)visible++;});
 groups.forEach(group=>{group.hidden=![...group.querySelectorAll('[data-preset]')].some(row=>!row.hidden);});
 count.textContent=document.documentElement.lang.startsWith('zh')?`找到 ${visible} 个预设条目`:`Found ${visible} preset entries`;
}
input.addEventListener('input',filterCatalog);filterCatalog();"""


def esc(value):
    return html.escape(str(value), quote=True)


def load(source, name):
    data = json.loads((source / name).read_text())
    assert isinstance(data, list) and data
    for row in data:
        for key in ("size_width", "size_height", "dpi"):
            assert float(row[key]) > 0
    return data


def number(value):
    return format(float(value), "g")


def dimensions(row, prefix="size"):
    return f"{number(row[prefix + '_width'])} × {number(row[prefix + '_height'])}"


def preset_id(scope, row):
    # Based on source semantics, independent of array position. Translation
    # links are page-level; these IDs do not claim cross-locale identity.
    return scope + "-" + hashlib.sha256(json.dumps(row, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]


def table(title, headers, rows, scope):
    rendered = []
    for source_row, cells in rows:
        rendered.append(f'<tr id="{preset_id(scope, source_row)}" data-preset>' + "".join(f"<td>{esc(c)}</td>" for c in cells) + "</tr>")
    return f'<section class="catalog-group" data-catalog-group><h2>{esc(title)}</h2><div class="catalog-scroll" tabindex="0" role="region" aria-label="{esc(title)}"><table><caption>{esc(title)}</caption><thead><tr>' + "".join(f'<th scope="col">{esc(h)}</th>' for h in headers) + "</tr></thead><tbody>\n" + "\n".join(rendered) + "\n</tbody></table></div></section>"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    args = parser.parse_args()
    domestic = load(args.source_dir, "photo_size.json")
    english = load(args.source_dir, "photo_size_en.json")
    chinese = load(args.source_dir, "photo_size_hans.json")
    signature = lambda r: tuple(r[k] for k in ("region_code", "unit", "size_width", "size_height", "dpi"))
    assert len(english) == len(chinese)
    assert all(signature(a) == signature(b) for a, b in zip(english, chinese))
    # Leave the disputed AR translation and channel-dependent JP visa entry
    # out of this public catalogue. No changes to the app's developer data.
    selected = [(en, zh) for en, zh in zip(english, chinese)
                if not (en["region_code"] == "AR" and en["category"] == "Visa in USA")
                and not (en["region_code"] == "JP" and en["category"] == "Visa")]
    # Same named preset can occur in Popular and its normal category. Combine
    # identical parameters, while retaining all category labels and variants.
    unique = {}
    for row in domestic:
        key = tuple((k, v) for k, v in sorted(row.items()) if k != "category")
        if key not in unique:
            unique[key] = (row, [])
        if row["category"] not in unique[key][1]:
            unique[key][1].append(row["category"])
    for lang in ("zh", "en"):
        zh = lang == "zh"
        path = ROOT / f"photo_sizes_{lang}.html"
        page = path.read_text()
        title = "证件照尺寸目录：一寸、考试报名、护照与签证" if zh else "Passport, visa and ID photo size presets"
        description = "查询小美证件照预设的毫米、像素与DPI，按考试名称、国家或证件用途查找；支持自定义尺寸。" if zh else "Find photo size presets by country or document, with explicit mm, inch or pixel dimensions and DPI. Custom sizes are also available."
        page = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", page)
        page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(description)}">', page)
        schema = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": description, "url": f"https://xiaomei.appro7.com/photo_sizes_{lang}.html", "inLanguage": "zh-CN" if zh else "en", "dateModified": DATE, "about": {"@id": "https://xiaomei.appro7.com/#app"}}
        page = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>', page, flags=re.S)
        page = re.sub(r"<h1>.*?</h1>", f"<h1>{esc(title)}</h1>", page)
        intro_start = page.index("<p>", page.index("<h1>"))
        intro_end = page.index('<aside class="notice">', intro_start)
        intro = '<p>按名称、国家或用途查找尺寸。下表根据开发提供的2026年10月28日新版预设整理；不同地区、平台与版本的选项可能不同，请以所用App为准。支持自定义尺寸。</p><p class="meta">目录更新：2026年10月29日。这里列出App预设参数，不代表受理机构对照片的认证。</p>' if zh else '<p>Search by country or document to find a photo size preset. This catalogue uses the developer’s updated preset data supplied on October 28, 2026. Available options can vary by region, platform and app version. Custom dimensions are also supported.</p><p class="meta">Updated October 29, 2026. These are app preset values, rather than certification by a receiving authority.</p>'
        page = page[:intro_start] + intro + "\n" + page[intro_end:]
        start = page.index('<label for="topic-search">')
        end = page.index('<div class="badges">', start)
        body = '<label for="topic-search">' + ('查找国家、证件、考试名称或尺寸' if zh else 'Find a country, document or size') + '</label>\n<input id="topic-search" type="search" placeholder="' + ('例如：一寸、教师、美国、35 × 45' if zh else 'For example: United States, visa, 35 × 45') + '">\n<p id="result-count" role="status" aria-live="polite"></p>\n'
        body += '<p>' + ('所有尺寸按宽 × 高列出。mm为毫米，in为英寸（1英寸=25.4毫米），px为像素。DPI是数据声明的分辨率；电子照片还需核对文件格式、大小及构图。' if zh else 'Dimensions are width × height. mm means millimetres, in means inches (1 inch = 25.4 mm), and px means pixels. DPI is the resolution declared in the preset data. Digital submissions also have file-format, file-size and framing requirements.') + '</p>\n'
        if zh:
            body += '<p class="catalog-links"><a href="#domestic-catalog">国内常用与考试</a><a href="#international-catalog">国际证件预设</a></p><p>国内常用与考试表使用国内版数据；国际证件表使用国际版简体中文数据。两者的用途与可用选项有差异。</p>\n<div id="domestic-catalog"></div>'
            rows = [(r, [r['name'], '、'.join(categories), dimensions(r) + ' mm', dimensions(r, 'pixel') + ' px', number(r['dpi'])]) for r, categories in unique.values()]
            body += table("国内常用与考试预设", ["预设名称", "分类", "毫米尺寸（宽 × 高）", "像素尺寸（宽 × 高）", "DPI"], rows, "domestic")
        body += '<div id="international-catalog"></div>'
        rows = []
        for en, ch in selected:
            r = ch if zh else en
            rows.append((r, [r['country'] + ' (' + r['region_code'] + ')', r['category'], dimensions(r) + ' ' + r['unit'], number(r['dpi'])]))
        body += table("国际证件预设" if zh else "International document presets", ["国家或地区", "用途", "尺寸（宽 × 高）", "DPI"] if zh else ["Country or region", "Document", "Size (width × height)", "DPI"], rows, "international")
        body += '<p>' + ('需要其他尺寸时，可在App中使用自定义尺寸。提交前仍请核对当前受理要求。' if zh else 'Use custom dimensions in the app when you need another size, and check the current requirements before submitting.') + '</p>'
        body += '<h2>' + ('下一步怎么做' if zh else 'Prepare and print your photo') + '</h2><p><a href="prepare_photo_' + lang + '.html">' + ('照片制作前的检查清单' if zh else 'Photo preparation checklist') + '</a> · <a href="print_photos_' + lang + '.html">' + ('多联排版与打印' if zh else 'Multi-copy layout and printing') + '</a></p>\n<script>' + SCRIPT + '</script>\n'
        page = page[:start] + body + page[end:]
        # Idempotent CSS marker.
        page = re.sub(r'/\* catalog \*/.*?/\* end catalog \*/', '', page, flags=re.S)
        page = page.replace('</style>', '/* catalog */' + CSS + '/* end catalog */</style>')
        path.write_text(page)
        print(path.name, "preset rows", len(rows) + (len(unique) if zh else 0), "bytes", len(page.encode()))
    sitemap = ROOT / "sitemap.xml"
    text = sitemap.read_text()
    text = re.sub(r'(photo_sizes_(?:zh|en)\.html</loc><lastmod>)[^<]+', r'\g<1>' + DATE, text)
    sitemap.write_text(text)


if __name__ == "__main__":
    main()
