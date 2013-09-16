package com.appspand.chat.protocol;

import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by jaepil on 8/3/13.
 */
public class ChatProtocol {
    private static final Map<String, Type> TypeMap = new HashMap<String, Type>(){{
        put("User_LoginReq", new TypeToken<Header<User_LoginReq>>(){}.getType());
        put("User_LoginAns", new TypeToken<Header<User_LoginAns>>(){}.getType());
        put("User_UnregisterAns", new TypeToken<Header<User_UnregisterAns>>(){}.getType());

        put("Group_JoinReq", new TypeToken<Header<Group_JoinReq>>(){}.getType());
        put("Group_JoinAns", new TypeToken<Header<Group_JoinAns>>(){}.getType());
        put("Group_JoinNoti", new TypeToken<Header<Group_JoinNoti>>(){}.getType());
        put("Group_LeaveReq", new TypeToken<Header<Group_LeaveReq>>(){}.getType());
        put("Group_LeaveAns", new TypeToken<Header<Group_LeaveAns>>(){}.getType());
        put("Group_LeaveNoti", new TypeToken<Header<Group_LeaveNoti>>(){}.getType());
        put("Group_InviteReq", new TypeToken<Header<Group_InviteReq>>(){}.getType());
        put("Group_InviteAns", new TypeToken<Header<Group_InviteAns>>(){}.getType());
        put("Group_InviteNoti", new TypeToken<Header<Group_InviteNoti>>(){}.getType());
        put("Group_InfoReq", new TypeToken<Header<Group_InfoReq>>(){}.getType());
        put("Group_InfoAns", new TypeToken<Header<Group_InfoAns>>(){}.getType());

        put("Message_SendReq", new TypeToken<Header<Message_SendReq>>(){}.getType());
        put("Message_SendAns", new TypeToken<Header<Message_SendAns>>(){}.getType());
        put("Message_NewNoti", new TypeToken<Header<Message_NewNoti>>(){}.getType());
        put("Message_CancelReq", new TypeToken<Header<Message_CancelReq>>(){}.getType());
        put("Message_CancelAns", new TypeToken<Header<Message_CancelAns>>(){}.getType());
        put("Message_CancelNoti", new TypeToken<Header<Message_CancelNoti>>(){}.getType());
        put("Message_OpenReq", new TypeToken<Header<Message_OpenReq>>(){}.getType());
        put("Message_OpenAns", new TypeToken<Header<Message_OpenAns>>(){}.getType());
        put("Message_OpenNoti", new TypeToken<Header<Message_OpenNoti>>(){}.getType());
        put("Message_ReadReq", new TypeToken<Header<Message_ReadReq>>(){}.getType());
        put("Message_ReadAns", new TypeToken<Header<Message_ReadAns>>(){}.getType());
        put("Message_ReadNoti", new TypeToken<Header<Message_ReadNoti>>(){}.getType());
        put("Message_GetReq", new TypeToken<Header<Message_GetReq>>(){}.getType());
        put("Message_GetAns", new TypeToken<Header<Message_GetAns>>(){}.getType());
        put("Message_ClearReq", new TypeToken<Header<Message_ClearReq>>(){}.getType());
        put("Message_ClearAns", new TypeToken<Header<Message_ClearAns>>(){}.getType());
    }};

    public static class Header<T> {
        public String cmd;
        public String user_uid;
        public T payload;
    }

    public static <T> String toJSON(String userUID, T obj)
    {
        Gson gson = new Gson();

        String cmd = obj.getClass().getSimpleName();
        Header<T> req = new Header<T>();
        req.cmd = cmd;
        req.user_uid = userUID;
        req.payload = obj;

        Type type = new TypeToken<Header<T>>(){}.getType();
        return gson.toJson(req, type);
    }

    public static <T> T fromJSON(String className, String json)
    {
        Gson gson = new Gson();
        Type type = TypeMap.get(className);
        Header<T> header = gson.fromJson(json, type);
        return header.payload;
    }

    // User
    public static class UserInfo {
        @SerializedName("user_uid")
        public String mUserUID;
        @SerializedName("user_name")
        public String mUserName;
    }

    public static class User_LoginReq {
        @SerializedName("user_uid")
        public String mUserUID;
        @SerializedName("user_name")
        public String mUserName;
    }

    public static class User_LoginAns {
        @SerializedName("request")
        public User_LoginReq mRequest;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    public static class User_UnregisterReq {
        @SerializedName("user_uid")
        public String mUserUID;
    }

    public static class User_UnregisterAns {
        @SerializedName("request")
        public User_UnregisterReq mRequest;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    // Group
    public static class Group_JoinReq {
        @SerializedName("group_uid")
        public String mGroupUID;
        @SerializedName("user_uid")
        public String mUserUID;
        @SerializedName("invitee_uids")
        public String[] mInviteeUIDs;
    }

    public static class Group_JoinAns {
        @SerializedName("request")
        public Group_JoinReq mRequest;
        @SerializedName("invitees")
        public UserInfo[] mInvitees;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    public static class Group_JoinNoti {
        @SerializedName("group_uid")
        public String mGroupUID;
        @SerializedName("user_uid")
        public String mUserUID;
    }

    public static class Group_LeaveReq {
        @SerializedName("group_uid")
        public String mGroupUID;
        @SerializedName("user_uid")
        public String mUserUID;
    }

