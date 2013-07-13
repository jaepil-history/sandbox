package com.appspand.chat;

/**
 * Created by wannafree on 13. 7. 11..
 */
public class Friend {
    private long idx;
    private String user_id;

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

    @Override
    public String toString() {
        return user_id;
    }

}
