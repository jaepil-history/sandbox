package com.appspand.chat;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import com.appspand.chat.protocol.ChatProtocol;

import java.text.DateFormat;
import java.util.Iterator;
import java.util.List;
import java.util.TimeZone;

import static java.lang.System.currentTimeMillis;

public class ChatRoomActivity extends Activity {
    private static final String TAG = ChatRoomActivity.class.getSimpleName();
    private static final boolean D = true;

    private BroadcastReceiver mReceiver = null;

    private String mMyID;
    private String mRoomID;

    private EditText mMessageText;
    private ViewGroup mMessagesContainer;
    private ScrollView mScrollContainer;

    private DataSource mDatasource;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chatroom);

        Bundle extras = getIntent().getExtras();

        mMyID = extras.getString("my_id");
        mRoomID = extras.getString("room_id");

        String databaseName = mMyID + ".db";
        mDatasource = new DataSource(this, databaseName);
        mDatasource.open();

        // UI stuff
        mMessagesContainer = (ViewGroup) findViewById(R.id.messagesContainer);
        mScrollContainer = (ScrollView) findViewById(R.id.scrollContainer);

        Button sendMessageButton = (Button) findViewById(R.id.sendButton);
        sendMessageButton.setOnClickListener(onSendMessageClickListener);

        mMessageText = (EditText) findViewById(R.id.messageEdit);


        //Load history
        List<Message> values = mDatasource.getAllMessage(mRoomID);
        Iterator<Message> iter = values.iterator();
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);

        while(iter.hasNext()) {
            Message msg = iter.next();
            String finalMessage = msg.getSenderID() + "(" + msg.getStringTime() + ") : " + msg.getMsg();
            final TextView textView = new TextView(ChatRoomActivity.this);
            textView.setTextColor(Color.BLACK);
            textView.setText(finalMessage);
            textView.setLayoutParams(params);
            mMessagesContainer.addView(textView);
        }

        mScrollContainer.post(new Runnable(){
            public void run(){
                mScrollContainer.fullScroll(ScrollView.FOCUS_DOWN);
            }
        });

        ChatApplication application = (ChatApplication)getApplication();
        application.getChatConnector().getMessages(mMyID, mRoomID, false, 0, 100, new long[]{},
                new ChatConnector.AsyncResult<ChatProtocol.Message_GetAns>() {
                    @Override
                    public void handle(ChatProtocol.Message_GetAns response) {
                        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);

                        for (ChatProtocol.MessageInfo m: response.mMessageInfo) {
                            String senderID = m.mSenderUID;
                            int issuedAt = m.mIssuedAt;
                            String message = m.mMessage;

                            DateFormat df = DateFormat.getTimeInstance();
                            df.setTimeZone(TimeZone.getTimeZone("Asia/Seoul"));
                            String time = df.format(issuedAt);

                            String finalMessage = senderID + "(" + time + ") : " + message;
                            final TextView textView = new TextView(ChatRoomActivity.this);
                            textView.setTextColor(Color.BLACK);
                            textView.setText(finalMessage);
                            textView.setLayoutParams(params);
                            mMessagesContainer.addView(textView);
                        }

                        mScrollContainer.post(new Runnable(){
                            public void run(){
                                mScrollContainer.fullScroll(ScrollView.FOCUS_DOWN);
                            }
                        });
                    }
                }
        );
    }

    @Override
    protected void onResume() {
        super.onResume();

        IntentFilter intentFilter = new IntentFilter(ChatService.ACTION_ON_NOTIFICATION_EVENT);
        mReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String command = intent.getStringExtra(ChatService.EXTRA_COMMAND_NAME);
                String payload = intent.getStringExtra(ChatService.EXTRA_COMMAND_DATA);
                if (D) Log.d(TAG, "onNotiEvent(" + command + "): " + payload);

                if (command.equals(ChatService.COMMAND_NEW_MESSAGE_NOTI)) {
                    ChatProtocol.Message_NewNoti noti = ChatConnector.parseNotificationEvent(command, payload);

                    String senderUid = noti.mMessageInfo.mSenderUID;
                    String message = noti.mMessageInfo.mMessage;
                    long messageUid = noti.mMessageInfo.mUID;
                    int issuedAt = 0;

                    DateFormat df = DateFormat.getTimeInstance();
                    df.setTimeZone(TimeZone.getTimeZone("Asia/Seoul"));
                    String time = df.format(issuedAt);

                    String finalMessage = senderUid + "(" + time + ") : " + message;
                    showMessage(finalMessage);

                    ChatApplication application = (ChatApplication)getApplication();
                    application.getChatConnector().markAsReadMessages(mMyID, senderUid,
                            false, new long[] {messageUid},
                            new ChatConnector.AsyncResult<ChatProtocol.Message_ReadAns>() {
                                @Override
                                public void handle(ChatProtocol.Message_ReadAns response) {
                                }
                            }
                    );
                } else if (command.equals(ChatService.COMMAND_CANCEL_MESSAGE_NOTI)) {
                    ChatProtocol.Message_CancelNoti noti = ChatConnector.parseNotificationEvent(command, payload);
                    // TODO:
                } else if (command.equals(ChatService.COMMAND_READ_MESSAGE_NOTI)) {
                    ChatProtocol.Message_ReadNoti noti = ChatConnector.parseNotificationEvent(command, payload);
                    // TODO:
                }
            }
        };

        this.registerReceiver(mReceiver, intentFilter);
    }

    @Override
    protected void onPause() {
        super.onPause();

        this.unregisterReceiver(this.mReceiver);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.chat_room, menu);
        return true;
    }

    private void sendMessage() {
        if (mMessageText != null) {
            String msg = mMessageText.getText().toString();
            long time = currentTimeMillis();
            DateFormat df = DateFormat.getTimeInstance();
            df.setTimeZone(TimeZone.getTimeZone("Asia/Seoul"));
            String gmtTime = df.format(time);
            String finalMessage = mMyID + "(" + gmtTime + ") : " + msg;

            ChatApplication application = (ChatApplication)getApplication();
            application.getChatConnector().sendMessage(mMyID, mRoomID, false, msg, false,
                    new ChatConnector.AsyncResult<ChatProtocol.Message_SendAns>() {
                        @Override
                        public void handle(ChatProtocol.Message_SendAns response) {
                        }
                    }
            );

            mDatasource.insertMessage( mRoomID, mMyID, msg, time );
            mMessageText.setText("");
            showMessage(finalMessage);
        }
    }

    private void showMessage(String message) {
        final TextView textView = new TextView(ChatRoomActivity.this);
        textView.setTextColor(Color.BLACK);
        textView.setText(message);

        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        textView.setLayoutParams(params);

        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                mMessagesContainer.addView(textView);

                // Scroll to bottom
                if (mScrollContainer.getChildAt(0) != null) {
                    mScrollContainer.scrollTo(mScrollContainer.getScrollX(), mScrollContainer.getChildAt(0).getHeight());
                }
                mScrollContainer.fullScroll(View.FOCUS_DOWN);
            }
        });
    }

    private View.OnClickListener onSendMessageClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            sendMessage();
        }
    };

}
