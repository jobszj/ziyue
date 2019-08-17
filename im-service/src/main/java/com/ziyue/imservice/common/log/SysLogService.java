package com.ziyue.imservice.common.log;

import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class SysLogService {

    public static Logger log = LoggerFactory.getLogger(SysLogService.class);

    public boolean save(SysLogDomain sysLog) {

        //写入文件日志中
        log.info(sysLog.toString());

        //向数据库中记录核心数据
        return true;
    }
}
