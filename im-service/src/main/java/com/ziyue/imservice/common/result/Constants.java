package com.ziyue.imservice.common.result;

import com.googlecode.protobuf.format.JsonFormat;
import io.netty.util.AttributeKey;

/**
 * @author 作者 : zhangjian
 * @version v1.0.
 * @描述： 返回响应码
 * @date 创建时间：2019年5月20日
 */
public enum Constants {

    //接口返回成功
    SUCCESS(10000, "success"),
    EX_GLOBAL(10001, "全局异常类型"),
    EX_CUSTOMIZE(10002, "自定义异常类型"),

    //3位数代表消息类型
    CHAT_CONNECT(100, "第一次（或重连）初始化连接"),
    CHAT_CONNECT_CHATROOM(101, "进入问答室"),
    CHAT_CONNECT_QUESTION(102, "进入提问聊天"),
    CHAT_PRIVATE(110, "私人聊天消息"),
    CHAT_PRIVATE_SIGN(111, "私聊消息签收"),
    CHAT_PRIVATE_IN(112, "私聊消息输入中"),
    CHAT_CHATROOM(120, "问答室聊天消息"),
    CHAT_CHATROOM_SIGN(121, "问答室聊天消息签收"),
    CHAT_CHATROOM_IN(122, "问答室聊天消息输入中"),
    CHAT_QUESTION(130, "提问聊天消息"),
    CHAT_QUESTION_SIGN(131, "提问聊天消息签收"),
    CHAT_QUESTION_IN(132, "提问聊天消息输入中"),
    CHAT_KEEPALIVE(140, "心跳消息"),
    CHAT_ADD_FRIENDS(150, "添加好友"),
    CHAT_AGREE_FRIEND(151, "同意添加好友"),
    CHAT_REFUSE_RFIEND(152, "拒绝添加好友");

    private int code;

    private String msg;

    Constants(int code, String msg) {
        this.code = code;
        this.msg = msg;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }
}
