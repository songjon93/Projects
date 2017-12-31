package cats.coding.istalku;

import android.Manifest;
import android.app.DatePickerDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.app.Fragment;
import android.app.FragmentManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.DatePicker;
import android.widget.ListView;
import android.widget.Toast;

public class Menu extends AppCompatActivity {
    ArrayList<Fragment> fragments = new ArrayList<>();
    ArrayList<Data> dataList;
    static String fileName;
    MenuItem calendar;
    Storage storage;
    double totalDist = 0;
    double max_speed = 0;
    HourlyData[] hourlyDataList;
    static SharedPreferences sp;
    private int index;
    int mSteps;
    BroadcastReceiver receiver;
    private DialogFragment dateDialog;

    //Set a navigation view listener
    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            FragmentManager fm = getFragmentManager();
            switch (item.getItemId()) {
                case R.id.navigation_home:
                    index = 0;
                    fm.beginTransaction().replace(R.id.frame_content, fragments.get(0)).commit();
                    return true;
                case R.id.navigation_dashboard:
                    index = 1;
                    fm.beginTransaction().replace(R.id.frame_content, fragments.get(1)).commit();
                    return true;
                case R.id.navigation_notifications:
                    index = 2;
                    fm.beginTransaction().replace(R.id.frame_content, fragments.get(2)).commit();
                    return true;
            }

