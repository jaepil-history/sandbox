package com.appspand.chat;

import android.util.Log;
import android.util.Pair;

import com.appspand.chat.protocol.ChatProtocol;
import com.google.gson.reflect.TypeToken;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Type;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;

import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketHandler;
import de.tavendo.autobahn.WebSocketException;

/**
 * Created by jaepil on 7/13/13.
 */

public class ChatConnector {
    private static final String TAG = ChatConnector.class.getSimpleName();
    private static final boolean D = true;

    private String mUrl = "";
    private final WebSocketConnection mConnection = new WebSocketConnection();
    private HashMap<String, AsyncResult> mAsyncResultHandlers = new HashMap<String, AsyncResult>();

    private String mLastLoginStr = "";
    private Deque<Pair<String, AsyncResult>> mMessageQueue = new ArrayDeque<Pair<String, AsyncResult>>();

    public static class AsyncResult<T> {
        private final Type mType = new TypeToken<T>(){}.getType();

        void handle(String className, String response) {
            T t = ChatProtocol.fromJSON(className, response);
            handle(t);
        }
        void handle(T response) {}
    }

    public ChatConnector(String url) {
        this.mUrl = url;
    }

    public void open()
    {
        try {
            mConnection.connect(mUrl, new WebSocketHandler() {
                @Override
                public void onOpen() {
                    if (D) Log.d(TAG, "Status: Connected to " + mUrl);

                    if (!mLastLoginStr.isEmpty()) {
                        sendMessage(mLastLoginStr);
                    }
                }

                @Override
                public void onTextMessage(String payload) {
                    if (D) Log.d(TAG, "Got message: " + payload);

                    try {
                        JSONObject command = new JSONObject(payload);
                        String cmd = command.getString("cmd");
                        if (cmd.equals("Message_NewNoti")) {
                            onNewMessage(payload);
                        } else {
                            AsyncResult handler = mAsyncResultHandlers.remove(cmd);
                            if (handler != null) {
                                handler.handle(cmd, payload);
                            }
                        }
                    }
                    catch (JSONException e)
                    {
                    }
                }

                @Override
                public void onClose(int code, String reason) {
                    if (D) Log.d(TAG, "Connection lost.");
                }
            });
        } catch (WebSocketException e) {
            if (D) Log.d(TAG, e.toString());
        }
    }

    public void close()
    {
        mConnection.disconnect();
    }

    protected void onNewMessage(String payload) {}

    private void sendMessage(String message)
    {
//        if (!mConnection.isConnected()) {
//            mConnection.reconnect();
//        } else {
//            mConnection.sendTextMessage(message);
//        }
        mConnection.sendTextMessage(message);
    }

    public void login(String userUid, String userName,
                      AsyncResult<ChatProtocol.User_LoginAns> asyncResult)
    {
        ChatProtocol.User_LoginReq req = new ChatProtocol.User_LoginReq();
        req.mUserUID = userUid;
        req.mUserName = userName;

        if (!mAsyncResultHandlers.containsKey("User_LoginAns"))
        {
            mAsyncResultHandlers.put("User_LoginAns", asyncResult);
        }

        mLastLoginStr = ChatProtocol.toJSON(userUid, req);
        sendMessage(mLastLoginStr);
    }

    public void joinGroup(String userUid, String[] invitees,
                          AsyncResult<ChatProtocol.Group_JoinAns> asyncResult)
    {
        ChatProtocol.Group_JoinReq req = new ChatProtocol.Group_JoinReq();
        req.mUserUID = userUid;
        req.mInviteeUIDs = invitees;

        if (!mAsyncResultHandlers.containsKey("Group_JoinAns"))
        {
            mAsyncResultHandlers.put("Group_JoinAns", asyncResult);
        }

        String message = ChatProtocol.toJSON(userUid, req);
        sendMessage(message);
    }

    public void leaveGroup(String userUid, String groupUid,
                           AsyncResult<ChatProtocol.Group_LeaveAns> asyncResult)
    {
        ChatProtocol.Group_LeaveReq req = new ChatProtocol.Group_LeaveReq();
        req.mUserUID = userUid;
        req.mGroupUID = groupUid;

        if (!mAsyncResultHandlers.containsKey("Group_LeaveAns"))
        {
            mAsyncResultHandlers.put("Group_LeaveAns", asyncResult);
        }

        String message = ChatProtocol.toJSON(userUid, req);
        sendMessage(message);
    }

    public void inviteUser(String userUid, String groupUid, String[] invitees,
                           AsyncResult<ChatProtocol.Group_InviteAns> asyncResult)
    {
        ChatProtocol.Group_InviteReq req = new ChatProtocol.Group_InviteReq();
        req.mUserUID = userUid;
        req.mGroupUID = groupUid;
        req.mInviteeUIDs = invitees;

        if (!mAsyncResultHandlers.containsKey("Group_InviteAns"))
        {
            mAsyncResultHandlers.put("Group_InviteAns", asyncResult);
        }

        String message = ChatProtocol.toJSON(userUid, req);
        sendMessage(message);
    }

    public void sendMessage(String senderUid, String targetUid, boolean isGroup,
                            String message, AsyncResult<ChatProtocol.Message_SendAns> asyncResult)
    {
        ChatProtocol.Message_SendReq req = new ChatProtocol.Message_SendReq();
        req.mSenderUID = senderUid;
        req.mTargetUID = targetUid;
        req.mIsGroup = isGroup;
        req.mMessage = message;

        if (!mAsyncResultHandlers.containsKey("Message_SendAns"))
        {
            mAsyncResultHandlers.put("Message_SendAns", asyncResult);
        }

        sendMessage(ChatProtocol.toJSON(senderUid, req));
    }

    public void getMessages(String userUid, String targetUid, boolean isGroup,
                            long sinceUid, int count,
                            AsyncResult<ChatProtocol.Message_GetAns> asyncResult)
    {
        ChatProtocol.Message_GetReq req = new ChatProtocol.Message_GetReq();
        req.mUserUID = userUid;
        req.mTargetUID = targetUid;
        req.mIsGroup = isGroup;
        req.mSinceUID = sinceUid;
        req.mCount = count;

        if (!mAsyncResultHandlers.containsKey("Message_GetAns"))
        {
            mAsyncResultHandlers.put("Message_GetAns", asyncResult);
        }

        sendMessage(ChatProtocol.toJSON(userUid, req));
    }

    public void markAsReadMessages(String userUid, String senderUid, boolean isGroup,
                                   long[] messageUids,
                                   AsyncResult<ChatProtocol.Message_ReadAns> asyncResult) {
        ChatProtocol.Message_ReadReq req = new ChatProtocol.Message_ReadReq();
        req.mUserUID = userUid;
        req.mSenderUID = senderUid;
        req.mIsGroup = isGroup;
        req.mMessageUIDs = messageUids;

        if (!mAsyncResultHandlers.containsKey("Message_ReadAns"))
        {
            mAsyncResultHandlers.put("Message_ReadAns", asyncResult);
        }

        sendMessage(ChatProtocol.toJSON(userUid, req));
    }
}