    public static class Group_LeaveAns {
        @SerializedName("request")
        public Group_LeaveReq mRequest;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    public static class Group_LeaveNoti {
        @SerializedName("group_uid")
        public String mGroupUID;
        @SerializedName("user_info")
        public UserInfo mUserInfo;
    }

    public static class Group_InviteReq {
        @SerializedName("group_uid")
        public String mGroupUID;
        @SerializedName("user_uid")
        public String mUserUID;
        @SerializedName("invitee_uids")
        public String[] mInviteeUIDs;
    }

    public static class Group_InviteAns {
        @SerializedName("request")
        public Group_InviteReq mRequest;
        @SerializedName("invitees")
        public UserInfo[] mInvitees;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    public static class Group_InviteNoti {
        @SerializedName("group_uid")
        public String mGroupUID;
        @SerializedName("user_uid")
        public String mUserUID;
        @SerializedName("invitees")
        public UserInfo[] mInvitees;
    }

    public static class Group_InfoReq {
        @SerializedName("group_uid")
        public String mGroupUID;
        @SerializedName("user_uid")
        public String mUserUID;
    }

    public static class Group_InfoAns {
        @SerializedName("request")
        public Group_InfoReq mRequest;
        @SerializedName("members")
        public UserInfo[] mMembers;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    // Message
    public static class MessageInfo {
        @SerializedName("uid")
        public long mUID;
        @SerializedName("sender_uid")
        public String mSenderUID;
        @SerializedName("group_uid")
        public String mGroupUID;
        @SerializedName("message")
        public String mMessage;
        @SerializedName("countdown")
        public int mCountdown;
        @SerializedName("issued_at")
        public int mIssuedAt;
        @SerializedName("expires_at")
        public int mExpiresAt;
        @SerializedName("is_secret")
        public boolean mIsSecret;
        @SerializedName("recipient_count")
        public int mRecipientCount;
        @SerializedName("unveil_count")
        public int mUnveilCount;
    }

    public static class Message_SendReq {
        @SerializedName("sender_uid")
        public String mSenderUID;
        @SerializedName("target_uid")
        public String mTargetUID;
        @SerializedName("is_group")
        public boolean mIsGroup;
        @SerializedName("message")
        public String mMessage;
        @SerializedName("is_secret")
        public boolean mIsSecret;
    }

    public static class Message_SendAns {
        @SerializedName("request")
        public Message_SendReq mRequest;
        @SerializedName("message_info")
        public MessageInfo mMessageInfo;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    public static class Message_NewNoti {
        @SerializedName("message_info")
        public MessageInfo mMessageInfo;
    }

    public static class Message_CancelReq {
        @SerializedName("sender_uid")
        public String mSenderUID;
        @SerializedName("target_uid")
        public String mTargetUID;
        @SerializedName("is_group")
        public boolean mIsGroup;
        @SerializedName("message_uid")
        public long mMessageUID;
    }

    public static class Message_CancelAns {
        @SerializedName("request")
        public Message_CancelReq mRequest;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    public static class Message_CancelNoti {
        @SerializedName("message_info")
        public MessageInfo mMessageInfo;
    }

    public static class Message_OpenReq {
        @SerializedName("sender_uid")
        public String mSenderUID;
        @SerializedName("target_uid")
        public String mTargetUID;
        @SerializedName("is_group")
        public boolean mIsGroup;
        @SerializedName("message_uid")
        public long mMessageUID;
    }

    public static class Message_OpenAns {
        @SerializedName("request")
        public Message_OpenReq mRequest;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    public static class Message_OpenNoti {
        @SerializedName("sender_uid")
        public String mSenderUID;
        @SerializedName("target_uid")
        public String mTargetUID;
        @SerializedName("is_group")
        public boolean mIsGroup;
        @SerializedName("message_uid")
        public long mMessageUID;
    }

    public static class Message_ReadReq {
        @SerializedName("user_uid")
        public String mUserUID;
        @SerializedName("sender_uid")
        public String mSenderUID;
        @SerializedName("is_group")
        public boolean mIsGroup;
        @SerializedName("message_uids")
        public long[] mMessageUIDs;
    }

    public static class Message_ReadAns {
        @SerializedName("request")
        public Message_ReadReq mRequest;
        @SerializedName("message_info")
        public MessageInfo[] mMessageInfo;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    public static class Message_ReadNoti {
        @SerializedName("message_info")
        public MessageInfo[] mMessageInfo;
    }

    public static class Message_GetReq {
        @SerializedName("user_uid")
        public String mUserUID;
        @SerializedName("target_uid")
        public String mTargetUID;
        @SerializedName("is_group")
        public boolean mIsGroup;
        @SerializedName("since_uid")
        public long mSinceUID;
        @SerializedName("count")
        public int mCount;
        @SerializedName("message_uids")
        public long[] mMessageUIDs;
    }

    public static class Message_GetAns {
        @SerializedName("request")
        public Message_GetReq mRequest;
        @SerializedName("message_info")
        public MessageInfo[] mMessageInfo;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }

    public static class Message_ClearReq {
        @SerializedName("user_uid")
        public String mUserUID;
        @SerializedName("target_uid")
        public String mTargetUID;
    }

    public static class Message_ClearAns {
        @SerializedName("request")
        public Message_ClearAns mRequest;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
    }
}
