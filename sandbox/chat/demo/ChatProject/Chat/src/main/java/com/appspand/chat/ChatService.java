package com.appspand.chat;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;

import android.util.Log;

/**
 * Created by jaepil on 7/11/13.
 */
public class ChatService extends Service {
    // Debugging
    private static final String TAG = ChatService.class.getSimpleName();
    private static final boolean D = true;

    // Socket
    //private static final String SERVER_URL = "ws://chat.appengine.jaepil.appspand.com:8080/v1/ws";
    private static final String SERVER_URL = "ws://chat.appengine.appspand.com:8080/v1/ws";

    private ChatConnector mChatConnector = null;

//    // Actions
//    public static final String ACTION_LOGIN = "com.appspand.chat.LOGIN";
//    public static final String ACTION_LOGOUT = "com.appspand.chat.LOGOUT";
//    public static final String ACTION_INVITE_USER = "com.appspand.chat.INVITE_USER";
//    public static final String ACTION_SEND_MESSAGE = "com.appspand.chat.SEND_MESSAGE";
//
//    // Extras
//    public static final String EXTRAS_USER_ID = "user_id";
//    public static final String EXTRAS_INVITEE_ID_LIST = "invitee_id_list";
//    public static final String EXTRAS_SENDER_ID = "sender_id";
//    public static final String EXTRAS_TARGET_ID = "target_id";
//    public static final String EXTRAS_TARGET_ID_LIST = "target_id_list";
//    public static final String EXTRAS_IS_GROUP = "is_group";
//    public static final String EXTRAS_GROUP_ID = "group_id";
//    public static final String EXTRAS_GROUP_ID_LIST = "group_id_list";
//
//    public static final String EXTRAS_CHAT_MESSAGE = "chat_message";
//    public static final String EXTRAS_MESSAGE_ID = "message_id";
//    public static final String EXTRAS_MESSAGE_ID_LIST = "message_id_list";
//
//    // Constants that indicate the current connection state
//    public static final int STATE_NONE = 0;
//    public static final int STATE_CONNECTING = 10;
//    public static final int STATE_CONNECTED = 20;
//    public static final int STATE_LOGGING_IN = 30;
//    public static final int STATE_LOGGED_IN = 40;
//
//    private int mState;
//
    public ChatService()
    {
//        mState = STATE_NONE;
    }

    private final IBinder mBinder = new LocalBinder();

    public class LocalBinder extends Binder
    {
        public ChatService getService()
        {
            return ChatService.this;
        }

        public ChatConnector getChannel()
        {
            return getService().mChatConnector;
        }
    }

    @Override
    public void onCreate()
    {
        if (D) Log.d(TAG, "onCreate");

        mChatConnector = new ChatConnector(SERVER_URL) {
            @Override
            protected void onNewMessage(String payload) {
                if (D) Log.d(TAG, "onNewMessage: " + payload);

                Intent intent = new Intent("com.appspand.chat.ChatService.NewMessage");
                intent.putExtra("payload", payload);
                sendBroadcast(intent);
            }
        };
        mChatConnector.open();
    }

    @Override
    public void onDestroy()
    {
        if (D) Log.d(TAG, "onDestroy");

        mChatConnector.close();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId)
    {
        if (D) Log.d(TAG, "onStartCommand");

        super.onStartCommand(intent, flags, startId);

        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent)
    {
        if (D) Log.d(TAG, "onBind");

        return mBinder;
    }

    @Override
    public boolean onUnbind(Intent intent)
    {
        if (D) Log.d(TAG, "onUnbind");

        return true;
    }

    @Override
    public void onRebind(Intent intent)
    {
        if (D) Log.d(TAG, "onRebind");
    }
/*
    @Override
    protected void onHandleIntent(Intent intent)
    {
        if (D) Log.d(TAG, "onHandleIntent");

        Context context = getApplicationContext();
        if (intent.getAction() == ACTION_LOGIN)
        {
            String userID = intent.getStringExtra(EXTRAS_USER_ID);
        }
        else if (intent.getAction() == ACTION_LOGOUT)
        {
            String userID = intent.getStringExtra(EXTRAS_USER_ID);
        }
        else if (intent.getAction() == ACTION_INVITE_USER)
        {
            String userID = intent.getStringExtra(EXTRAS_USER_ID);
            String[] invitees = intent.getStringArrayExtra(EXTRAS_INVITEE_ID_LIST);
        }
        else if (intent.getAction() == ACTION_SEND_MESSAGE)
        {
            String userID = intent.getStringExtra(EXTRAS_USER_ID);
            String targetID = intent.getStringExtra(EXTRAS_TARGET_ID);
            boolean isGroup = intent.getBooleanExtra(EXTRAS_IS_GROUP, false);
            String message = intent.getStringExtra(EXTRAS_CHAT_MESSAGE);
        }

        SystemClock.sleep(30000); // 30 seconds
//        String resultTxt = msg + " "
//                + DateFormat.format("MM/dd/yy h:mmaa", System.currentTimeMillis());
    }*/
}
