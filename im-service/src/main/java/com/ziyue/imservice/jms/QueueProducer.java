package com.ziyue.imservice.jms;

import javax.annotation.Resource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class QueueProducer {

    /*@Resource
    private JmsMessagingTemplate jmsTemplate;

    @Value("${spring.activemq.topic.ordercreate}")
    private String orderCreate;

    @Value("${spring.activemq.topic.waystatus}")
    private String wayStatus;

    *//*
     * 向其他系统推送运单状态队列
     *//*
    public void sendTopic(String name, String msg) {
        Destination des = new ActiveMQTopic(wayStatus);
        jmsTemplate.convertAndSend(des, msg);
    }*/
}
