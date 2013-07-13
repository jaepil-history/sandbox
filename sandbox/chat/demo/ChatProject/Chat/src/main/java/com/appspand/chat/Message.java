package com.appspand.chat;

import java.text.DateFormat;
import java.util.TimeZone;

/**
 * Created by wannafree on 13. 7. 13..
 */
public class Message {
    private long idx;
    private String room_id;
    private String sender_id;
    private String msg;
    private long time;
    DateFormat df;

    Message ()
    {
        df = DateFormat.getTimeInstance();
        df.setTimeZone(TimeZone.getTimeZone("Asia/Seoul"));
    }

    public long getIdx()
    {
        return idx;
    }

    public void setIdx(long idx) {
        this.idx = idx;
    }

    public String getRoomID() {
        return room_id;
    }

    public void setRoomID(String room_id) {
        this.room_id = room_id;
    }

    public String getSenderID() {
        return sender_id;
    }

    public void setSenderID(String sender_id) {
        this.sender_id = sender_id;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public long getTime() {
        return time;
    }

    public String getStringTime() {

        return df.format(this.time);
    }

    public void setTime(long time) {
        this.time = time;
    }



    @Override
    public String toString() {
        String finalMessage = "[" + this.room_id + "]\r\n" + this.sender_id + "(" + this.getStringTime() + ") : " + this.msg;
        return finalMessage;
    }

}
