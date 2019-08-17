package com.ziyue.imapi;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication(exclude = MongoAutoConfiguration.class)
@ComponentScan(basePackages = "com.ziyue")
@MapperScan("com.ziyue.immodel.mapper")
public class ImApiApplication {

    public static void main(String[] args) {

        SpringApplication.run(ImApiApplication.class, args);
    }

}
