#!  /usr/bin/python
# coding=utf-8

import os
import traceback
from uuid import uuid1

import logging
import requests
import yaml
from celery import task
from post_office import mail

from cmdb.models import Host, HostIP
from deploy_manager.models import *
from saltjob.salt_https_api import salt_api_token
from saltjob.salt_token_id import token_id
from saltops.settings import SALT_REST_URL, PACKAGE_PATH, SALT_CONN_TYPE, SALT_HTTP_URL, DEFAULT_LOGGER
from tools_manager.models import ToolsExecDetailHistory, ToolsExecJob

logger = logging.getLogger(DEFAULT_LOGGER)


def generateDynamicScript(script_content, script_type, param="", extra_param="", extend_dict=None):
    """
    动态生成脚本文件
    :return: 脚本文件的名称，脚本的完整路径
    """
    logger.info("动态生成脚本文件")

    script_content = script_content.replace('\r', '')

    logger.info("填写动态变量")
    if param != "":
        yaml_params = yaml.load(param)[0]
        for key in yaml_params:
            script_content = script_content.replace('${%s}' % key, yaml_params[key])

    if extra_param != "":
        yaml_params = yaml.load(extra_param)[0]
        for key in yaml_params:
            script_content = script_content.replace('${%s}' % key, yaml_params[key])

    if extend_dict is not None:
        for k in extend_dict:
            script_content = script_content.replace('${%s}' % k, extend_dict[k])

    uid = uuid1().__str__()
    scriptPath = PACKAGE_PATH + uid + '.' + script_type
    output = open(scriptPath, 'wb')
    output.write(bytes(script_content, encoding='utf8'))
    output.close()
    logger.info("写入文件结束，文件为%s", scriptPath)
    return uid, scriptPath


def prepareScript(script_path):
    """
    判断执行模式，执行对应的操作
    :return:
    """
    if SALT_CONN_TYPE == 'http':
        logger.info("当前执行模式为分离模式，发送脚本到Master节点")
        url = SALT_HTTP_URL + '/upload'
        files = {'file': open(script_path, 'rb')}
        requests.post(url, files=files)
        logger.info("发送远程文件结束")


def runSaltCommand(host, script_type, filename):
    """
    执行远程命令
    :param host:
    :param script_type:
    :param filename:
    :return:
    """
    client = 'local'
    if host.enable_ssh is True:
        client = 'ssh'

    if script_type == 'sls':
        result = salt_api_token({'fun': 'state.sls', 'tgt': host,
                                 'arg': filename},
                                SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(client=client)['return'][0]
        logger.info("执行结果为:%s", result)
    else:
        result = salt_api_token({'fun': 'cmd.script', 'tgt': host,
                                 'arg': 'salt://%s.%s' % (filename, script_type)},
                                SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(client=client)['return'][0]
        logger.info("执行结果为:%s", result)
    return result


def getHostViaResult(result, host, hostname):
    """
    因为Salt-SSH和Salt-Minion获取结果的方式不太一样，所以要区别对待
    :param result:
    :param host:
    :param hostname:
    :return:
    """
    if host.enable_ssh is False:
        dataResult = result[hostname]
        targetHost = Host.objects.get(host_name=hostname)
    else:
        dataResult = result[hostname]['return']
        targetHost = Host.objects.get(host=hostname)
    return targetHost, dataResult


@task(name='execTools')
def execTools(obj, hostList, ymlParam):
    hostSet = Host.objects.filter(pk__in=hostList).all()
    toolExecJob = ToolsExecJob(
        param=ymlParam,
        tools=obj
    )
    toolExecJob.save()
    toolExecJob.hosts.add(*hostSet)
    toolExecJob.save()

    script_type = 'sls'
    if obj.tool_run_type == 1:
        script_type = "sh"
    if obj.tool_run_type == 2:
        script_type = "ps"
    if obj.tool_run_type == 3:
        script_type = "py"
    script_name, script_path = generateDynamicScript(obj.tool_script, script_type, ymlParam, "", None)

    prepareScript(script_path)

    logger.info("开始执行命令")
    logger.info("获取目标主机信息,目标部署主机共%s台", hostSet.count())

    for target in hostSet:
        try:
            result = runSaltCommand(target, script_type, script_name)

            for master in result:
                targetHost, dataResult = getHostViaResult(result, target, master)

                if obj.tool_run_type == 0:
                    for cmd in dataResult:
                        rs_msg = dataResult[cmd]['comment']
                        for key in dataResult[cmd]['data']:
                            rs_msg = rs_msg + '\n' + key + ':' + dataResult[cmd]['data'][key]
                        execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                            host=targetHost,
                                                            exec_result=rs_msg,
                                                            err_msg='')
                        execDetail.save()
                else:
                    execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                        host=targetHost,
                                                        exec_result=dataResult['stdout'],
                                                        err_msg=dataResult['stderr'])
                    execDetail.save()
        except Exception as e:
            execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                host=target,
                                                exec_result='执行失败',
                                                err_msg=dataResult[0])
            execDetail.save()

    return toolExecJob


