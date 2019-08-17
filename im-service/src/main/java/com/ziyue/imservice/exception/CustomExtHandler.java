package com.ziyue.imservice.exception;

import com.ziyue.imservice.common.result.Constants;
import com.ziyue.imservice.common.result.ResultJson;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import javax.servlet.http.HttpServletRequest;

@RestControllerAdvice
public class CustomExtHandler {

    private static final Logger LOG = LoggerFactory.getLogger(CustomExtHandler.class);

	/*@ExceptionHandler(value=Exception.class)
	public Object handleException(Exception e, HttpServletRequest request){
		LOG.error("url {}, msg {}", request.getRequestURL(), e.getMessage()); 
		return ResultJson.buildError(Constants.EX_GLOBAL, e);
	}*/

    @ExceptionHandler(value = ImException.class)
    public Object handleOMSException(ImException e, HttpServletRequest request) {
        LOG.error("url {}, msg {}", request.getRequestURL(), e.getMessage());
        return ResultJson.buildError(Constants.EX_CUSTOMIZE, e.getMessage());

        //进行页面跳转
        /*ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("error.html");
        modelAndView.addObject("msg", e.getMsg());
        return modelAndView;*/
    }
}
