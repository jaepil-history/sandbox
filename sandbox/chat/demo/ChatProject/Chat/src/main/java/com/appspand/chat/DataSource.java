package com.appspand.chat;

import java.util.ArrayList;
import java.util.List;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;

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
    /*
    public void deleteMemo(Memo memo) {
        long id = memo.getId();
        database.delete(MySQLiteHelper.TABLE_MEMOS,
                MySQLiteHelper.COLUMN_ID + " = " + id, null);
    }

    public List<Memo> getAllMemos() {
        List<Memo> memos = new ArrayList<Memo>();
        Cursor cursor = null;
        try {
            cursor = database.query(MySQLiteHelper.TABLE_MEMOS,
                    allColumns, null, null, null, null, null);
            cursor.moveToFirst();
            while (!cursor.isAfterLast()) {
                Memo memo = cursorToMemo(cursor);
                memos.add(memo);
                cursor.moveToNext();
            }
            return memos;
        } finally {
            closeCursor(cursor);
        }
    }



    */

}
