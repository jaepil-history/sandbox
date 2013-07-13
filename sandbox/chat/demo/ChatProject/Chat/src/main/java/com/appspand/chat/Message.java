package com.appspand.chat;

/**
 * Created by wannafree on 13. 7. 13..
 */
public class Message {
    private long idx;
    private String user_id;
    private String msg;
    private long time;

    public long getIdx()
    {
        return idx;
    }

    public void setIdx(long idx) {
        this.idx = idx;
    }

    public String getUserID() {
        return user_id;
    }

    public void setUserID(String userID) {
        this.user_id = userID;
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

    public void setTime(long time) {
        this.time = time;
    }

    @Override
    public String toString() {
        return user_id;
    }
}
