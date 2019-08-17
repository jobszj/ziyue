package com.ziyue.imservice.common.jwt;

import com.ziyue.imservice.common.result.Constants;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.MalformedJwtException;
import io.jsonwebtoken.SignatureAlgorithm;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class JwtToken {

    private static Logger logger = LoggerFactory.getLogger(JwtToken.class);
    public static final long EXPIRATION_TIME = 3600_000_000L;
    static final String JWT_SECRET = "asdfghjkl1234567890";
    static final String TOKEN_PREFIX = "Bearer";

    /**
     * 生成jwt token
     */
    public static String generateToken(String username, Date generateTime) {
        HashMap<String, Object> map = new HashMap<>();
        //可以把任何安全的数据放到map里面
        map.put("username", username);
        map.put("generateTime", generateTime);
        String jwt = Jwts.builder()
                .setClaims(map)
                .setExpiration(new Date(generateTime.getTime() + EXPIRATION_TIME))
                .signWith(SignatureAlgorithm.HS512, JWT_SECRET)
                .compact();
        return jwt;
    }

    public static Map<String, Object> validateToken(String token) {
        Map<String, Object> resp = new HashMap<String, Object>();
        if (token != null) {
            // 解析token
            try {
                Map<String, Object> body = Jwts.parser()
                        .setSigningKey(JWT_SECRET)
                        .parseClaimsJws(token)
                        .getBody();
                String username = (String) (body.get("username"));
                Date generateTime = new Date((Long) body.get("generateTime"));

                if (username == null || username.isEmpty()) {
                    resp.put("ERR_MSG", Constants.EX_GLOBAL);
                    return resp;
                }
                resp.put("username", username);
                resp.put("generateTime", generateTime);
                return resp;
            } catch (MalformedJwtException e) {
                // don't trust the JWT!
                // jwt 解析错误
                resp.put("ERR_MSG", Constants.EX_GLOBAL);
                return resp;
            } catch (ExpiredJwtException e) {
                // jwt 已经过期，在设置jwt的时候如果设置了过期时间，这里会自动判断jwt是否已经过期，如果过期则会抛出这个异常，我们可以抓住这个异常并作相关处理。
                resp.put("ERR_MSG", Constants.EX_GLOBAL);
                return resp;
            }
        } else {
            resp.put("ERR_MSG", Constants.EX_GLOBAL);
            return resp;
        }
    }

}