@task(name='deployTask')
def deployTask(deployJob, uninstall=False, uninstall_host=[]):
    """
    部署业务
    :param deployJob:
    :return:
    """
    try:
        project = deployJob.project_version.project
        defaultVersion = project.projectversion_set.get(is_default=True)
        logger.info("使用的默认版本为%s", defaultVersion)

        isSubScript = defaultVersion.sub_job_script_type == 100

        script_type = 'sls'
        if isSubScript is True:
            if project.job_script_type == 1:
                script_type = 'sh'
        else:
            if defaultVersion.sub_job_script_type == 1:
                script_type = 'sh'

        if isSubScript is True:
            if uninstall is False:
                playbookContent = project.playbook
            else:
                playbookContent = project.anti_install_playbook
        else:
            if uninstall is False:
                playbookContent = defaultVersion.subplaybook
            else:
                playbookContent = defaultVersion.anti_install_playbook

        extent_dict = (
            {'version': defaultVersion.name}
        )
        script_name, script_path = generateDynamicScript(playbookContent, script_type, project.extra_param,
                                                         defaultVersion.extra_param, extent_dict)
        prepareScript(script_path)

        if uninstall is False and defaultVersion.files is not None:
            try:
                prepareScript(defaultVersion.files.path)
            except Exception as e:
                logger.info("没有文件，不执行发送操作")

        jobList = []

        if uninstall is False:
            hosts = project.host.all()
        else:
            hosts = uninstall_host

        logger.info("获取目标主机信息,目标部署主机共%s台", len(hosts))
        hasErr = False
        for target in hosts:
            logger.info("执行脚本，目标主机为:%s", target)

            result = runSaltCommand(target, script_type, script_name)

            # SLS模式
            if script_type == 'sls':
                for master in result:
                    if isinstance(result[master], dict):
                        targetHost, dataResult = getHostViaResult(result, target, master)
                        for cmd in dataResult:

                            if not dataResult[cmd]['result']:
                                hasErr = True

                            msg = ""
                            if "stdout" in dataResult[cmd]['changes']:
                                msg = dataResult[cmd]['changes']["stdout"]
                            stderr = ""
                            if "stderr" in dataResult[cmd]['changes']:
                                stderr = dataResult[cmd]['changes']["stderr"]

                            jobCmd = ""
                            if 'name' in dataResult[cmd]:
                                jobCmd = dataResult[cmd]['name']

                            duration = 0
                            if 'duration' in dataResult[cmd]:
                                duration = dataResult[cmd]['duration']

                            # startTime = None
                            # if 'start_time' in dataResult[cmd]:
                            #     startTime = dataResult[cmd]['start_time']
                            deployJobDetail = DeployJobDetail(
                                host=targetHost,
                                deploy_message=msg,
                                job=deployJob,
                                stderr=stderr,
                                job_cmd=jobCmd,
                                comment=dataResult[cmd]['comment'],
                                is_success=dataResult[cmd]['result'],
                                # start_time=startTime,
                                duration=duration,
                            )
                            jobList.append(deployJobDetail)

            else:
                for master in result:
                    targetHost, dataResult = getHostViaResult(result, target, master)
                    if dataResult['stderr'] != '':
                        hasErr = True

                    deployJobDetail = DeployJobDetail(
                        host=targetHost,
                        deploy_message=dataResult['stdout'],
                        job=deployJob,
                        stderr=dataResult['stderr'],
                        job_cmd=playbookContent,
                        is_success=True if dataResult['stderr'] == '' else False,
                    )
                    jobList.append(deployJobDetail)

        os.remove(script_path)
        deployJob.deploy_status = 1 if hasErr is False else 2
        deployJob.save()
        for i in jobList:
            i.save()
        logger.info("执行脚本完成")
    except Exception as e:
        deployJob.deploy_status = 2
        deployJob.save()
        logger.info("执行失败%s:" % e)

        mail.send(
            '529280602@qq.com',  # List of email addresses also accepted
            subject='My email',
            message='Hi there!',
            html_message='Hi <strong>there</strong>!',
        )


