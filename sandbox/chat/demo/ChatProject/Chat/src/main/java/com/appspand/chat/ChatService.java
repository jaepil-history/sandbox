package com.appspand.chat;

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.SystemClock;
import android.text.format.DateFormat;

import android.util.Log;

/**
 * Created by jaepil on 7/11/13.
 */
public class ChatService extends IntentService {
    // Debugging
    private static final String TAG = ChatService.class.getSimpleName();
    private static final boolean D = true;

    // Actions
    public static final String ACTION_LOGIN = "com.appspand.chat.LOGIN";
    public static final String ACTION_LOGOUT = "com.appspand.chat.LOGOUT";
    public static final String ACTION_INVITE_USER = "com.appspand.chat.INVITE_USER";
    public static final String ACTION_SEND_MESSAGE = "com.appspand.chat.SEND_MESSAGE";

    // Extras
    public static final String EXTRAS_USER_ID = "user_id";
    public static final String EXTRAS_INVITEE_ID_LIST = "invitee_id_list";
    public static final String EXTRAS_SENDER_ID = "sender_id";
    public static final String EXTRAS_TARGET_ID = "target_id";
    public static final String EXTRAS_TARGET_ID_LIST = "target_id_list";
    public static final String EXTRAS_IS_GROUP = "is_group";
    public static final String EXTRAS_GROUP_ID = "group_id";
    public static final String EXTRAS_GROUP_ID_LIST = "group_id_list";

    public static final String EXTRAS_CHAT_MESSAGE = "chat_message";
    public static final String EXTRAS_MESSAGE_ID = "message_id";
    public static final String EXTRAS_MESSAGE_ID_LIST = "message_id_list";

    // Constants that indicate the current connection state
    public static final int STATE_NONE = 0;
    public static final int STATE_CONNECTING = 10;
    public static final int STATE_CONNECTED = 20;
    public static final int STATE_LOGGING_IN = 30;
    public static final int STATE_LOGGED_IN = 40;

    private int mState;

    public ChatService()
    {
        super(ChatService.class.getSimpleName());

        mState = STATE_NONE;
    }

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
    }
}
