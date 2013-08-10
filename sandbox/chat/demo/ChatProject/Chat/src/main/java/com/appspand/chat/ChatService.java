package com.appspand.chat;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.util.Log;

import com.appspand.chat.protocol.ChatProtocol;

/**
 * Created by jaepil on 7/11/13.
 */
public class ChatService extends Service {
    // Debugging
    private static final String TAG = ChatService.class.getSimpleName();
    private static final boolean D = true;

    // Socket
    private static final String SERVER_URL = "ws://chat.dev.appspand.com/v1/ws";
    private ChatConnector mChatConnector = null;

    // Actions
    public static final String ACTION_ON_NEW_MESSAGE = "com.appspand.chat.ChatService.NewMessage";
    public static final String EXTRA_ON_NEW_MESSAGE = "payload";

    public ChatService()
    {
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
            protected void onNewMessage(String newMessage) {
                if (D) Log.d(TAG, "onNewMessage: " + newMessage);

                Intent intent = new Intent(ACTION_ON_NEW_MESSAGE);
                intent.putExtra(EXTRA_ON_NEW_MESSAGE, newMessage);
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
}
