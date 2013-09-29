package com.appspand.chat;

import android.util.Log;

import com.appspand.chat.protocol.ChatProtocol;

import org.json.JSONException;
import org.json.JSONObject;

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

    public static class AsyncResult<T> {
        public void handle(String className, String response) {
            T t = ChatProtocol.fromJSON(className, response);
            handle(t);
        }
        public void handle(T response) {}
    }

    public ChatConnector(String url) {
        this.mUrl = url;
    }

    private void internalOpen(final String[] data)
    {
        try {
            mConnection.connect(mUrl, new WebSocketHandler() {
                @Override
                public void onOpen() {
                    if (D) Log.d(TAG, "Status: Connected to " + mUrl);

                    if (mLastLoginStr.length() > 0) {
                        mConnection.sendTextMessage(mLastLoginStr);
                    }

                    if (data != null)
                    {
                        for (int i = 0; i < data.length; ++i)
                        {
                            mConnection.sendTextMessage(data[i]);
                        }
                    }
                }

                @Override
                public void onTextMessage(String payload) {
                    if (D) Log.d(TAG, "Got message: " + payload);

                    try {
                        JSONObject command = new JSONObject(payload);
                        String cmd = command.getString("cmd");
                        if (cmd.equals("Group_JoinNoti") || cmd.equals("Group_LeaveNoti")
                                || cmd.equals("Group_InviteNoti") || cmd.equals("Message_NewNoti")
                                || cmd.equals("Message_ReadNoti") || cmd.equals("Message_OpenNoti")
                                || cmd.equals("Message_CancelNoti")) {
                            onNotificationEvent(cmd, payload);
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

                    internalOpen(null);
                }
            });
        } catch (WebSocketException e) {
            if (D) Log.d(TAG, e.toString());
        }
    }

    public void open()
    {
        internalOpen(null);
    }

    public void close()
    {
        mConnection.disconnect();
    }

    protected void onNotificationEvent(String command, String data) {}

    public static <T> T parseNotificationEvent(String command, String data)
    {
        T noti = ChatProtocol.fromJSON(command, data);
        return noti;
    }

    private void sendMessage(String message)
    {
        if (!mConnection.isConnected()) {
            internalOpen(new String[] {message});
        } else {
            mConnection.sendTextMessage(message);
        }
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

    public void unregister(String userUid,
                           AsyncResult<ChatProtocol.User_UnregisterAns> asyncResult)
    {
        ChatProtocol.User_UnregisterReq req = new ChatProtocol.User_UnregisterReq();
        req.mUserUID = userUid;

        if (!mAsyncResultHandlers.containsKey("User_UnregisterAns"))
        {
            mAsyncResultHandlers.put("User_UnregisterAns", asyncResult);
        }

        String message = ChatProtocol.toJSON(userUid, req);
        sendMessage(message);
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

    public void getGroupInfo(String userUid, String groupUid,
                             AsyncResult<ChatProtocol.Group_InfoAns> asyncResult)
    {
        ChatProtocol.Group_InfoReq req = new ChatProtocol.Group_InfoReq();
        req.mUserUID = userUid;
        req.mGroupUID = groupUid;

        if (!mAsyncResultHandlers.containsKey("Group_InfoAns"))
        {
            mAsyncResultHandlers.put("Group_InfoAns", asyncResult);
        }

        String message = ChatProtocol.toJSON(userUid, req);
        sendMessage(message);
    }

    public void sendMessage(String senderUid, String targetUid, boolean isGroup,
                            String message, boolean isSecret,
                            AsyncResult<ChatProtocol.Message_SendAns> asyncResult)
    {
        ChatProtocol.Message_SendReq req = new ChatProtocol.Message_SendReq();
        req.mSenderUID = senderUid;
        req.mTargetUID = targetUid;
        req.mIsGroup = isGroup;
        req.mMessage = message;
        req.mIsSecret = isSecret;

        if (!mAsyncResultHandlers.containsKey("Message_SendAns"))
        {
            mAsyncResultHandlers.put("Message_SendAns", asyncResult);
        }

        sendMessage(ChatProtocol.toJSON(senderUid, req));
    }

    public void cancelMessage(String senderUid, String targetUid, boolean isGroup,
                              long messageUid, AsyncResult<ChatProtocol.Message_CancelAns> asyncResult)
    {
        ChatProtocol.Message_CancelReq req = new ChatProtocol.Message_CancelReq();
        req.mSenderUID = senderUid;
        req.mTargetUID = targetUid;
        req.mIsGroup = isGroup;
        req.mMessageUID = messageUid;

        if (!mAsyncResultHandlers.containsKey("Message_CancelAns"))
        {
            mAsyncResultHandlers.put("Message_CancelAns", asyncResult);
        }

        sendMessage(ChatProtocol.toJSON(senderUid, req));
    }

    public void openMessage(String senderUid, String targetUid, boolean isGroup,
                            long messageUid, AsyncResult<ChatProtocol.Message_OpenAns> asyncResult)
    {
        ChatProtocol.Message_OpenReq req = new ChatProtocol.Message_OpenReq();
        req.mSenderUID = senderUid;
        req.mTargetUID = targetUid;
        req.mIsGroup = isGroup;
        req.mMessageUID = messageUid;

        if (!mAsyncResultHandlers.containsKey("Message_OpenAns"))
        {
            mAsyncResultHandlers.put("Message_OpenAns", asyncResult);
        }

        sendMessage(ChatProtocol.toJSON(senderUid, req));
    }

    public void getMessages(String userUid, String targetUid, boolean isGroup,
                            long sinceUid, int count, long[] messageUids,
                            AsyncResult<ChatProtocol.Message_GetAns> asyncResult)
    {
        ChatProtocol.Message_GetReq req = new ChatProtocol.Message_GetReq();
        req.mUserUID = userUid;
        req.mTargetUID = targetUid;
        req.mIsGroup = isGroup;
        req.mSinceUID = sinceUid;
        req.mCount = count;
        req.mMessageUIDs = messageUids;

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

    public void clearMessages(String userUid, String targetUid,
                              AsyncResult<ChatProtocol.Message_ClearAns> asyncResult) {
        ChatProtocol.Message_ClearReq req = new ChatProtocol.Message_ClearReq();
        req.mUserUID = userUid;
        req.mTargetUID = targetUid;

        if (!mAsyncResultHandlers.containsKey("Message_ClearAns"))
        {
            mAsyncResultHandlers.put("Message_ClearAns", asyncResult);
        }

        sendMessage(ChatProtocol.toJSON(userUid, req));
    }
}
