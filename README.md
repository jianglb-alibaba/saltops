<div align="center">
  <img src="http://git.oschina.net/uploads/images/2017/0222/194334_0f219bc2_8819.png"><br><br>
</div>


#saltops

#目标
SaltOps是一个基于SaltStack和Django开发的运维平台，
平台的主要功能包括：CMDB、包发布管理、工具系统、最终作为包发布和工具系统的接色
与Jenkins、Zabbix等系统进行整合

#系统会具备什么功能

* CMDB：这个也是没办法的事情，资产信息还是要的。。而且Salt的Agent非常适合采集这些基础信息
最后，包发布的过程是需要用到CMDB信息的，所以CMDB是作为附属品存在的
* 包发布：程序包发布的功能，这块主要是用到salt的state.sls，通过编写好
sls文件，然后调用salt进行发布的动作，发布完后应用与主机的信息自然就对接起来了
* 工具平台：既然都接上了Salt，把工具平台做了也是很自然的事情啦～

#为什么使用DjangoAdmin
DjangoAdmin大多作为后台管理员使用的，这里用DjangoAdmin的原因是：没资源。。且每天写的时间也有限，用它的话大多数界面都不用自己做，还是挺省事的

# 文档

> 由于界面变动比较频繁，部分文档截图可能会比较旧

- [SaltOps的定位与目标](doc/wiki/SaltOps的定位与目标.md)
- [架构概览](doc/wiki/架构概览.md)
- [安装前准备](doc/wiki/安装前准备.md)
- [集中部署](doc/wiki/集中部署.md)
- [分离部署](doc/wiki/分离部署.md)
- [功能简介:首页](doc/wiki/首页.md)
- [功能简介:资产管理](doc/wiki/资产管理.md)
- [功能简介:发布管理](doc/wiki/发布管理.md)
- [功能简介:工具管理](doc/wiki/工具管理.md)
- [对外接口](doc/wiki/对外接口.md)
- [使用SaltSSH](doc/wiki/使用SaltSSH.md)
- [系统配置与可用参数列表](doc/wiki/系统配置与可用参数列表.md)
- [常见问题](doc/wiki/常见问题.md)

#常用部署模板

- [JDK](doc/sls/jdk8.sls)
- [ElasticSearch](doc/sls/elasticsearch-master.sls)
- [Golang](doc/sls/golang.sls)