package com.ziyue.imutils;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.TimeZone;

public final class DateUtils {

    public static int daysBetween(Date d1, Date d2) {
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
        String date1 = simpleDateFormat.format(d1);
        String date2 = simpleDateFormat.format(d2);

        int i = compareDate(date1, date2);
        return i;
    }

    private static int compareDate(String strDate1, String strDate2) {
        int result = 0;
        Date date1 = null;
        Date date2 = null;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        try {
            date1 = sdf.parse(strDate1);
            date2 = sdf.parse(strDate2);

            if (date1.getTime() > date2.getTime())
                result = 1;
            else if (date1.getTime() < date2.getTime())
                result = -1;
            else
                result = 0;
        } catch (ParseException e) {
            e.printStackTrace();
        }

        return result;
    }

    //往前推*天初始化时间
    public static Date beforeDay(Date nowDate, int num) {
        //设置日期，当前日期的前num天
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(nowDate);

        calendar.set(Calendar.DATE, calendar.get(Calendar.DATE) - num);
        Date updateDate = calendar.getTime();

        return updateDate;
    }

    public static Date getTodayBegin(Date date) throws ParseException {
        TimeZone curTimeZone = TimeZone.getTimeZone("GMT+8");
        Calendar c = Calendar.getInstance(curTimeZone);
        c.setTime(date);
        c.set(Calendar.HOUR_OF_DAY, 0);
        c.set(Calendar.MINUTE, 0);
        c.set(Calendar.SECOND, 0);
        Date z = c.getTime();

        return z;
    }

    public static Date getTodayEnd(Date date) throws ParseException {
        TimeZone curTimeZone = TimeZone.getTimeZone("GMT+8");
        Calendar c = Calendar.getInstance(curTimeZone);
        c.setTime(date);
        c.set(Calendar.HOUR_OF_DAY, 23);
        c.set(Calendar.MINUTE, 59);
        c.set(Calendar.SECOND, 59);
        Date z = c.getTime();

        return z;
    }
}
