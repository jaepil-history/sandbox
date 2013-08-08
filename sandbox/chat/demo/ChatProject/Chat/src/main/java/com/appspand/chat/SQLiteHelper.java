package com.appspand.chat;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class SQLiteHelper extends SQLiteOpenHelper {
    private static final String DATABASE_CREATE_FRIEND_LIST = "create table friend_list (_id integer primary key autoincrement, user_id text not null);" ;
    private static final String DATABASE_CREATE_MESSAGE_LIST = "create table message_list (_id integer primary key autoincrement, room_id text not null, sender_id text not null, msg text not null, time integer not null);" ;

    public SQLiteHelper(Context context, String name) {
        super(context, name, null, 1);
    }

    @Override
    public void onCreate(SQLiteDatabase database) {
        database.execSQL(DATABASE_CREATE_FRIEND_LIST);
        database.execSQL(DATABASE_CREATE_MESSAGE_LIST);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db,
                          int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS friend_list");
        db.execSQL("DROP TABLE IF EXISTS message_list");
        onCreate(db);
    }
}