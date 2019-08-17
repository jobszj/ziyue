package com.ziyue.imservice.jms;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class QueueConsumer {

    /*@Autowired
    private ConfigMapper configMapper;

    //消费队列数据项指定服务推送订单
    @JmsListener(destination = "${spring.activemq.topic.ordercreate}")
    public void createOrderTopic(String orderVo) {
        System.out.println("msg = " + orderVo);
        consumerTopic(orderVo, "CREATEORDER");
    }*/

    /*private void consumerTopic(String msg, String config) {
        List<Config> configs = configMapper.readConfig(config);
        //读取数据库配置文件，需要向哪些系统推送订单数据
        for (Config con : configs) {
            String url = con.getSurface();
            String b = con.getIsNow();
            String method = con.getMethod();
            if (b.equals("Y")) {
                System.out.println(url);
                //配置好了再打开
                //HttpUtils.post(url, msg);
            } else {
                //HttpUtils.get(url);
            }
        }
    }*/
}
