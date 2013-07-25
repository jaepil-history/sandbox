package com.appspand.chat;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.os.Bundle;
import android.app.Activity;
import android.util.Log;
import android.view.Gravity;
import android.view.Menu;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.sql.Date;
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
        application.getChatConnector().getMessages(mMyID, mRoomID, false, 0, 100,
                new ChatConnector.AsyncResult() {
                    @Override
                    public void handle(String response) {
                        try {
                            JSONObject command = new JSONObject(response);
                            JSONObject loginAns = command.getJSONObject("payload");
                            int errorCode = loginAns.getInt("error_code");
                            if (errorCode != 0) {
                                return;
                            }

                            LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);

                            String message_info_str = loginAns.getString("message_info");
                            JSONObject message_info = new JSONObject(message_info_str);
                            JSONArray messages = message_info.getJSONArray("messages");

                            for (int i = 0; i < messages.length(); ++i) {
                                JSONObject obj = messages.getJSONObject(i);
                                String senderID = obj.getString("sender_uid");
                                int issuedAt = obj.getInt("issued_at");
                                String message = obj.getString("message");

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
                        } catch (JSONException e) {
                        }
                    }
                }
        );
    }

    @Override
    protected void onResume() {
        super.onResume();

        IntentFilter intentFilter = new IntentFilter("android.intent.action.MAIN");
        mReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String payload = intent.getStringExtra("onNewMessage");
                if (D) Log.d(TAG, payload);

                try {
                    JSONObject commandJson = new JSONObject(payload);
                    JSONObject payloadJson = commandJson.getJSONObject("payload");

                    LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);

                    String senderID = payloadJson.getString("sender_uid");
                    String message = payloadJson.getString("message");
                    int issuedAt = 0;

                    DateFormat df = DateFormat.getTimeInstance();
                    df.setTimeZone(TimeZone.getTimeZone("Asia/Seoul"));
                    String time = df.format(issuedAt);

                    String finalMessage = senderID + "(" + time + ") : " + message;
                    final TextView textView = new TextView(ChatRoomActivity.this);
                    textView.setTextColor(Color.BLACK);
                    textView.setText(finalMessage);
                    textView.setLayoutParams(params);
                    mMessagesContainer.addView(textView);

                    mScrollContainer.post(new Runnable(){
                        public void run(){
                            mScrollContainer.fullScroll(ScrollView.FOCUS_DOWN);
                        }
                    });
                } catch (JSONException e) {
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
            application.getChatConnector().sendMessage(mMyID, mRoomID, false, msg,
                    new ChatConnector.AsyncResult() {
                        @Override
                        public void handle(String response) {
                            try {
                                JSONObject command = new JSONObject(response);
                                JSONObject loginAns = command.getJSONObject("payload");
                                int errorCode = loginAns.getInt("error_code");
                                if (errorCode == 0) {
                                    //
                                }
                            } catch (JSONException e) {
                            }
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
