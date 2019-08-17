package com.ziyue.imapi;

import com.ziyue.imservice.ImServer;
import org.springframework.context.ApplicationListener;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.stereotype.Component;

@Component
public class NettyBooter implements ApplicationListener<ContextRefreshedEvent> {

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        if (event.getApplicationContext().getParent() == null){
            try {
                ImServer.getInstance().init();
            }catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
