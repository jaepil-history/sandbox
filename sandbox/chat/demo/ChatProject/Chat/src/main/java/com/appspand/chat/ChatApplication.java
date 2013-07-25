package com.appspand.chat;

import android.app.Activity;
import android.app.Application;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.res.Configuration;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;

/**
 * Created by jaepil on 7/13/13.
 */
public class ChatApplication extends Application
{
    private static final String TAG = ChatApplication.class.getSimpleName();
    private static final boolean D = true;

    private Activity mCurrentActivity = null;

    private ActivityLifecycleCallbacks callbacks = new ActivityLifecycleCallbacks() {
        @Override
        public void onActivityCreated(Activity activity, Bundle bundle) {
            if (D) Log.d(TAG, "onActivityCreated");
        }

        @Override
        public void onActivityStarted(Activity activity) {
            if (D) Log.d(TAG, "onActivityStarted");
        }

        @Override
        public void onActivityResumed(Activity activity) {
            if (D) Log.d(TAG, "onActivityResumed");
        }

        @Override
        public void onActivityPaused(Activity activity) {
            if (D) Log.d(TAG, "onActivityPaused");
        }

        @Override
        public void onActivityStopped(Activity activity) {
            if (D) Log.d(TAG, "onActivityStopped");
        }

        @Override
        public void onActivitySaveInstanceState(Activity activity, Bundle bundle) {
        }

        @Override
        public void onActivityDestroyed(Activity activity) {
            if (D) Log.d(TAG, "onActivityDestroyed");
        }
    };

    @Override
    public void onCreate()
    {
        if (D) Log.d(TAG, "onCreated");

        super.onCreate();

        registerActivityLifecycleCallbacks(callbacks);

        doBindService();
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig)
    {
        super.onConfigurationChanged(newConfig);
    }

    private ChatService mChatService = null;
    private ChatConnector mChatConnector = null;
    private boolean mIsBound = false;
    private ServiceConnection mServiceConnection = new ServiceConnection()
    {
        public void onServiceConnected(ComponentName className, IBinder service)
        {
            if (D) Log.d(TAG, "onServiceConnected");

            // This is called when the connection with the service has been
            // established, giving us the service object we can use to
            // interact with the service.  Because we have bound to a explicit
            // service that we know is running in our own process, we can
            // cast its IBinder to a concrete class and directly access it.
            mChatService = ((ChatService.LocalBinder)service).getService();
            mChatConnector = ((ChatService.LocalBinder)service).getChannel();

//            // Tell the user about this for our demo.
//            Toast.makeText(Binding.this, R.string.local_service_connected,
//                    Toast.LENGTH_SHORT).show();
        }

        public void onServiceDisconnected(ComponentName className)
        {
            if (D) Log.d(TAG, "onServiceDisconnected");

            // This is called when the connection with the service has been
            // unexpectedly disconnected -- that is, its process crashed.
            // Because it is running in our same process, we should never
            // see this happen.
            mChatService = null;
            mChatConnector = null;
//            Toast.makeText(Binding.this, R.string.local_service_disconnected,
//                    Toast.LENGTH_SHORT).show();
        }
    };

    public ChatService getChatService()
    {
        return mChatService;
    }

    public ChatConnector getChatConnector()
    {
        return mChatConnector;
    }

    private void doStartService()
    {
        Intent chatService = new Intent(this, ChatService.class);
        startService(chatService);
    }

    private void doStopService()
    {
        Intent chatService = new Intent(this, ChatService.class);
        stopService(chatService);
    }

    private void doBindService()
    {
        // Establish a connection with the service.  We use an explicit
        // class name because we want a specific service implementation that
        // we know will be running in our own process (and thus won't be
        // supporting component replacement by other applications).
        bindService(new Intent(ChatApplication.this,
                ChatService.class), mServiceConnection, Context.BIND_AUTO_CREATE);
        mIsBound = true;
    }

    private void doUnbindService()
    {
        if (mIsBound)
        {
            // Detach our existing connection.
            unbindService(mServiceConnection);
            mIsBound = false;
        }
    }
}
