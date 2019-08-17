package com.ziyue.imentity.entity.Vo;

import lombok.Data;

import java.util.Date;

@Data
public class Message {
    //消息的id,用于向前端和mongodb中插入数据
    private Integer msgid;
    //发送人
    private Integer senduser;
    //发送人昵称或姓名
    private String sendusername;
    //发送人头像
    private String avatar;
    //接收人
    private Integer receiveuser;
    //群ID
    private Integer chatroomid;
    //提问id
    private Integer questionid;
    //是否已读 0 未读  1 已读
    private Integer isread;
    //类型 0 单聊消息  1 群消息  心跳  连接、断线重连
    private Integer type=0;
    //消息类型,文本、视频、音频、
    private String msgType;
    //消息内容
    private String content;
    //发送消息的时间
    private Date time;
}
