/**
 ***************************************************************************************
 *  @Author     1044053532@qq.com   
 *  @License    http://www.apache.org/licenses/LICENSE-2.0
 ***************************************************************************************
 */
package com.ziyue.imservice;

import com.ziyue.imservice.common.result.ImConstants;
import com.ziyue.imservice.exception.InitErrorException;
import com.ziyue.imservice.netty.ImServerHandler;
import com.ziyue.imservice.netty.connertor.impl.ImConnertorImpl;
import com.ziyue.imservice.netty.model.MessageProxy;
import com.ziyue.imservice.netty.model.proto.MessageProto;
import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.Channel;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelFutureListener;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.ChannelPipeline;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.protobuf.ProtobufDecoder;
import io.netty.handler.codec.protobuf.ProtobufEncoder;
import io.netty.handler.codec.protobuf.ProtobufVarint32FrameDecoder;
import io.netty.handler.codec.protobuf.ProtobufVarint32LengthFieldPrepender;
import io.netty.handler.timeout.IdleStateHandler;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ImServer  {

    private final static Logger log = LoggerFactory.getLogger(ImServer.class);
    
    private ProtobufDecoder decoder = new ProtobufDecoder(MessageProto.Model.getDefaultInstance());
    private ProtobufEncoder encoder = new ProtobufEncoder();
    
    
    private MessageProxy proxy;
    private ImConnertorImpl connertor;
    private int port;
 
    private final EventLoopGroup bossGroup = new NioEventLoopGroup();
    private final EventLoopGroup workerGroup = new NioEventLoopGroup();
    private Channel channel;

    private static class SingletionWSServer {
        static final ImServer instance = new ImServer();
    }

    public static ImServer getInstance() {
        return SingletionWSServer.instance;
    }

    public void init() throws Exception {
        log.info("start qiqiim server ...");

        // Server 服务启动
        ServerBootstrap bootstrap = new ServerBootstrap();

        bootstrap.group(bossGroup, workerGroup);
        bootstrap.channel(NioServerSocketChannel.class);
        bootstrap.childHandler(new ChannelInitializer<SocketChannel>() {
            @Override
            public void initChannel(SocketChannel ch) throws Exception {
    		ChannelPipeline pipeline = ch.pipeline();
             pipeline.addLast("frameDecoder", new ProtobufVarint32FrameDecoder());
             pipeline.addLast("decoder", decoder);
             pipeline.addLast("frameEncoder", new ProtobufVarint32LengthFieldPrepender());
             pipeline.addLast("encoder",encoder);
             pipeline.addLast(new IdleStateHandler(ImConstants.ImserverConfig.READ_IDLE_TIME,ImConstants.ImserverConfig.WRITE_IDLE_TIME,0));
             pipeline.addLast("handler", new ImServerHandler(proxy, connertor));
            }
        });
        
        // 可选参数
    	bootstrap.childOption(ChannelOption.TCP_NODELAY, true);
        // 绑定接口，同步等待成功
        log.info("start qiqiim server at port[" + port + "].");
        ChannelFuture future = bootstrap.bind(port).sync();
    	channel = future.channel();
        future.addListener(new ChannelFutureListener() {
            public void operationComplete(ChannelFuture future) throws Exception {
                if (future.isSuccess()) {
                    log.info("Server have success bind to " + port);
                } else {
                    log.error("Server fail bind to " + port);
                   throw new InitErrorException("Server start fail !", future.cause());
                }
            }
        });
       // future.channel().closeFuture().syncUninterruptibly();
    }

    public void destroy() {
        log.info("destroy server ...");
        // 释放线程池资源
        if (channel != null) {
			channel.close();
		}
        bossGroup.shutdownGracefully();
        workerGroup.shutdownGracefully();
        log.info("destroy server complate.");
    }

    public void setPort(int port) {
        this.port = port;
    }

	public void setProxy(MessageProxy proxy) {
		this.proxy = proxy;
	}

    public void setConnertor(ImConnertorImpl connertor) {
		this.connertor = connertor;
	}

}
