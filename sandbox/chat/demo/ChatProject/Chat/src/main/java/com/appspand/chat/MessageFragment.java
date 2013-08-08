package com.appspand.chat;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.List;


/**
 * Created by wannafree on 13. 7. 12..
 */

public class MessageFragment extends Fragment {
    /**
     * The fragment argument representing the section number for this
     * fragment.
     */

    private static final String DEBUG_TAG  = "[LOG_MESSAGEFRAGMENT]";

    private DataSource mDatasource;
    private SharedPreferences mSharedPref;
    private String mMyID;
    private ArrayAdapter<Message> mDataAdapter;

    public MessageFragment() {
    }

    @Override
    public void onCreate (Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

        mSharedPref = getActivity().getSharedPreferences("pref", 0);
        mMyID = mSharedPref.getString("id", "");

        String databaseName = mMyID + ".db";
        mDatasource = new DataSource(getActivity(), databaseName);
        mDatasource.open();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View rootView = inflater.inflate(R.layout.message_fragment, container, false);
        return rootView;

    }

    public void displayListView() {

        //Array list of countries
        List<Message> values = mDatasource.getLastMessage();

        //create an ArrayAdaptar from the String Array
        mDataAdapter = new ArrayAdapter<Message>(getActivity(),  R.layout.message_list, values);
        ListView listView = (ListView) getView().findViewById(R.id.messageListView);
        // Assign adapter to ListView
        listView.setAdapter(mDataAdapter);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View view,
                                    int position, long id) {

                Message selectedMessage = (Message)parent.getAdapter().getItem(position);

                Intent intent = new Intent ( getActivity(), ChatRoomActivity.class );
                intent.putExtra("room_id",selectedMessage.getRoomID());
                intent.putExtra("my_id",mMyID);
                startActivity ( intent );

            }
        });
    }
}