@task(name='scanHostJob')
def scanHostJob():
    logger.info('扫描Minion启动状态列表')
    upList = []
    try:
        manageInstance = salt_api_token({'fun': 'manage.status'},
                                        SALT_REST_URL, {'X-Auth-Token': token_id()})
        statusResult = manageInstance.runnerRun()
        upList = statusResult['return'][0]['up']
    except Exception as e:
        logger.info("没有任何主机启动状态信息:%s" % e)

    logger.info("扫描客户端注册列表")
    minions_rejected = []
    minions_denied = []
    minions_pre = []
    try:
        minionsInstance = salt_api_token({'fun': 'key.list_all'},
                                         SALT_REST_URL, {'X-Auth-Token': token_id()})
        minionList = minionsInstance.wheelRun()['return'][0]['data']['return']
        minions_pre = minionList['minions_pre']
        logger.info("待接受主机:%s" % len(minions_pre))
        # minions = minionList['minions']
        minions_rejected = minionList['minions_rejected']
        logger.info("已拒绝主机:%s", len(minions_rejected))

        minions_denied = minionList['minions_denied']
        logger.info("已禁用主机:%s", len(minions_denied))
    except Exception as e:
        logger.info("扫描主机键值状态异常:%s" % e)
        # logger.info("自动主机")
        # for minion in minions_pre:
        #     logger.info("自动接受主机:%s" % minion)
        #     salt_api_token({'fun': 'key.accept', 'match': minion},
        #                    SALT_REST_URL, {'X-Auth-Token': token_id()}).wheelRun()
        # rs = Host.objects.filter(host_name=minion)
        # if len(rs) == 0:
        #     try:
        #         device = Host(host_name=minion, minion_status=2)
        #         device.save()
        #     except Exception as e:
        #         logger.info(e)

    logger.info("获取Minion主机资产信息")
    result = salt_api_token({'fun': 'grains.items', 'tgt': '*'},
                            SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
    logger.info("扫描Minion数量为[%s]", len(result))
    Host.objects.update(minion_status=0)

    for host in result:
        try:
            minionstatus = 0
            if host in upList:
                minionstatus = 1
            if host in minions_rejected:
                minionstatus = 3
            if host in minions_denied:
                minionstatus = 4

            rs = Host.objects.filter(host_name=host, host=result[host]["host"])
            if len(rs) == 0:
                logger.info("新增主机:%s", result[host]["host"])
                device = Host(host_name=host,
                              kernel=result[host]["kernel"],
                              kernel_release=result[host]["kernelrelease"],
                              virtual=result[host]["virtual"],
                              host=result[host]["host"],
                              osrelease=result[host]["osrelease"],
                              saltversion=result[host]["saltversion"],
                              osfinger=result[host]["osfinger"],
                              os_family=result[host]["os_family"],
                              num_gpus=result[host]["num_gpus"],
                              system_serialnumber=result[host]["system_serialnumber"]
                              if 'system_serialnumber' in result[host] else result[host]["serialnumber"],
                              cpu_model=result[host]["cpu_model"],
                              productname=result[host]["productname"],
                              osarch=result[host]["osarch"],
                              cpuarch=result[host]["osarch"],
                              os=result[host]["os"],
                              # num_cpus=int(result[host]["num_cpus"]),
                              mem_total=result[host]["mem_total"],
                              minion_status=minionstatus
                              )
                device.save()
                for ip in result[host]["ipv4"]:
                    hostip = HostIP(ip=ip, host=device)
                    hostip.save()
            else:
                entity = rs[0]
                logger.info("更新主机:%s", entity)
                entity.kernel = result[host]["kernel"]
                # entity.num_cpus = result[host]["num_cpus"],
                entity.kernel_release = result[host]["kernelrelease"]
                entity.virtual = result[host]["virtual"]
                entity.osrelease = result[host]["osrelease"],
                entity.saltversion = result[host]["saltversion"]
                entity.osfinger = result[host]["osfinger"]
                entity.os_family = result[host]["os_family"]
                entity.num_gpus = result[host]["num_gpus"]
                entity.system_serialnumber = result[host]["system_serialnumber"] \
                    if 'system_serialnumber' in result[host] else result[host]["serialnumber"]
                entity.cpu_model = result[host]["cpu_model"]
                entity.productname = result[host]["productname"]
                entity.osarch = result[host]["osarch"]
                entity.cpuarch = result[host]["osarch"]
                entity.os = result[host]["os"]
                entity.mem_total = result[host]["mem_total"]
                entity.minion_status = minionstatus
                entity.save()

                HostIP.objects.filter(host=entity).delete()
                for ip in result[host]["ipv4"]:
                    hostip = HostIP(ip=ip, host=entity)
                    hostip.save()

        except Exception as e:
            logger.error("自动扫描出现异常:%s", e)

    logger.info("扫描Salt-SSH主机信息")
    sshResult = salt_api_token({'fun': 'grains.items', 'tgt': '*'},
                               SALT_REST_URL, {'X-Auth-Token': token_id()}).sshRun()['return'][0]
    logger.info("扫描主机数量为[%s]", len(sshResult))
    for host in sshResult:
        try:
            if 'return' in sshResult[host]:
                rs = Host.objects.filter(host=host)
                if rs is not None:
                    entity = rs[0]
                    logger.info("更新主机:%s", host)
                    entity.host_name = sshResult[host]['return']['fqdn'] if 'fqdn' in sshResult[host]['return'] else ""
                    entity.kernel = sshResult[host]['return']['kernel']
                    entity.kernel_release = sshResult[host]['return']['kernelrelease']
                    entity.virtual = sshResult[host]['return']['virtual']
                    entity.osrelease = sshResult[host]['return']['osrelease']
                    entity.saltversion = sshResult[host]['return']['saltversion']
                    entity.osfinger = sshResult[host]['return']['osfinger']
                    entity.os_family = sshResult[host]['return']['os_family']
                    entity.num_gpus = sshResult[host]['return']['num_gpus']
                    entity.system_serialnumber = sshResult[host]['return']["serialnumber"]
                    entity.cpu_model = sshResult[host]['return']["cpu_model"]
                    entity.productname = sshResult[host]['return']["productname"]
                    entity.osarch = sshResult[host]['return']["osarch"]
                    entity.cpuarch = sshResult[host]['return']["cpuarch"]
                    entity.os = sshResult[host]['return']["os"]
                    # entity.num_cpus = int(sshResult[host]['return']["num_cpus"]),
                    # entity.mem_total = int(sshResult[host]['return']["mem_total"]),
                    entity.minion_status = 1
                    entity.save()
                    HostIP.objects.filter(host=entity).delete()
                    for ip in sshResult[host]['return']["ipv4"]:
                        hostip = HostIP(ip=ip, host=entity)
                    hostip.save()

        except Exception as e:
            traceback.print_exc()


def loadProjectConfig(id):
    obj = Project.objects.get(pk=id)
    targets = ""
    for host in obj.host.all():
        if host.enable_ssh is False:
            targets += host.host_name + ","
        else:
            targets += host.host + ","
    if targets != "":
        targets = targets[0:len(targets) - 1]
        for configobj in obj.projectconfigfile_set.all():
            salt_api_token({'fun': 'cp.push', 'tgt': targets, 'arg': configobj.config_path},
                           SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()

            for host in obj.host.all():
                if SALT_CONN_TYPE == 'http':
                    url = SALT_HTTP_URL + '/read'
                    if host.enable_ssh is False:
                        data = requests.post(url, data={
                            "name": "/var/cache/salt/master/minions/" + host.host_name + '/files' + configobj.config_path}).content
                        data = str(data, encoding="utf-8")
                    else:
                        data = requests.post(url, data={
                            "name": "/var/cache/salt/master/minions/" + host.host + configobj.config_path}).content
                        data = str(data, encoding="utf-8")
                else:
                    data = open("/var/cache/salt/master/minions/" + host.host + configobj.config_path, 'r').read()

                project_host = ProjectHost.objects.get(project=obj, host=host)
                ProjectHostConfigFile.objects.filter(project_host=project_host).delete()
                entity = ProjectHostConfigFile(project_host=project_host, file_path=configobj.config_path,
                                               file_content=data)
                entity.save()


@task(name='scanProjectConfig')
def scanProjectConfig():
    project_config_file = ProjectConfigFile.objects.all()
    for project in project_config_file:
        loadProjectConfig(project.project.id)