            return false;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
        initializeTabs();
        index = 0;
        getSupportActionBar().setDisplayUseLogoEnabled(true);
        getSupportActionBar().setDisplayShowHomeEnabled(true);
        getSupportActionBar().setTitle("");
        getSupportActionBar().setIcon(R.drawable.round_icon_small);
        sp = PreferenceManager.getDefaultSharedPreferences(this);
        BottomNavigationView navigation = findViewById(R.id.navigation);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);
        dateDialog = new DatePickerFragment();
        storage = new Storage(this);

        if (fileName != null){
            updateData(fileName);
            Log.d("fileName", fileName);
        }
        receiveBroadcast();
        checkPermissions();
    }

    // when you pause the view, save the filename and the index of the navigation view you are currently on
    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putString("fileName", fileName);
        outState.putInt("index", index);
    }

    // restore tab and file
    @Override
    protected void onRestoreInstanceState(Bundle savedInstanceState) {
        super.onRestoreInstanceState(savedInstanceState);
        fileName = savedInstanceState.getString("fileName");
        index = savedInstanceState.getInt("index");
        initializeTabs();
//        Log.d("index", String.valueOf(index));
        if (fileName == null || fileName.length() == 0) return;
        updateCalendar();
        updateData(fileName);
    }

    // parse the stored data into hourly data for graphical purpose
    public void updateHourlyData() {
        Data previous = dataList.get(0);
        hourlyDataList = new HourlyData[24];
        boolean[] hourSeen = new boolean[24];
        totalDist = 0;
        max_speed = 0;
        for (Data datum: dataList) {
            int hour = Integer.parseInt(datum.getTime().substring(0,2));
            double distance = Statistics.Haversine.haversine(
                    Double.parseDouble(previous.getLat()),
                    Double.parseDouble(previous.getLng()),
                    Double.parseDouble(datum.getLat()),
                    Double.parseDouble(datum.getLng()));

            double speed = 0;
            SimpleDateFormat format = new SimpleDateFormat("HHmmss");
            try{
                Date date1 = format.parse(previous.getTime());
                Date date2 = format.parse(datum.getTime());
                Log.d("time_ diff",String.valueOf(date2.getTime() - date1.getTime()));
                speed = (distance * 60 * 60000) / ((date2.getTime() - date1.getTime()));
                Log.d("speed",String.valueOf(speed));

            } catch (ParseException e){
                Log.d("Error", e.toString());
            }

            if (max_speed < speed) max_speed = speed;


            totalDist += distance;
            Log.d("distance", String.valueOf(distance));
            Log.d("hour", String.valueOf(hour));

            if (!hourSeen[hour]) {
                HourlyData newHourlyData = new HourlyData(hour);
                hourlyDataList[hour] = (newHourlyData);
                hourSeen[hour] = true;
            } else {
                hourlyDataList[hour].distance += distance;
                Log.d("distance", String.valueOf(distance));
            }
            previous = datum;
        }

        for (HourlyData datum: hourlyDataList) {
//            Log.d("hourlyData", datum.getDistance());
        }
    }

    // update the action menu title to the selected date
    public void updateCalendar(){
        String date = "";
        for(int i = 0; i < fileName.length(); i += 1){
            if (i < 4 || i == 5 || i == 7) date += fileName.charAt(i);
            else date += "/" + fileName.charAt(i);
        }
        if(calendar != null) calendar.setTitle(date);
    }

    // update the data in accordance to the selected file
    public void updateData(String file){
        totalDist = 0;
        max_speed = 0;
        dataList = storage.readFile(file);
        mSteps = storage.readSteps(file + "_steps");
        if (dataList != null){
            updateHourlyData();

            for (Data datum : dataList){
                Log.d("time", datum.getTime());
                Log.d("lat", datum.getLat());
                Log.d("lng", datum.getLng());
            }
        }

        else{
            Log.d("Error", "File Not Found");
            Toast.makeText(this, "No file found for the selected date", Toast.LENGTH_SHORT).show();
        }

        initializeTabs();
    }

    // listen to whether a service has been destroyed or not
    // listen to the file update, and update the view accordingly
    protected void receiveBroadcast(){
        receiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                Log.d("debug", "broadcast received");
                if (intent.getAction() == "STOP SERVICE")
                    invalidateOptionsMenu();
                else if (fileName != null) {
                    Toast.makeText(context, "Updating", Toast.LENGTH_SHORT).show();
                    updateCalendar();
                    updateData(fileName);
                }
            }
        };
        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction("STOP SERVICE");
        intentFilter.addAction("UPDATE");
        registerReceiver(receiver, intentFilter);
    }


    // initialize the tabs in the beginning
    public void initializeTabs(){
        fragments.clear();
        Fragment home = new Home();
        Fragment stats = new Statistics();
        Fragment map = new TimeMachine();

        fragments.add(home);
        fragments.add(stats);
        fragments.add(map);

        Log.d("index", String.valueOf(index));

        if(findViewById(R.id.frame_content) != null)
            getFragmentManager().beginTransaction().replace(R.id.frame_content, fragments.get(index)).commit();
    }

    // show the date picker fragment
    public void selectDate(){
        dateDialog.show(getFragmentManager(), "date");
    }

    // search for time stamp
    public void search(View view){
        ((TimeMachine)fragments.get(2)).showQuery(view);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch(item.getItemId()){
            case R.id.action_start:
                if (!sp.getBoolean("track", false)) {
                    item.setIcon(R.drawable.bino_small_x);
                    startForeground();
                    sp.edit().putBoolean("track", true).apply();
                } else {
                    item.setIcon(R.drawable.bino_small);
                    stopForeground();
                    sp.edit().putBoolean("track", false).apply();
                }
                break;
            case R.id.action_tutorial:
                sp.edit().putBoolean("first", true).apply();
                break;
            case R.id.date_selection:
                selectDate();
                break;
            case R.id.action_refresh:
                if(fileName != null) updateData(fileName);
                break;
            case R.id.delete:
                deleteFile();
                break;
            default:
                setGPS();
        }

        return true;
    }

    public void setGoalDistance(View view){
        ((Home)fragments.get(0)).setGoalDistance(view);
    }

    public void setGoalStep(View view){
        ((Home)fragments.get(0)).setGoalStep(view);
    }

    public void setGoalSpeed(View view){
        ((Home)fragments.get(0)).setGoalSpeed(view);
    }


    // delete file for the selected date
    public void deleteFile(){
        if (dataList == null){
            Toast.makeText(this, "There is no file for the selected date", Toast.LENGTH_SHORT).show();
        } else {
            this.deleteFile(fileName);
            dataList = null;
        }
    }

    // set gps frequeny, show the list view dialog
    public void setGPS(){
        FragmentManager fm = getFragmentManager();
        GpsDialog gpsDialog = new GpsDialog();
        gpsDialog.show(fm, "gps");
    }

    @Override
    public boolean onCreateOptionsMenu(android.view.Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);
        calendar = menu.getItem(1);
        if (fileName != null) updateCalendar();
        if (sp.getBoolean("track", false)) menu.getItem(0).setIcon(R.drawable.bino_small_x);
        else menu.getItem(0).setIcon(R.drawable.bino);
        return true;
    }

    private void checkPermissions() {
        if ((checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) || (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED)
                || (checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) || (checkSelfPermission(Manifest.permission.INTERNET) != PackageManager.PERMISSION_GRANTED)) {
            requestPermissions(new String[]{Manifest.permission.ACCESS_COARSE_LOCATION, Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.INTERNET}, 0);
        }
    }

    // start the tracking service
    public void startForeground(){
        Intent foreground = new Intent(this, ForegroundService.class);
        foreground.setAction("START");
        startService(foreground);
        Toast.makeText(this, "I am keeping an eye on you", Toast.LENGTH_SHORT).show();
    }

    // stop the tracking service
    public void stopForeground(){
        Intent foreground = new Intent(this, ForegroundService.class);
        stopService(foreground);
        Toast.makeText(this, "Ok, I will stop stalking", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(receiver);
    }

    // A date picker displayed via dialog fragment
    public static class DatePickerFragment extends DialogFragment
            implements DatePickerDialog.OnDateSetListener {

        View view;

        @Nullable
        @Override
        public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
            view = super.onCreateView(inflater, container, savedInstanceState);
            return view;
        }

        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            // Use the current date as the default date in the picker
            final Calendar c = Calendar.getInstance();
            int year = c.get(Calendar.YEAR);
            int month = c.get(Calendar.MONTH);
            int day = c.get(Calendar.DAY_OF_MONTH);
            return new DatePickerDialog(getActivity(), this, year, month, day);
        }

        @Override
        public void onDateSet(DatePicker view, int year, int month, int day) {
            Menu curActivity = (Menu) getActivity();
            String date = String.valueOf(year) + "/" + String.valueOf(month + 1) + "/" + String.valueOf(day);
            fileName = String.valueOf(year) + String.valueOf(month + 1) + String.valueOf(day);
            curActivity.updateCalendar();
            curActivity.updateData(fileName);
        }
    }

    // GPS frequency selector using a list view displayed via dialog fragment
    public static class GpsDialog extends DialogFragment {
        public View onCreateView(LayoutInflater inflater,
                                 ViewGroup container, Bundle savedInstanceState) {
            //---Inflate the layout for this fragment---
            Log.d("Dialog", "onCreateView");
            View v = inflater.inflate(
                    R.layout.gps_dialog, container, false);
            final ListView freq = v.findViewById(R.id.list);
            final Fragment parent = this;
            freq.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                    switch (i) {
                        case 0:
                            sp.edit().putInt("gps_freq", 30000).apply();
                            break;
                        case 1:
                            sp.edit().putInt("gps_freq", 60000).apply();
                            break;
                        case 2:
                            sp.edit().putInt("gps_freq", 300000).apply();
                            break;
                        case 3:
                            sp.edit().putInt("gps_freq", 180000).apply();
                            break;
                        case 4:
                            sp.edit().putInt("gps_freq", 3600000).apply();
                            break;
                    }
                    getFragmentManager().beginTransaction().remove(parent).commit();
                }
            });
            return v;
        }
    }
}
