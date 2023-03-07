# wolai_export
批量导出wolai笔记

运行脚本前需要将自己的 wolai `token` 填入脚本中

- 支持markdown和pdf格式导出
- pdf暂时不支持子页面导出
- markdown格式支持子页面导出
  - wolai导出的markdown中的双向关联链接是关联到线上的地址，脚本会将双向链接替换为obsidian支持的双向链接格式，如需关闭注释掉 `replace_wolai_url_to_inner_link('markdown')`即可
