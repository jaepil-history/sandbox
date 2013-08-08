package com.appspand.chat;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by wannafree on 13. 7. 11..
 */


public class DataSource {
    private SQLiteDatabase	database;
    private SQLiteHelper	dbHelper;

    public DataSource(Context context, String databaseName) {
        dbHelper = new SQLiteHelper(context,databaseName);
    }

    public void open() throws SQLException {
        database = dbHelper.getWritableDatabase();
    }

    public void close() {
        dbHelper.close();
    }


    public Message insertMessage(String room_id, String sender_id, String msg, long time) {
        ContentValues values = new ContentValues();
        values.put("room_id", room_id);
        values.put("sender_id", sender_id);
        values.put("msg", msg);
        values.put("time", time);

        long insertId = database.insert( "message_list", null,values);
        Message message = new Message();
        message.setIdx(insertId);
        message.setRoomID(room_id);
        message.setSenderID(sender_id);
        message.setMsg(msg);
        message.setTime(time);

        return message;
    }

    public List<Message> getAllMessage(String room_id) {
        List<Message> messageList = new ArrayList<Message>();
        Cursor cursor = null;
        try {
            String[] parms={room_id};

            cursor = database.query("message_list", null, "room_id=?", parms, null, null, null);
            cursor.moveToFirst();
            while (!cursor.isAfterLast()) {
                Message message = cursorToMessage(cursor);
                messageList.add(message);
                cursor.moveToNext();
            }
            return messageList;
        } finally {
            closeCursor(cursor);
        }
    }

    public List<Message> getLastMessage() {
        List<Message> messageList = new ArrayList<Message>();
        Cursor cursor = null;
        try {
            cursor = database.rawQuery("SELECT * FROM message_list group by room_id order by time desc", null);
            cursor.moveToFirst();
            while (!cursor.isAfterLast()) {
                Message message = cursorToMessage(cursor);
                messageList.add(message);
                cursor.moveToNext();
            }
            return messageList;
        } finally {
            closeCursor(cursor);
        }
    }

    private Message cursorToMessage(Cursor cursor) {
        Message message = new Message();
        int idIndex = cursor.getColumnIndex("_id");
        int roomIDIndex = cursor.getColumnIndex("room_id");
        int senderIDIndex = cursor.getColumnIndex("sender_id");
        int msgIDIndex = cursor.getColumnIndex("msg");
        int timeIDIndex = cursor.getColumnIndex("time");

        message.setIdx(cursor.getLong(idIndex));
        message.setRoomID(cursor.getString(roomIDIndex));
        message.setSenderID(cursor.getString(senderIDIndex));
        message.setMsg(cursor.getString(msgIDIndex));
        message.setTime(cursor.getLong(timeIDIndex));

        return message;
    }

    public Friend insertFriend(String id) {
        ContentValues values = new ContentValues();
        values.put("user_id", id);
        long insertId = database.insert( "friend_list", null,values);
        Friend friend = new Friend();
        friend.setIdx(insertId);
        friend.setUserID(id);
        return friend;

    }

    public List<Friend> getAllFriends() {
        List<Friend> friendList = new ArrayList<Friend>();
        Cursor cursor = null;
        try {
            cursor = database.query("friend_list", null, null, null, null, null, null);
            cursor.moveToFirst();
            while (!cursor.isAfterLast()) {
                Friend friend = cursorToFriend(cursor);
                friendList.add(friend);
                cursor.moveToNext();
            }
            return friendList;
        } finally {
            closeCursor(cursor);
        }
    }

    private Friend cursorToFriend(Cursor cursor) {
        Friend friend = new Friend();
        int idIndex = cursor.getColumnIndex("_id");
        int userIDIndex = cursor.getColumnIndex("user_id");
        friend.setIdx(cursor.getLong(idIndex));
        friend.setUserID(cursor.getString(userIDIndex));
        return friend;
    }

    private void closeCursor(Cursor cursor) {
        try {
            if (cursor != null) {
                cursor.close();
            }
        } catch (Exception e) {
        }
    }

}
