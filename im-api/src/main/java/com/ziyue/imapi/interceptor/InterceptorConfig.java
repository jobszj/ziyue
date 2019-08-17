package com.ziyue.imapi.interceptor;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class InterceptorConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        //'/*'匹配一个文件夹
        registry.addInterceptor(new ImInterceptor()).addPathPatterns("/v1/**");

        WebMvcConfigurer.super.addInterceptors(registry);
    }

}
