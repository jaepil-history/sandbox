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

public class FriendFragment extends Fragment {
    /**
     * The fragment argument representing the section number for this
     * fragment.
     */

    private static final String DEBUG_TAG  = "[LOG_FRIENDFRAGMENT]";

    private DataSource mDatasource;
    private SharedPreferences mSharedPref;
    private String mMyID;
    private ArrayAdapter<Friend> mDataAdapter;

    public FriendFragment() {
    }

    public void onAddFriend (String friend_id)
    {
        Friend insertedFriend = mDatasource.insertFriend( friend_id );
        mDataAdapter.add( insertedFriend );

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
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        //Generate list View from ArrayList
        displayListView();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View rootView = inflater.inflate(R.layout.friend_fragment, container, false);
        return rootView;

    }

    private void displayListView() {

        //Array list of countries
        List<Friend> values = mDatasource.getAllFriends();

        //create an ArrayAdaptar from the String Array
        mDataAdapter = new ArrayAdapter<Friend>(getActivity(),  R.layout.friend_list, values);
        ListView listView = (ListView) getView().findViewById(R.id.friendListView);
        // Assign adapter to ListView
        listView.setAdapter(mDataAdapter);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View view,
                                    int position, long id) {

                Friend selectedFriend = (Friend)parent.getAdapter().getItem(position);

                //start Chat with SelectedFriend
                Intent intent = new Intent ( getActivity(), ChatRoomActivity.class );
                intent.putExtra("room_id",selectedFriend.toString());
                intent.putExtra("my_id",mMyID);
                startActivity ( intent );

            }
        });

    }

}
