package com.appspand.chat;

import android.util.Log;
import android.util.Pair;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;

import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketConnectionHandler;
import de.tavendo.autobahn.WebSocketException;

/**
 * Created by jaepil on 7/13/13.
 */

public class ChatConnector {
    private static final String TAG = ChatConnector.class.getSimpleName();
    private static final boolean D = true;

    private String mUrl;
    private final WebSocketConnection mConnection = new WebSocketConnection();
    private HashMap<String, AsyncResult> mAsyncResultHandlers = new HashMap<String, AsyncResult>();

    private String mLastLoginStr;
    private Deque<Pair<String, AsyncResult>> mMessageQueue = new ArrayDeque<Pair<String, AsyncResult>>();

    public interface AsyncResult {
        abstract void handle(String response);
    }

    public ChatConnector(String url) {
        this.mUrl = url;
    }

    public void open()
    {
        try {
            mConnection.connect(mUrl, new WebSocketConnectionHandler() {
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
                                handler.handle(payload);
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
        if (!mConnection.isConnected()) {
            mConnection.reconnect();
        } else {
            mConnection.sendTextMessage(message);
        }
    }

    public void login(String userUid, String userName, AsyncResult asyncResult)
    {
        try {
            JSONObject payload = new JSONObject();
            payload.put("user_uid", userUid);
            payload.put("user_name", userName);

            JSONObject command = new JSONObject();
            command.put("cmd", "User_LoginReq");
            command.put("user_uid", userUid);
            command.put("payload", payload);

            if (!mAsyncResultHandlers.containsKey("User_LoginAns"))
            {
                mAsyncResultHandlers.put("User_LoginAns", asyncResult);
            }

            mLastLoginStr = command.toString();
            sendMessage(mLastLoginStr);
        }
        catch (JSONException e) {
        }
        finally {
        }
    }

    public void joinGroup(String userUid, String[] invitees, AsyncResult asyncResult)
    {
        try {
            JSONObject payload = new JSONObject();
            payload.put("user_uid", userUid);
            JSONArray uids = new JSONArray();
            for (int i = 0; i < invitees.length; ++i) {
                uids.put(invitees[i]);
            }
            payload.put("invitee_uids", uids);

            JSONObject command = new JSONObject();
            command.put("cmd", "Group_JoinReq");
            command.put("user_uid", userUid);
            command.put("payload", payload);

            if (!mAsyncResultHandlers.containsKey("Group_JoinAns"))
            {
                mAsyncResultHandlers.put("Group_JoinAns", asyncResult);
            }
            sendMessage(command.toString());
        }
        catch (JSONException e) {
        }
        finally {
        }
    }

    public void leaveGroup(String userUid, String groupUid, AsyncResult asyncResult)
    {
        try {
            JSONObject payload = new JSONObject();
            payload.put("user_uid", userUid);
            payload.put("group_uid", groupUid);

            JSONObject command = new JSONObject();
            command.put("cmd", "Group_LeaveReq");
            command.put("user_uid", userUid);
            command.put("payload", payload);

            if (!mAsyncResultHandlers.containsKey("Group_LeaveAns"))
            {
                mAsyncResultHandlers.put("Group_LeaveAns", asyncResult);
            }
            sendMessage(command.toString());
        }
        catch (JSONException e) {
        }
        finally {
        }
    }

    public void inviteUser(String userUid, String groupUid, String[] invitees,
                           AsyncResult asyncResult)
    {
        try {
            JSONObject payload = new JSONObject();
            payload.put("user_uid", userUid);
            payload.put("group_uid", groupUid);
            JSONArray uids = new JSONArray();
            for (int i = 0; i < invitees.length; ++i) {
                uids.put(invitees[i]);
            }
            payload.put("invitee_uids", uids);

            JSONObject command = new JSONObject();
            command.put("cmd", "Group_InviteReq");
            command.put("user_uid", userUid);
            command.put("payload", payload);

            if (!mAsyncResultHandlers.containsKey("Group_InviteAns"))
            {
                mAsyncResultHandlers.put("Group_InviteAns", asyncResult);
            }
            sendMessage(command.toString());
        }
        catch (JSONException e) {
        }
        finally {
        }
    }

    public void sendMessage(String senderUid, String targetUid, boolean isGroup,
                            String message, AsyncResult asyncResult)
    {
        try {
            JSONObject payload = new JSONObject();
            payload.put("sender_uid", senderUid);
            payload.put("target_uid", targetUid);
            payload.put("is_group", isGroup);
            payload.put("message", message);

            JSONObject command = new JSONObject();
            command.put("cmd", "Message_SendReq");
            command.put("user_uid", senderUid);
            command.put("payload", payload);

            if (!mAsyncResultHandlers.containsKey("Message_SendAns"))
            {
                mAsyncResultHandlers.put("Message_SendAns", asyncResult);
            }
            sendMessage(command.toString());
        }
        catch (JSONException e) {
        }
        finally {
        }
    }

    public void getMessages(String userUid, String targetUid, boolean isGroup,
                            long sinceUid, int count, AsyncResult asyncResult)
    {
        try {
            JSONObject payload = new JSONObject();
            payload.put("user_uid", userUid);
            payload.put("target_uid", targetUid);
            payload.put("is_group", isGroup);
            payload.put("since_uid", sinceUid);
            payload.put("count", count);

            JSONObject command = new JSONObject();
            command.put("cmd", "Message_GetReq");
            command.put("user_uid", userUid);
            command.put("payload", payload);

            if (!mAsyncResultHandlers.containsKey("Message_GetAns"))
            {
                mAsyncResultHandlers.put("Message_GetAns", asyncResult);
            }
            sendMessage(command.toString());
        }
        catch (JSONException e) {
        }
        finally {
        }
    }

    public void markAsReadMessages(String userUid, String senderUid, boolean isGroup,
                                   long[] messageUids, AsyncResult asyncResult) {
        try {
            JSONObject payload = new JSONObject();
            payload.put("user_uid", userUid);
            payload.put("sender_uid", senderUid);
            payload.put("is_group", isGroup);
            JSONArray uids = new JSONArray();
            for (int i = 0; i < messageUids.length; ++i) {
                uids.put(messageUids[i]);
            }
            payload.put("message_uids", uids);


            JSONObject command = new JSONObject();
            command.put("cmd", "Message_ReadReq");
            command.put("user_uid", userUid);
            command.put("payload", payload);

            if (!mAsyncResultHandlers.containsKey("Message_ReadAns"))
            {
                mAsyncResultHandlers.put("Message_ReadAns", asyncResult);
            }
            sendMessage(command.toString());
        }
        catch (JSONException e) {
        }
        finally {
        }
    }
}
