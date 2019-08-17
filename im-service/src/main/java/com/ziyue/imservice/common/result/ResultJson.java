package com.ziyue.imservice.common.result;

import com.alibaba.fastjson.JSONObject;

import java.io.Serializable;

public class ResultJson implements Serializable {

    private static final long serialVersionUID = 1L;

    private Integer code;  // 状态码
    private Object data;   // 数据
    private String msg;    // 描述

    public ResultJson(Integer code, Object data, String msg) {
        this.code = code;
        this.data = data;
        this.msg = msg;
    }

    //成功
    public static ResultJson buildSuccess(Constants c, Object data) {
        return new ResultJson(c.getCode(), data, c.getMsg());
    }

    // 失败
    public static ResultJson buildError(Constants c, Object data) {
        return new ResultJson(c.getCode(), data, c.getMsg());
    }

    public static JSONObject buildErrorJson(Constants c, Object data) {
        JSONObject rest = new JSONObject();
        rest.put("code", c.getCode());
        rest.put("data", data);
        rest.put("msg", c.getMsg());
        return rest;
    }

    public Integer getCode() {
        return code;
    }

    public void setCode(Integer code) {
        this.code = code;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    @Override
    public String toString() {
        return "{code=" + code + ", data=" + data + ", msg=" + msg
                + "}";
    }
}
