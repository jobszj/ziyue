package com.ziyue.imapi.interceptor;

import java.io.PrintWriter;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.ziyue.imservice.common.jwt.JwtToken;
import com.ziyue.imservice.common.result.Constants;
import com.ziyue.imservice.common.result.ResultJson;
import org.springframework.web.servlet.HandlerInterceptor;

import com.alibaba.fastjson.JSONObject;

public class ImInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        response.setHeader("Access-Control-Allow-Origin", "*");
        String token = request.getHeader("token");
        Map<String, Object> resultMap = JwtToken.validateToken(token);

        response.setCharacterEncoding("UTF-8");
        response.setContentType("application/json; charset=utf-8");
        PrintWriter out = null;
        if (resultMap.containsKey("ERR_MSG")) {
            Constants constants = (Constants) resultMap.get("ERR_MSG");
            JSONObject res = ResultJson.buildErrorJson(constants, token);
            out = response.getWriter();
            out.append(res.toString());
            return false;
        }
        return true;
    }

}
