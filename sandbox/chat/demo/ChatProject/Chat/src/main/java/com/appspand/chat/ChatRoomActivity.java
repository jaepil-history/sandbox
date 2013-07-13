package com.appspand.chat;

import android.graphics.Color;
import android.os.Bundle;
import android.app.Activity;
import android.view.Gravity;
import android.view.Menu;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import java.sql.Date;
import java.text.DateFormat;
import java.util.Iterator;
import java.util.List;
import java.util.TimeZone;

import static java.lang.System.currentTimeMillis;

public class ChatRoomActivity extends Activity {

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
