---
title: Hexo + GitHub 搭建博客
date: 2019-04-29 18:15:47
tags: hexo
categories:
- hexo
---

### Install Nodejs

```shell
brew install node
```

### Install Hexo

```shell
npm install -g hexo-cli
```

### Init blog

1) init

```shell
hexo init blog
```

2) demo test

```shell

hexo n "hello world"

hexo g

hexo s
```

###  github
1）github create blog project

2）`_config.yml` 配置

```
deploy:
  type: git
  repo: https://github.com/haojianggod/blog.git
  branch: master


```
这样我们执行hexo deploy 时候就知道该把blog 部署到哪里


### install hexo-deployer-git plugin

```shell

npm install hexo-deployer-git --save
```

### deploy blog

```shell

hexo clean

hexo d -g

```

这样就将blog部署到github上了，直接去haojiang.github.io/blog 查看


INDEX: https://zhuanlan.zhihu.com/p/26625249
