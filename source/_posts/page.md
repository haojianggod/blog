---
title: hexo命令
date: 2019-04-30 18:15:47
tags:
---

### init
```
$ hexo init blogs
```

### new

```
$ hexo new [layout] <title>
```
- 如果没有layout，则用默认的 default_layout(配置在_config.yml中)
- 如果title 中有空格，就需要用引号包起来

| Option |  Description |
|--------|--------------|
| -p, --path | Post path. Customize the path of the post.|
| -r, --replace | Replace the current post if existed.|
| -s, --slug  | Post slug. Customize the URL of the post.|

```
$ hexo new page --path about/me "About me"
```

will create source/about/me.md file with the title “About me” set in the front matter.


### generate

```
$ hexo generate
```

| Option |  Description |
|--------|--------------|
| -d, --deploy | Deploy after generation finishes|
| -w, --watch | Watch file changes|
| -b, --bail | Raise an error if any unhandled exception is thrown during generation|
| -f, --force | Force regenerate|


### publish

```
$ hexo publish [layout] <filename>

```
Publishes a draft.

### server

```
$ hexo server
```
Starts a local server. By default, this is at http://localhost:4000/.

| Option |  Description |
|--------|--------------|
| -p, --port | Override default port|
| -s, --static | Only serve static files|
| -l, --log| Enable logger. Override logger format.|


### deploy

```
$ hexo deploy
```

Deploys your website.

| Option |  Description |
|--------|--------------|
| -g, --generate | Generate before deployment|


### render

```
$ hexo render <file1> [file2] ...
```

Renders files.
|Option |  Description |
|--------|--------------|
| -o, --output | Output destination|





## 更换主题

```
主题： https://hexo.io/themes/
git clone https://github.com/iissnan/hexo-theme-next themes/next

git clone https://github.com/dongyuanxin/theme-ad themes/ad
```
- 引用：https://hexo.io/docs/commands
