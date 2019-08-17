package com.ziyue.imservice.service.impl;

import com.ziyue.imentity.entity.Vo.UserMessageEntity;
import com.ziyue.immodel.dao.UserMessageMapper;
import com.ziyue.imservice.service.UserMessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class UserMessageServiceImpl implements UserMessageService {

	private UserMessageMapper userMessageMapper;
	
	@Override
	public UserMessageEntity queryObject(Long id){
		return userMessageMapper.queryObject(id);
	}
	
	@Override
	public List<UserMessageEntity> queryList(Map<String, Object> map){
		return userMessageMapper.queryList(map);
	}
	
	@Override
	public int queryTotal(Map<String, Object> map){
		return userMessageMapper.queryTotal(map);
	}
	
	@Override
	public void save(UserMessageEntity userMessage){
		userMessageMapper.save(userMessage);
	}
	
	@Override
	public int update(UserMessageEntity userMessage){
		return userMessageMapper.update(userMessage);
	}
	
	@Override
	public int delete(Long id){
		return userMessageMapper.delete(id);
	}
	
	@Override
	public int deleteBatch(Long[] ids){
		return userMessageMapper.deleteBatch(ids);
	}

	@Override
	public List<UserMessageEntity> getHistoryMessageList(Map<String, Object> map) {
		return userMessageMapper.getHistoryMessageList(map);
	}

	@Override
	public int getHistoryMessageCount(Map<String, Object> map) {
		return userMessageMapper.getHistoryMessageCount(map);
	}

	@Override
	public List<UserMessageEntity> getOfflineMessageList(Map<String, Object> map) {
		 List<UserMessageEntity> result = userMessageMapper.getOfflineMessageList(map);
		 //更新状态为已读状态
		userMessageMapper.updatemsgstate(map);
		 return result;
	}
	
}
