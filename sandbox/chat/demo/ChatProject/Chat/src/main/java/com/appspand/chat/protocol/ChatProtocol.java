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

        put("Group_JoinReq", new TypeToken<Header<Group_JoinReq>>(){}.getType());
        put("Group_JoinAns", new TypeToken<Header<Group_JoinAns>>(){}.getType());
        put("Group_JoinNoti", new TypeToken<Header<Group_JoinNoti>>(){}.getType());
        put("Group_LeaveReq", new TypeToken<Header<Group_LeaveReq>>(){}.getType());
        put("Group_LeaveAns", new TypeToken<Header<Group_LeaveAns>>(){}.getType());
        put("Group_LeaveNoti", new TypeToken<Header<Group_LeaveNoti>>(){}.getType());
        put("Group_InviteReq", new TypeToken<Header<Group_InviteReq>>(){}.getType());
        put("Group_InviteAns", new TypeToken<Header<Group_InviteAns>>(){}.getType());
        put("Group_InviteNoti", new TypeToken<Header<Group_InviteNoti>>(){}.getType());

        put("Message_SendReq", new TypeToken<Header<Message_SendReq>>(){}.getType());
        put("Message_SendAns", new TypeToken<Header<Message_SendAns>>(){}.getType());
        put("Message_NewNoti", new TypeToken<Header<Message_NewNoti>>(){}.getType());
        put("Message_ReadReq", new TypeToken<Header<Message_ReadReq>>(){}.getType());
        put("Message_ReadAns", new TypeToken<Header<Message_ReadAns>>(){}.getType());
        put("Message_ReadNoti", new TypeToken<Header<Message_ReadNoti>>(){}.getType());
        put("Message_GetReq", new TypeToken<Header<Message_GetReq>>(){}.getType());
        put("Message_GetAns", new TypeToken<Header<Message_GetAns>>(){}.getType());
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
        @SerializedName("user_uid")
        public String mUserUID;
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
        @SerializedName("invitee_uids")
        public String[] mInviteeUIDs;
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
    }

    public static class Message_GetAns {
        @SerializedName("request")
        public Message_GetReq mRequest;
        @SerializedName("error_code")
        public int mErrorCode;
        @SerializedName("error_message")
        public String mErrorMessage;
        @SerializedName("message_info")
        public MessageInfo[] mMessageInfo;
    }
}
