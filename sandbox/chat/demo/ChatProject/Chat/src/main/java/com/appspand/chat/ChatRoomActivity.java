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

public class ChatRoomActivity extends Activity {

    private String mMyID;
    private String mOtherID;

    private EditText mMessageText;
    private ViewGroup mMessagesContainer;
    private ScrollView mScrollContainer;

    //private MyChatController myChatController;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chatroom);

        Bundle extras = getIntent().getExtras();

        mMyID = extras.getString("my_id");
        mOtherID = extras.getString("friend_id");

        // UI stuff
        mMessagesContainer = (ViewGroup) findViewById(R.id.messagesContainer);
        mScrollContainer = (ScrollView) findViewById(R.id.scrollContainer);

        Button sendMessageButton = (Button) findViewById(R.id.sendButton);
        sendMessageButton.setOnClickListener(onSendMessageClickListener);

        mMessageText = (EditText) findViewById(R.id.messageEdit);

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.chat_room, menu);
        return true;
    }

    private void sendMessage() {
        if (mMessageText != null) {
            String messageString = mMyID + ": " + mMessageText.getText().toString();
            //myChatController.sendMessage(messageString);
            mMessageText.setText("");
            showMessage(messageString, true);
        }
    }

    private void showMessage(String message, boolean leftSide) {
        final TextView textView = new TextView(ChatRoomActivity.this);
        textView.setTextColor(Color.BLACK);
        textView.setText(message);

        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);

        if (!leftSide) {
            //bgRes = R.drawable.right_message_bg;
            params.gravity = Gravity.RIGHT;
        }

        textView.setLayoutParams(params);

        //textView.setBackgroundResource(bgRes);

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
