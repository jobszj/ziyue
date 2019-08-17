package com.ziyue.imapi.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class RouterController {
    @RequestMapping("/chat")
    public String chat() {
        return "chat";
    }

    @RequestMapping("/index")
    public String index() {
        return "index";
    }
}
